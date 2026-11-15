"""Devium Tools > Background and extras: turn off apps that start with you, switch off system services you
don't use, and remove the extra apps Devium comes with. Everything can be turned back on / added back."""
import configparser
import glob
import os
import re
import shutil
import subprocess

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QGridLayout, QMessageBox, QWidget

import tools_extra as X
from devium_i18n import T

HOME = os.path.expanduser("~")
SYSTEM_AUTOSTART = "/etc/xdg/autostart"
USER_AUTOSTART = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config")), "autostart")
DESKTOP = os.environ.get("XDG_CURRENT_DESKTOP", "")

# Things the desktop needs: never offered here (sound, passwords, accessibility, the panel...)
ESSENTIAL = re.compile(r"^(devium-firstrun|devium-setup-wizard|polkit|.*polkit.*|xdg-user-dirs.*|at-spi.*|pipewire.*|"
                       r"wireplumber|gnome-keyring.*|.*kwallet.*|org\.kde\.plasmashell|org\.kde\.kaccess|kaccess|"
                       r"xembedsniproxy|gmenudbusmenuproxy|.*powerdevil.*|xfsettingsd|xfce4-settings-helper.*|"
                       r"org\.kde\.xwaylandvideobridge|geoclue.*|.*im-launch.*|ibus.*|fcitx.*|nm-applet|"
                       r"xfce4-notifyd|print-applet|org\.kde\.kgpg|spice-vdagent|vboxclient.*|vmware-user.*)$")

# Friendlier words for common background apps
NICE = {
    "devium-crash-catcher": ("Crash catcher", "Offers to send a report when an app crashes"),
    "devium-loading": ("Loading screen", "Covers the desktop while it loads after you log in"),
    "devium-snap-assist": ("Snap Assist", "Pick a window for the other half when you snap one to the side"),
    "devium-desk-widgets": ("Devium widgets", "Widgets on the desktop (Xfce and Hyprland)"),
    "org.kde.discover.notifier": ("Update notifications (Discover)", "Pop-ups about app updates (Devium Updates does this too)"),
    "org.kde.kdeconnect.daemon": ("Phone link (KDE Connect)", "Lets your phone connect to this computer"),
    "archpill": ("ArchPill", "The pill at the top of the screen"),
    "linux-magnify": ("Linux Magnify", "The magnifying dock"),
    "baloo_file": ("File search indexing", "Indexes files so search is instant (uses memory and disk)"),
    "org.kde.yakuake": ("Yakuake", "Drop-down terminal"),
}

# System services people often don't need (root; helper only touches these)
SERVICES = [
    ("bluetooth", "Bluetooth", "Wireless headphones, mice and keyboards", ["bluetooth.service"]),
    ("printing", "Printing", "Printers and the print queue", ["cups.socket", "cups.service"]),
    ("avahi", "Network discovery", "Finds printers, phones and shared folders on your network", ["avahi-daemon.service", "avahi-daemon.socket"]),
    ("modem", "Mobile broadband modems", "Only needed for 4G/5G modems and SIM cards in laptops", ["ModemManager.service"]),
    ("sshd", "SSH server", "Lets other computers log in to this one over the network", ["sshd.service"]),
    ("docker", "Docker", "Starts the Docker engine when something uses it", ["docker.socket", "docker.service"]),
    ("autoupdate", "Automatic updates", "Installs updates by itself once a day", ["devium-autoupdate.timer"]),
    ("health", "Daily disk health check", "Checks your disks once a day and warns before one fails", ["devium-health.timer"]),
]

