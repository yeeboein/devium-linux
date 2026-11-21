"""Devium Tools > System storage: where your disk space went, in one picture.

A coloured bar for each disk (System, Apps, Games, Documents, Downloads, Pictures, Videos, Music, Code, Caches,
Other) with the size of each part, buttons to open the folders or clean up, and every drive with its free space.
Reads only; nothing is deleted here (Clean up does that). Uses the small helpers devium-tools hands to tools_extra."""
import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QRectF, QSize, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QWidget

import devium_ui as ui
import tools_extra as X
from devium_i18n import T

HOME = os.path.expanduser("~")


def xdg(name, fallback):
    try:
        out = subprocess.run(["xdg-user-dir", name], capture_output=True, text=True, timeout=3).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        out = ""
    return out if out and out != HOME else os.path.join(HOME, fallback)


def categories():
    """[(id, name, colour, [paths], open_what)] in the order shown. open_what: a folder, 'clean', 'apps' or None."""
    steam = [os.path.join(HOME, p) for p in (".local/share/Steam", ".steam", "Games", ".local/share/lutris",
                                              ".config/heroic")]
    code = [PROJECTS] + [os.path.join(HOME, d) for d in ("code", "dev", "src", "repos", "git")]
    return [
        ("system", "System", "#8fb4d8", ["/usr", "/opt", "/boot", "/etc", "/var/lib/pacman"], None),
        ("apps", "Apps", "#b4a7e0", ["/var/lib/flatpak", os.path.join(HOME, ".local/share/flatpak"),
                                     os.path.join(HOME, ".var/app")], "apps"),
        ("games", "Games", "#e0a0b4", steam, None),
        ("documents", "Documents", "#e8cd96", [xdg("DOCUMENTS", "Documents")], xdg("DOCUMENTS", "Documents")),
        ("downloads", "Downloads", "#e8b08f", [xdg("DOWNLOAD", "Downloads")], xdg("DOWNLOAD", "Downloads")),
        ("pictures", "Pictures", "#8fd4b8", [xdg("PICTURES", "Pictures")], xdg("PICTURES", "Pictures")),
        ("videos", "Videos", "#80c8e8", [xdg("VIDEOS", "Videos")], xdg("VIDEOS", "Videos")),
        ("music", "Music", "#d8b0e0", [xdg("MUSIC", "Music")], xdg("MUSIC", "Music")),
        ("code", "Code and projects", "#a8dcd8", code, PROJECTS),
        ("caches", "Caches, logs and the bin", "#9aa6b8", [os.path.join(HOME, ".cache"), "/var/cache", "/var/log",
                                                            os.path.join(HOME, ".local/share/Trash")], "clean"),
    ]


OTHER = ("other", "Other (settings, hidden files, everything else)", "#586272")
PROJECTS = os.environ.get("PROJECTS_DIR", os.path.join(HOME, "Projects"))


def mount_of(path):
    path = os.path.realpath(path)
    while not os.path.ismount(path) and path != "/":
        path = os.path.dirname(path)
    return path


def du(path):
    """Bytes in this folder on the same disk (-x), 0 if it isn't there or can't be read."""
    if not os.path.exists(path):
        return 0
    try:
        out = subprocess.run(["du", "-sxb", path], capture_output=True, text=True, timeout=240).stdout.split()
        return int(out[0]) if out else 0
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return 0


class Scan(QThread):
    """Measure every category. Emits {mount: {"total", "used", "free", "cats": {id: bytes}}}."""
    done = pyqtSignal(object)

    def run(self):
        cats = categories()
        jobs = [(cid, p) for cid, _n, _c, paths, _o in cats for p in paths]
        with ThreadPoolExecutor(max_workers=4) as pool:
            sizes = list(pool.map(lambda j: du(j[1]), jobs))
        disks = {}
        for (cid, path), size in zip(jobs, sizes):
            if not size:
                continue
            mnt = mount_of(path)
            if mnt not in disks:
                try:
                    u = shutil.disk_usage(mnt)
                except OSError:
                    continue
                disks[mnt] = {"total": u.total, "used": u.used, "free": u.free, "cats": {}}
            disks[mnt]["cats"][cid] = disks[mnt]["cats"].get(cid, 0) + size
        # the main disk and your home disk are always shown, even when empty
        for mnt in {"/", mount_of(HOME)}:
            if mnt not in disks:
                try:
                    u = shutil.disk_usage(mnt)
                    disks[mnt] = {"total": u.total, "used": u.used, "free": u.free, "cats": {}}
                except OSError:
                    pass
        self.done.emit(disks)


