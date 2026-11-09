#!/usr/bin/env python3
"""Run a command (archinstall) and keep a Devium progress bar pinned to the bottom line
of the terminal while it installs.

    install-progress.py archinstall --config FILE ...

The bar appears once the disk work starts (the menus before that are left alone).
The terminal's scroll region is shrunk by one line, and the program is told the terminal
is one line shorter, so its output scrolls above the bar and never covers it.
"""
import fcntl
import os
import pty
import re
import select
import signal
import struct
import sys
import termios
import time
import tty

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[()][A-Z0-9]|\x1b[78=>]")
BLUE = "\x1b[38;2;143;180;216m"
LAV = "\x1b[38;2;180;184;224m"
DIM = "\x1b[38;2;92;104;120m"
BG = "\x1b[48;2;30;35;42m"
RST = "\x1b[0m"

# (substring in the output, percent, label) - the bar never goes backwards
STAGES = [
    ("Wiping partitions", 2, "Preparing the disk"),
    ("Creating partitions", 4, "Preparing the disk"),
    ("Starting installation", 6, "Starting"),
    ("Waiting for", 7, "Getting ready"),
    ("Installing packages", 9, "Installing the base system"),
    ("Building image", 86, "Building the startup image"),
    ("bootloader", 88, "Setting up the bootloader"),
    ("Installing systemd bootloader", 88, "Setting up the bootloader"),
    ("grub", 88, "Setting up the bootloader"),
    ("Creating user", 90, "Creating your user"),
    ("custom command", 92, "Adding Devium's apps and look"),
    ("devium-setup", 93, "Adding Devium's apps and look"),
    ("Installation completed", 100, "Done! Devium is installed"),
]
ACTIVATE = ("Wiping partitions", "Creating partitions", "Starting installation", "Starting device modifications")


class Bar:
    def __init__(self):
        self.active = False
        self.pct = 0
        self.label = "Preparing"
        self.totals = []          # pacstrap package totals seen (1st = base system, 2nd = Devium)
        self.started = time.time()
        self.last_draw = 0.0
        self.buf = ""

    def feed(self, text):
        self.buf = (self.buf + ANSI.sub("", text))[-4000:]
        for key, pct, label in STAGES:
            if key in text and pct >= self.pct:
                self.set(pct, label)
        for done, total, what in re.findall(r"\(\s*(\d+)/(\d+)\)\s+(installing|upgrading|reinstalling|checking|loading)",
                                            self.buf):
            self.packages(int(done), int(total), what == "installing" or what == "upgrading" or what == "reinstalling")
        m = re.findall(r"Total \(\s*(\d+)/(\d+)\)", self.buf)
        if m:
            self.packages(int(m[-1][0]), int(m[-1][1]), False, download=True)
        self.buf = self.buf[-300:]

    def packages(self, done, total, installing, download=False):
        if total not in self.totals:
            self.totals.append(total)
        phase = self.totals.index(total)
        frac = done / max(total, 1)
        if phase == 0:   # base system: 9-30 %
            lo, hi, name = (9, 18, "Downloading the base system") if download else (18, 30, "Installing the base system")
        else:            # Devium's packages: 30-85 %
            lo, hi, name = (30, 55, "Downloading Devium's packages") if download else (55, 85, "Installing Devium's packages")
        if not download and not installing:
            return
        pct = int(lo + (hi - lo) * frac)
        if pct >= self.pct:
            self.set(pct, f"{name} ({done} of {total})")

    def set(self, pct, label):
        self.pct, self.label = min(pct, 100), label


def winsize(fd):
    try:
        r, c = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, b"\0" * 4))
        return max(r, 5), max(c, 20)
    except OSError:
        return 24, 80


def set_child_size(fd, rows, cols):
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))


def main():
    cmd = sys.argv[1:]
    if not cmd:
        print(__doc__)
        return 2
    out = sys.stdout.buffer
    rows, cols = winsize(0)
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(cmd[0], cmd)
    set_child_size(fd, rows, cols)
    bar = Bar()

    def draw(force=False):
        if not bar.active:
            return
        now = time.time()
        if not force and now - bar.last_draw < 0.25:
            return
        bar.last_draw = now
        width = max(10, min(40, cols - 50))
        filled = int(width * bar.pct / 100)
        elapsed = int(now - bar.started)
        eta = ""
        if 5 < bar.pct < 100:
            left = int(elapsed * (100 - bar.pct) / bar.pct)
            eta = f"  ~{left // 60} min left" if left >= 60 else "  <1 min left"
        text = (f" {LAV}Devium{RST}{BG} {BLUE}{'█' * filled}{DIM}{'░' * (width - filled)}{RST}{BG}"
                f" {bar.pct:3d}%  {bar.label}{DIM}{eta}")
        visible = len(ANSI.sub("", text))
        pad = " " * max(0, cols - visible)
        out.write(f"\x1b7\x1b[{rows};1H{BG}\x1b[2K{text}{pad}{RST}\x1b8".encode())
        out.flush()

    def activate():
        bar.active = True
        bar.started = time.time()
        # make room: scroll everything up one line, then fence off the last line
        out.write(f"\n\x1b7\x1b[1;{rows - 1}r\x1b8\x1b[A".encode())
        out.flush()
        set_child_size(fd, rows - 1, cols)
        os.kill(pid, signal.SIGWINCH)
        draw(force=True)

    def on_resize(*_):
        nonlocal rows, cols
        rows, cols = winsize(0)
        if bar.active:
            out.write(f"\x1b7\x1b[1;{rows - 1}r\x1b8".encode())
            set_child_size(fd, rows - 1, cols)
            draw(force=True)
        else:
            set_child_size(fd, rows, cols)
        os.kill(pid, signal.SIGWINCH)

    signal.signal(signal.SIGWINCH, on_resize)
    old = termios.tcgetattr(0) if os.isatty(0) else None
    if old:
        tty.setraw(0)
    try:
        while True:
            try:
                r, _, _ = select.select([0, fd], [], [], 0.5)
            except InterruptedError:
                continue
            if fd in r:
                try:
                    data = os.read(fd, 65536)
                except OSError:
                    break
                if not data:
                    break
                text = data.decode(errors="replace")
                if not bar.active and any(k in text for k in ACTIVATE):
                    out.write(data)
                    out.flush()
                    activate()
                    bar.feed(text)
                    continue
                out.write(data)
                out.flush()
                bar.feed(text)
                tail = text[-12:]
                if "\x1b" not in tail or re.search(r"\x1b\[[0-9;?]*[A-Za-z]$", tail):
                    draw()
            if 0 in r:
                try:
                    data = os.read(0, 1024)
                except OSError:
                    data = b""
                if data:
                    os.write(fd, data)
            elif bar.active:
                draw()   # keep the timer fresh even when nothing prints
    finally:
        if old:
            termios.tcsetattr(0, termios.TCSADRAIN, old)
        if bar.active:
            draw(force=True)
            out.write(f"\x1b7\x1b[r\x1b8\n".encode())   # give the whole screen back
            out.flush()
    _, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status)


if __name__ == "__main__":
    sys.exit(main())