# The extra apps Devium comes with that are safe to remove (the helper only removes these)
EXTRAS = [
    ("kate", "Kate", "Text and code editor", ["kate"]),
    ("gwenview", "Gwenview", "Picture viewer", ["gwenview"]),
    ("okular", "Okular", "PDF and document viewer", ["okular"]),
    ("ark", "Ark", "Opens zip and other archive files", ["ark"]),
    ("kcalc", "KCalc", "Calculator", ["kcalc"]),
    ("spectacle", "Spectacle", "Screenshots (Print key, Meta+Shift+S)", ["spectacle"]),
    ("discover", "Discover", "App store (Devium Configure can install apps too)", ["discover"]),
    ("kinfocenter", "Info Center", "Details about your hardware", ["kinfocenter"]),
    ("plasma-systemmonitor", "System Monitor", "Live CPU, memory and app list", ["plasma-systemmonitor"]),
    ("timeshift", "Timeshift", "Restore points before updates (updates can't be undone without it)", ["timeshift"]),
    ("neovim", "Neovim", "Terminal code editor", ["neovim"]),
    ("btop", "btop", "Terminal system monitor", ["btop"]),
    ("starship", "Starship", "The colourful terminal prompt", ["starship"]),
    ("mousepad", "Mousepad", "Text editor", ["mousepad"]),
    ("ristretto", "Ristretto", "Picture viewer", ["ristretto"]),
    ("atril", "Atril", "PDF viewer", ["atril"]),
    ("galculator", "Galculator", "Calculator", ["galculator"]),
    ("file-roller", "File Roller", "Opens zip and other archive files", ["file-roller", "thunar-archive-plugin"]),
    ("xfce4-screenshooter", "Screenshooter", "Screenshots", ["xfce4-screenshooter"]),
    ("xfce4-taskmanager", "Task Manager", "List of running programs", ["xfce4-taskmanager"]),
    ("xfce4-clipman-plugin", "Clipman", "Clipboard history", ["xfce4-clipman-plugin"]),
    ("gnome-disk-utility", "Disks", "Format and check drives", ["gnome-disk-utility"]),
    ("loupe", "Loupe", "Picture viewer", ["loupe"]),
    ("papers", "Papers", "PDF viewer", ["papers"]),
    ("gnome-calculator", "Calculator", "Calculator", ["gnome-calculator"]),
    ("nwg-look", "nwg-look", "GTK theme settings", ["nwg-look"]),
]