class StorageBar(QWidget):
    """One horizontal bar made of coloured parts; the grey end is free space."""

    def __init__(self):
        super().__init__()
        self.parts = []      # [(bytes, colour)]
        self.total = 1
        self.setMinimumHeight(30)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def sizeHint(self):
        return QSize(400, 30)

    def set_data(self, parts, total):
        self.parts, self.total = parts, max(1, total)
        self.update()

    def paintEvent(self, _ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(0, 3, self.width(), self.height() - 6)
        clip = QPainterPath()
        clip.addRoundedRect(r, 11, 11)
        p.setClipPath(clip)
        free = QColor(self.palette().mid().color())
        free.setAlphaF(0.35)
        p.fillRect(r, free)
        x = r.left()
        for size, colour in self.parts:
            w = r.width() * size / self.total
            if w < 1:
                continue
            p.fillRect(QRectF(x, r.top(), w, r.height()), QColor(colour))
            x += w
            p.fillRect(QRectF(x - 1, r.top(), 1, r.height()), QColor(0, 0, 0, 70))   # thin gap between parts


def dot(colour):
    d = QLabel()
    d.setFixedSize(14, 14)
    d.setStyleSheet(f"background: {colour}; border-radius: 7px;")
    return d


def drives():
    """Every real mounted drive: [(source, fstype, total, used, mountpoint)]."""
    try:
        out = subprocess.run(["df", "-B1", "--output=source,fstype,size,used,target", "-x", "tmpfs", "-x", "devtmpfs",
                              "-x", "squashfs", "-x", "overlay", "-x", "efivarfs"],
                             capture_output=True, text=True, timeout=10).stdout.splitlines()[1:]
    except (OSError, subprocess.TimeoutExpired):
        return []
    seen, rows = set(), []
    for line in out:
        f = line.split(None, 4)
        if len(f) < 5 or f[0] in seen or not f[0].startswith("/dev/"):
            continue
        seen.add(f[0])
        try:
            rows.append((f[0], f[1], int(f[2]), int(f[3]), f[4]))
        except ValueError:
            pass
    return rows


def make_storage_page(win):
    page = X.Page(T("System storage"), T("Where your disk space went. This only looks; nothing is deleted here. "
                                         "Use Clean up to free space."))
    page.summary = X.label("", "h2")
    page.add(page.summary)
    page.disks_box = QWidget()
    box = QGridLayout(page.disks_box)
    box.setContentsMargins(0, 0, 0, 0)
    box.setSpacing(10)
    page.add(page.disks_box)
    page.add(X.row(X.button(T("Free up space"), lambda: win.go("clean"), True, "edit-clear"),
                   X.button(T("Look again"), lambda: scan(), icon="view-refresh"),
                   X.button(T("See what's big (Filelight)"), lambda: ui.launch("filelight") or ui.launch("baobab")
                            or ui.launch("qdirstat"), icon="filelight")))
    page.drives_card = QWidget()
    page.drives_lay = QGridLayout(page.drives_card)
    page.drives_lay.setContentsMargins(0, 0, 0, 0)
    page.add(X.label(T("Drives"), "h2"))
    page.add(page.drives_card)
    page.finish()
    page.names = {c[0]: (c[1], c[2], c[4]) for c in categories()}
    page.names[OTHER[0]] = (OTHER[1], OTHER[2], None)
    page.scanner = None

    def clear(lay):
        while lay.count():
            w = lay.takeAt(0).widget()
            if w:
                w.deleteLater()

    def action(what):
        if what == "clean":
            return lambda: win.go("clean")
        if what == "apps":
            return lambda: win.go("apps")
        return lambda: ui.launch("xdg-open", what)

    def show(disks):
        clear(box)
        r = 0
        main_mnt = "/" if "/" in disks else next(iter(disks), "/")
        order = [main_mnt] + sorted(m for m in disks if m != main_mnt)
        worst_free = 1.0
        for mnt in order:
            d = disks[mnt]
            used, total = d["used"], d["total"]
            known = sum(d["cats"].values())
            d["cats"][OTHER[0]] = max(0, used - known)
            worst_free = min(worst_free, d["free"] / max(1, total))
            title = T("This computer") if mnt == "/" else f"{T('Disk')} {mnt}"
            head = X.label(f"{title}: {X.human(d['free'])} {T('free')} {T('of')} {X.human(total)}", "h2")
            bar = StorageBar()
            parts = [(d["cats"][cid], page.names[cid][1]) for cid in page.names if d["cats"].get(cid)]
            bar.set_data(parts, total)
            bar.setToolTip(f"{X.human(used)} {T('used')}")
            frame = QWidget()
            lay = QGridLayout(frame)
            lay.setContentsMargins(0, 0, 0, 6)
            lay.setHorizontalSpacing(10)
            lay.setVerticalSpacing(4)
            lay.addWidget(head, 0, 0, 1, 4)
            lay.addWidget(bar, 1, 0, 1, 4)
            row = 2
            for cid, size in sorted(d["cats"].items(), key=lambda kv: -kv[1]):
                if not size:
                    continue
                name, colour, opens = page.names[cid]
                pct = 100 * size / max(1, total)
                lay.addWidget(dot(colour), row, 0)
                lay.addWidget(QLabel(T(name)), row, 1)
                lab = QLabel(f"{X.human(size)}  ·  {pct:.0f}%")
                lab.setObjectName("subtitle")
                lay.addWidget(lab, row, 2)
                if opens and os.path.exists(opens) or opens in ("clean", "apps"):
                    b = QPushButton(T("Clean up") if opens == "clean" else T("Manage") if opens == "apps"
                                    else T("Open"))
                    b.clicked.connect(action(opens))
                    lay.addWidget(b, row, 3)
                row += 1
            lay.setColumnStretch(1, 1)
            box.addWidget(X.card(frame), r, 0)
            r += 1
        mnt = disks.get(main_mnt)
        warn = ""
        if worst_free < 0.10:
            warn = f"  ·  {T('Running low on space. Press Free up space.')}"
        page.summary.setText((f"{X.human(mnt['used'])} {T('used')} · {X.human(mnt['free'])} {T('free')}" if mnt
                              else "") + warn)

    def show_drives():
        clear(page.drives_lay)
        for i, (src, fs, total, used, target) in enumerate(drives()):
            page.drives_lay.addWidget(QLabel(f"{target}  ({src.replace('/dev/', '')}, {fs})"), i, 0)
            bar = QProgressBar()
            bar.setMaximum(1000)
            bar.setValue(int(1000 * used / max(1, total)))
            bar.setFormat("")
            bar.setFixedHeight(12)
            page.drives_lay.addWidget(bar, i, 1)
            lab = QLabel(f"{X.human(used)} / {X.human(total)}")
            lab.setObjectName("subtitle")
            page.drives_lay.addWidget(lab, i, 2)
        page.drives_lay.setColumnStretch(1, 1)

    def scan():
        page.summary.setText(T("Measuring… (this can take a minute the first time)"))
        show_drives()
        page.scanner = Scan()
        page.scanner.done.connect(show)
        page.scanner.start()

    page.scan = scan
    page.show_disks = show
    def on_show():
        if not page.loaded:
            page.loaded = True
            scan()
    page.on_show = on_show
    return page


if __name__ == "__main__":      # python3 tools_storage.py: print the numbers (no window)
    for _cid, _name, _c, _paths, _o in categories():
        print(f"{_name:28} {sum(du(p) for p in _paths) / 1e9:6.2f} GB")
    print(json.dumps(drives()[:3]))