def sh(cmd, timeout=15):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def installed(pkg):
    return subprocess.run(["pacman", "-Q", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0 \
        if shutil.which("pacman") else False


# ---------------------------------------------------------------------------- background apps (autostart)
def read_desktop(path):
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    cp.optionxform = str
    try:
        cp.read(path, encoding="utf-8")
        return dict(cp["Desktop Entry"])
    except Exception:
        return None


def shown_here(e):
    only = [x for x in e.get("OnlyShowIn", "").split(";") if x]
    never = [x for x in e.get("NotShowIn", "").split(";") if x]
    here = DESKTOP.split(":")
    if only and not any(x in here for x in only):
        return False
    return not any(x in here for x in never)


def autostart_entries():
    """[{id, name, desc, on, exec, user_path}] for apps that start when you log in."""
    found = {}
    for d in (SYSTEM_AUTOSTART, USER_AUTOSTART):
        for f in sorted(glob.glob(os.path.join(d, "*.desktop"))):
            e = read_desktop(f)
            if e is None:
                continue
            fid = os.path.basename(f)[:-8]
            found[fid] = (e, f)    # the user's own file wins over the system one
    out = []
    for fid, (e, f) in sorted(found.items()):
        if ESSENTIAL.match(fid) or e.get("Type", "Application") != "Application" or not shown_here(e):
            continue
        name, desc = NICE.get(fid, (e.get("Name", fid), e.get("Comment", "")))
        on = e.get("Hidden", "false").lower() != "true" and e.get("X-GNOME-Autostart-enabled", "true").lower() != "false"
        out.append({"id": fid, "name": name, "desc": desc, "on": on, "exec": e.get("Exec", ""),
                    "user_path": os.path.join(USER_AUTOSTART, fid + ".desktop"), "src": f})
    # ArchPill and Linux Magnify may start another way (their own autostart names)
    return out


def set_autostart(entry, on):
    """Turn an app that starts at login on or off (a personal override, so the system file stays as it is)."""
    os.makedirs(USER_AUTOSTART, exist_ok=True)
    path = entry["user_path"]
    if entry["src"] != path:   # copy the system entry so we can change it just for you
        shutil.copy(entry["src"], path)
    text = open(path).read()
    text = re.sub(r"^Hidden=.*\n?", "", text, flags=re.M)
    text = re.sub(r"^X-GNOME-Autostart-enabled=.*\n?", "", text, flags=re.M)
    if not on:
        text = text.replace("[Desktop Entry]\n", "[Desktop Entry]\nHidden=true\n", 1)
    with open(path, "w") as f:
        f.write(text)
    if on and entry["src"] == path and os.path.exists(os.path.join(SYSTEM_AUTOSTART, entry["id"] + ".desktop")):
        os.remove(path)    # back to the system default
    if not on:
        stop_now(entry)


def program(entry):
    words = [w for w in entry["exec"].split() if not w.startswith("%") and "=" not in w]
    return os.path.basename(words[0]) if words else ""


def stop_now(entry):
    prog = program(entry)
    if prog and prog not in ("sh", "bash", "env", "python3", "python"):
        subprocess.run(["pkill", "-u", str(os.getuid()), "-x", prog[:15]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif entry["id"].startswith("devium-"):
        subprocess.run(["pkill", "-u", str(os.getuid()), "-f", "/" + entry["id"]], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)


def memory_of(entry):
    """How much memory the app is using right now (MB), or None if it's not running."""
    prog = program(entry)
    generic = prog in ("sh", "bash", "env", "python3", "python", "")
    total = 0
    for st in glob.glob("/proc/[0-9]*/status"):
        try:
            if os.stat(st).st_uid != os.getuid():
                continue
            pid = st.split("/")[2]
            args = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
            args = [x.decode(errors="replace") for x in args if x]
            if not args:
                continue
            first = os.path.basename(args[0])
            second = os.path.basename(args[1]) if len(args) > 1 else ""
            if (not generic and first == prog) or second == entry["id"] or (not generic and second == prog):
                for line in open(st):
                    if line.startswith("VmRSS:"):
                        total += int(line.split()[1])
        except (OSError, ValueError):
            pass
    return round(total / 1024) if total else None


def cell(box, desc):
    """A tick box with its explanation underneath."""
    from PyQt6.QtWidgets import QVBoxLayout
    w = QWidget()
    v = QVBoxLayout(w)
    v.setContentsMargins(0, 2, 0, 2)
    v.setSpacing(0)
    box.setStyleSheet("font-weight: 600;")
    v.addWidget(box)
    if desc:
        d = X.label(desc, "subtitle")
        d.setContentsMargins(26, 0, 0, 0)
        v.addWidget(d)
    return w


# ---------------------------------------------------------------------------- the page
def make_page(win):
    page = X.Page(T("Background and extras"),
                  T("Turn off apps that start with you, switch off services you don't use, and remove extra apps. "
                    "Anything here can be turned back on or added back later."))
    # --- background apps
    page.bg_grid = QGridLayout()
    page.bg_grid.setVerticalSpacing(2)
    bg = QWidget()
    bg.setLayout(page.bg_grid)
    page.bg_total = X.label("", "subtitle")
    page.add(X.card(X.label(T("Apps that start with you"), "h2"),
                    X.label("These start in the background every time you log in. Untick one to stop it now and stop it "
                            "starting again.", "subtitle"), bg, page.bg_total))
    # --- services
    page.svc_grid = QGridLayout()
    page.svc_grid.setVerticalSpacing(2)
    svc = QWidget()
    svc.setLayout(page.svc_grid)
    page.add(X.card(X.label(T("System services"), "h2"),
                    X.label("Parts of the system that run all the time. Switch off the ones you never use (asks for your "
                            "password).", "subtitle"), svc))
    # --- extra apps
    page.ex_grid = QGridLayout()
    page.ex_grid.setVerticalSpacing(2)
    ex = QWidget()
    ex.setLayout(page.ex_grid)
    page.ex_note = X.label("", "subtitle")
    page.add(X.card(X.label(T("Extra apps Devium comes with"), "h2"),
                    X.label("Tick the ones you don't want and press Remove. Removed apps don't come back with updates; "
                            "\"Add back removed apps\" brings them back.", "subtitle"), ex, page.ex_note,
                    X.row(X.button(T("Remove ticked apps"), lambda: remove_extras(page), True, "edit-delete"),
                          X.button(T("Add back removed apps"), lambda: add_back(page), icon="list-add"))))
    page.finish()

    def clear(grid):
        while grid.count():
            w = grid.takeAt(0).widget()
            if w:
                w.deleteLater()

    def fill():
        # background apps
        clear(page.bg_grid)
        total = 0
        for i, e in enumerate(autostart_entries()):
            mb = memory_of(e) if e["on"] else None
            total += mb or 0
            box = QCheckBox(e["name"] + (f"   ·  {mb} MB" if mb else ""))
            box.setChecked(e["on"])
            box.setToolTip(e["desc"])
            box.toggled.connect(lambda on, e=e: (set_autostart(e, on), fill()))
            page.bg_grid.addWidget(cell(box, e["desc"]), i // 2, i % 2)
        page.bg_total.setText(T("Together they use about") + f" {total} MB " + T("of memory right now.") if total else "")
        # services
        clear(page.svc_grid)
        n = 0
        for sid, name, desc, units in SERVICES:
            states = [sh(["systemctl", "is-enabled", u]).strip() for u in units]
            if all(s in ("", "not-found") for s in states):
                continue
            on = any(s in ("enabled", "static", "alias", "enabled-runtime") for s in states)
            box = QCheckBox(T(name))
            box.setChecked(on)
            box.setStyleSheet("font-weight: 600;")
            box.toggled.connect(lambda on, sid=sid, box=box: toggle_service(page, sid, on, box))
            page.svc_grid.addWidget(cell(box, T(desc)), n // 2, n % 2)
            n += 1
        # extra apps
        clear(page.ex_grid)
        page.extra_boxes = []
        page.removed = []
        m = 0
        for eid, name, desc, pkgs in EXTRAS:
            if not installed(pkgs[0]):
                if os.path.exists(os.path.join(HOME, ".config/devium/removed-extras")) and \
                        eid in open(os.path.join(HOME, ".config/devium/removed-extras")).read().split():
                    page.removed.append((eid, name, pkgs))
                continue
            size = sh(["pacman", "-Qi", pkgs[0]])
            msize = re.search(r"Installed Size\s*:\s*([\d.]+)\s*(\w+)", size)
            sz = f"   ·  {msize.group(1)} {msize.group(2)}" if msize else ""
            box = QCheckBox(f"{name}{sz}")
            box.setStyleSheet("font-weight: 600;")
            page.extra_boxes.append((eid, name, pkgs, box))
            page.ex_grid.addWidget(cell(box, T(desc)), m // 2, m % 2)
            m += 1
        page.ex_note.setText((T("Removed earlier:") + " " + ", ".join(n for _e, n, _p in page.removed))
                             if page.removed else "")

    page.fill = fill
    page.on_show = fill
    return page


def toggle_service(page, sid, on, box):
    r = subprocess.run(["pkexec", "/usr/lib/devium/devium-helper", "service", sid, "on" if on else "off"])
    if r.returncode != 0:
        box.blockSignals(True)
        box.setChecked(not on)
        box.blockSignals(False)


def remove_extras(page):
    pick = [(eid, name, pkgs) for eid, name, pkgs, box in page.extra_boxes if box.isChecked()]
    if not pick:
        return
    names = ", ".join(n for _e, n, _p in pick)
    warn = ("\n\nWithout Timeshift, updates can't be undone." if any(e == "timeshift" for e, _n, _p in pick) else "")
    if QMessageBox.question(page, T("Remove"), f"Remove {names}?{warn}") != QMessageBox.StandardButton.Yes:
        return
    ids = [e for e, _n, _p in pick]

    def done(code):
        if code == 0:
            path = os.path.join(HOME, ".config/devium/removed-extras")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            old = open(path).read().split() if os.path.exists(path) else []
            open(path, "w").write("\n".join(sorted(set(old) | set(ids))) + "\n")
        page.fill()
    X.root(page, T("Remove"), "remove-extra", *ids, done=done)


def add_back(page):
    if not page.removed:
        QMessageBox.information(page, T("Add back"), T("Nothing has been removed here."))
        return
    ids = [e for e, _n, _p in page.removed]

    def done(code):
        path = os.path.join(HOME, ".config/devium/removed-extras")
        if code == 0 and os.path.exists(path):
            os.remove(path)
        page.fill()
    X.root(page, T("Add back"), "add-extra", *ids, done=done)
