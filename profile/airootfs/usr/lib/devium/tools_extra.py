"""Devium Tools pages added in beta15: Look (accent colour, reset desktop), Phone link,
Backup and move, Drivers, Health check, and the developer extras (ports, project starters, tool packs).

Imported by devium-tools, which passes in its small helpers (Page, card, row, button, ...)."""
import datetime
import glob
import json
import os
import re
import shutil
import subprocess

from PyQt6.QtCore import QProcess, Qt, QTimer
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (QCheckBox, QColorDialog, QComboBox, QDialog, QFileDialog, QFormLayout, QGridLayout,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMessageBox, QPushButton, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout, QWidget)

import devium_ui as ui
from devium_i18n import T

HOME = os.path.expanduser("~")
CONFIG = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config")), "devium")
KDE = shutil.which("plasmashell") is not None
HYPR = bool(os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")) or shutil.which("Hyprland") is not None and not KDE
XFCE = shutil.which("xfce4-session") is not None and not KDE

# set by devium-tools
Page = card = row = button = label = root = run = read = human = RunDialog = in_terminal = None


def setup(**helpers):
    globals().update(helpers)


# ============================================================================ Look: accent colour + reset
ACCENTS = [   # name, main colour, second colour (for the soft gradient)
    ("Devium blue", "#8fb4d8", "#b4b8e0"),
    ("Lavender", "#b4a7e0", "#d4b8e8"),
    ("Mint", "#8fd4b8", "#a8dcd8"),
    ("Sky", "#80c8e8", "#a8c8f0"),
    ("Peach", "#e8b08f", "#e8c8a8"),
    ("Rose", "#e0a0b4", "#d8b0e0"),
    ("Lemon", "#e0cc80", "#e0d8a8"),
    ("Graphite", "#a8b0bc", "#c4ccd6"),
]


def second_colour(hexcol):
    """A softer partner colour for a custom accent (a little lighter, hue nudged towards lavender)."""
    c = QColor(hexcol)
    h, s, v, _a = c.getHsv()
    h = (h + 25) % 360 if h >= 0 else 0
    return QColor.fromHsv(h, max(0, int(s * 0.8)), min(255, int(v * 1.05) + 10)).name()


def current_accent():
    try:
        a, b = open(os.path.join(CONFIG, "accent")).read().split()[:2]
        return a, b
    except (OSError, ValueError):
        return ui.ACCENT, ui.ACCENT2


def apply_accent(a, b, login_screen=True, parent=None):
    """Use colour a (and partner b) everywhere: KDE, Hyprland borders, the Devium apps, the login screen."""
    old_a, old_b = current_accent()
    os.makedirs(CONFIG, exist_ok=True)
    with open(os.path.join(CONFIG, "accent"), "w") as f:
        f.write(f"{a} {b}\n")
    if KDE and shutil.which("plasma-apply-colorscheme"):
        subprocess.run(["plasma-apply-colorscheme", "--accent-color", a],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    conf = os.path.join(HOME, ".config/hypr/hyprland.conf")
    if os.path.exists(conf):
        text = open(conf).read()
        text = re.sub(r"(col\.active_border\s*=\s*).*", rf"\1rgb({a[1:]}) rgb({b[1:]}) 45deg", text)
        open(conf, "w").write(text)
    # Hyprland edition: the bar, the app launcher and notifications use the accent too
    for rel in (".config/waybar/style.css", ".config/fuzzel/fuzzel.ini", ".config/mako/config"):
        path = os.path.join(HOME, rel)
        if not os.path.exists(path):
            continue
        text = open(path).read()
        new = re.sub(re.escape(old_a[1:]), a[1:], text, flags=re.I)
        new = re.sub(re.escape(old_b[1:]), b[1:], new, flags=re.I)
        if new != text:
            open(path, "w").write(new)
    if HYPR:
        subprocess.Popen(["bash", "-c", "hyprctl reload; pkill -SIGUSR2 waybar; makoctl reload"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    if XFCE:
        subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Gtk/ColorPalette", "-n", "-t", "string",
                        "-s", f"selected_bg_color:{a}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if login_screen and os.path.isdir("/usr/share/sddm/themes/devium"):
        subprocess.run(["pkexec", "/usr/lib/devium/devium-helper", "sddm-accent", a, b],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def swatch(a, b, size=38):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    from PyQt6.QtGui import QLinearGradient, QPainter, QBrush
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    g = QLinearGradient(0, 0, size, size)
    g.setColorAt(0, QColor(a))
    g.setColorAt(1, QColor(b))
    p.setBrush(QBrush(g))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(2, 2, size - 4, size - 4)
    p.end()
    return QIcon(pix)


def reset_desktop(parent):
    """Put the dock, panels and look back to Devium's defaults (a copy of the old settings is kept)."""
    if QMessageBox.question(parent, T("Reset desktop"),
                            "Put the dock, panels, theme and shortcuts back to how Devium starts?\n\n"
                            "Your files and apps are not touched, and a copy of your current desktop settings "
                            "is saved in ~/.config/devium/reset-backup-…") != QMessageBox.StandardButton.Yes:
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = os.path.join(CONFIG, f"reset-backup-{stamp}")
    os.makedirs(bak, exist_ok=True)
    cfg = os.path.join(HOME, ".config")
    files = []
    if KDE:
        files = ["plasma-org.kde.plasma.desktop-appletsrc", "plasmashellrc", "kdeglobals", "kwinrc",
                 "plasmarc", "kglobalshortcutsrc", "devium/dock.js", "devium/dock-launchers", "devium/accent"]
    elif HYPR:
        files = ["hypr", "waybar", "fuzzel", "mako", "kitty", "devium/accent"]
    elif XFCE:
        files = ["xfce4", "devium/accent"]
    for f in files:
        src = os.path.join(cfg, f)
        if os.path.exists(src):
            dst = os.path.join(bak, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
    if KDE:
        skel = "/etc/skel/.config/kglobalshortcutsrc"
        if os.path.exists(skel):
            shutil.copy(skel, os.path.join(cfg, "kglobalshortcutsrc"))
        script = ("plasma-apply-lookandfeel -a org.devium.desktop --resetLayout; "
                  "systemctl --user restart plasma-plasmashell.service || "
                  "(kquitapp6 plasmashell; kstart plasmashell)")
        subprocess.Popen(["bash", "-c", "sleep 1; " + script], start_new_session=True)
    elif HYPR:
        for f in ("hypr", "waybar", "fuzzel", "mako", "kitty"):
            s = os.path.join("/etc/skel/.config", f)
            if os.path.exists(s):
                shutil.copytree(s, os.path.join(cfg, f), dirs_exist_ok=True)
        subprocess.Popen(["bash", "-c", "hyprctl reload; pkill waybar; setsid waybar >/dev/null 2>&1 &"],
                         start_new_session=True)
    elif XFCE:
        QMessageBox.information(parent, T("Reset desktop"), "Done. Log out and back in to see the default desktop.")
    if os.path.exists("/etc/sddm.conf.d") and os.path.exists("/usr/share/sddm/themes/devium/theme.conf.user"):
        subprocess.run(["pkexec", "/usr/lib/devium/devium-helper", "sddm-accent", ui.ACCENT, ui.ACCENT2],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


DEVIUM_WIDGETS = [   # plugin id, name, what it shows
    ("org.devium.clock", "Clock", "Big clock, date and a greeting"),
    ("org.devium.weather", "Weather", "Now and the next 5 days"),
    ("org.devium.sea", "Sea conditions", "Waves, swell, water temperature, wind and tide"),
    ("org.devium.system", "System", "CPU, memory and disk rings, temperature, battery"),
    ("org.devium.focus", "Focus timer", "25 minutes of focus, then a 5 minute break"),
    ("org.devium.projects", "Git projects", "Your repos: branch, changes, ahead/behind"),
    ("org.devium.servers", "Dev servers", "What's running on which port"),
    ("org.devium.links", "Devium shortcuts", "Spotlight, Tools, Configure, Updates…"),
    ("org.devium.photo", "Photo", "A picture or a slideshow from your Pictures folder"),
]


def add_widget(plugin):
    """Put a widget on the desktop (Plasma finds a free spot for it)."""
    js = f"var d = desktops(); if (d.length) {{ d[0].addWidget('{plugin}'); }}"
    for q in ("qdbus6", "qdbus"):
        if shutil.which(q):
            return subprocess.run([q, "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", js],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    return False


def widgets_card(page):
    grid = QGridLayout()
    grid.setSpacing(6)
    for i, (pid, name, desc) in enumerate(DEVIUM_WIDGETS):
        b = QPushButton(f"+  {T(name)}")
        b.setToolTip(T(desc))
        b.setMinimumHeight(36)
        b.clicked.connect(lambda _c=False, pid=pid, name=name:
                          page.widget_note.setText(T("Added") + f" {T(name)}. " + T("Drag it where you like.")
                                                   if add_widget(pid) else T("Couldn't add it. Is Plasma running?")))
        grid.addWidget(b, i // 4, i % 4)
    w = QWidget()
    w.setLayout(grid)
    page.widget_note = label("", "subtitle")
    return card(label(T("Devium widgets"), "h2"),
                label("Widgets for your desktop in the Devium style. Click one to add it, then drag it where you "
                      "want. Right-click a widget to change its settings (like the place for weather and sea) or "
                      "remove it. You also find them in right-click desktop > Add or Manage Widgets.", "subtitle"),
                w, page.widget_note)


DESK_CFG = os.path.join(CONFIG, "desk-widgets.json")


def desk_widgets_card(page):
    """Xfce and Hyprland: the same widgets, drawn by devium-desk-widgets."""
    try:
        cfg = json.load(open(DESK_CFG))
    except (OSError, ValueError):
        cfg = {"widgets": []}
    on = {w.get("id") for w in cfg.get("widgets", [])}
    grid = QGridLayout()
    boxes = []
    for i, (pid, name, desc) in enumerate(DEVIUM_WIDGETS):
        wid = pid.split(".")[-1]
        b = QCheckBox(T(name))
        b.setToolTip(T(desc))
        b.setChecked(wid in on)
        boxes.append((wid, b))
        grid.addWidget(b, i // 4, i % 4)
    holder = QWidget()
    holder.setLayout(grid)
    place = QLineEdit(cfg.get("place", ""))
    place.setPlaceholderText(T("Place for weather and sea (empty = from your IP address)"))
    imperial = QCheckBox(T("Use °F, mph and feet"))
    imperial.setChecked(bool(cfg.get("imperial")))
    note = label("", "subtitle")

    def apply():
        keep = {w.get("id"): w for w in cfg.get("widgets", [])}      # keep where you dragged them
        cfg["widgets"] = [keep.get(wid, {"id": wid}) for wid, b in boxes if b.isChecked()]
        cfg["place"] = place.text().strip()
        cfg["imperial"] = imperial.isChecked()
        os.makedirs(CONFIG, exist_ok=True)
        with open(DESK_CFG, "w") as f:
            json.dump(cfg, f, indent=1)
        if HYPR and not shutil.which("qs"):
            root(page, T("Devium widgets"), "archpill-deps")      # installs Quickshell
        subprocess.Popen(["devium-desk-widgets"], start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        note.setText(T("Done. Drag a widget to move it.") if cfg["widgets"] else T("Widgets turned off."))

    return card(label(T("Devium widgets"), "h2"),
                label("Widgets on your desktop in the Devium style, behind your windows. Tick the ones you want and "
                      "press Apply, then drag them where you like.", "subtitle"),
                holder, place, imperial, row(button(T("Apply"), apply, True, "dialog-ok")), note)


def make_look_page(win):
    page = Page(T("Look"), T("Pick your accent colour, or put the desktop back to how Devium starts."))
    a, b = current_accent()
    page.current = label("", "subtitle")

    def show_current(a, b):
        page.current.setText(T("Current accent:") + f" <b style='color:{a}'>{a}</b>")
        page.current.setTextFormat(Qt.TextFormat.RichText)

    show_current(a, b)
    login = QCheckBox(T("Use it on the login screen too (asks for your password)"))
    login.setChecked(True)
    login.setVisible(os.path.isdir("/usr/share/sddm/themes/devium"))
    grid = QGridLayout()
    grid.setSpacing(8)

    def pick(ca, cb):
        apply_accent(ca, cb, login.isChecked(), page)
        show_current(ca, cb)
        page.done_note.setText(T("Done! Devium apps use the new colour next time you open them."))

    for i, (name, ca, cb) in enumerate(ACCENTS):
        btn = QPushButton(T(name))
        btn.setIcon(swatch(ca, cb))
        btn.setIconSize(btn.iconSize() * 2)
        btn.setMinimumHeight(48)
        btn.clicked.connect(lambda _c=False, ca=ca, cb=cb: pick(ca, cb))
        grid.addWidget(btn, i // 4, i % 4)

    def custom():
        c = QColorDialog.getColor(QColor(current_accent()[0]), page, T("Pick any colour"))
        if c.isValid():
            pick(c.name(), second_colour(c.name()))

    w = QWidget()
    w.setLayout(grid)
    page.done_note = label("", "subtitle")
    what = ("the theme highlight, the dock, window borders" if KDE else
            "window borders, the bar" if HYPR else "highlights")
    page.add(card(label(T("Accent colour"), "h2"),
                  label(f"Changes {what}, the Devium apps and the login screen to match.", "subtitle"),
                  w, row(button(T("Pick any colour…"), custom, icon="color-picker"), login), page.current,
                  page.done_note))
    engines = [("duckduckgo", "DuckDuckGo"), ("brave", "Brave Search"), ("google", "Google"),
               ("startpage", "Startpage"), ("bing", "Bing"), ("ecosia", "Ecosia")]
    eng_file = os.path.join(CONFIG, "search-engine")
    eng_box = QComboBox()
    for key, name in engines:
        eng_box.addItem(name, key)
    try:
        cur = open(eng_file).read().strip()
    except OSError:
        cur = "duckduckgo"
    eng_box.setCurrentIndex(max(0, [k for k, _n in engines].index(cur) if cur in [k for k, _n in engines] else 0))

    def set_engine(_i):
        os.makedirs(CONFIG, exist_ok=True)
        with open(eng_file, "w") as f:
            f.write(eng_box.currentData() + "\n")
    eng_box.currentIndexChanged.connect(set_engine)
    page.add(card(label(T("Web search in Spotlight"), "h2"),
                  label("Type anything in Spotlight (Meta+Space) and pick \"Search the web\". Shortcuts: yt (YouTube), "
                        "g (Google), wiki, gh (GitHub), aur, arch (Arch Wiki), so (Stack Overflow), maps, r (Reddit), "
                        "then your words. Typing an address like github.com opens it.", "subtitle"),
                  row(QLabel(T("Search with:")), eng_box)))
    page.add(card(label(T("Customise"), "h2"),
                  label("Dozens of optional tweaks: macOS-style window buttons, see-through windows, blur, wobbly "
                        "windows, magic lamp, hot corners, clock with seconds, bigger cursor, night light and more.",
                        "subtitle"),
                  row(button(T("Open Customise"), lambda: ui.launch("devium-setup-wizard", "--customise"), True,
                             "preferences-desktop-theme"))))
    page.add(card(label(T("Reset desktop"), "h2"),
                  label("Dock in the wrong place, panels gone, or the theme looks broken? Put the desktop back "
                        "to Devium's defaults without reinstalling. Your files and apps stay.", "subtitle"),
                  row(button(T("Reset desktop"), lambda: reset_desktop(page), icon="edit-undo"))))
    if KDE and os.path.isdir("/usr/share/plasma/plasmoids/org.devium.home"):
        home_box = QCheckBox(T("Home screen pages (like iPhone)"))
        try:
            home_box.setChecked(bool(json.load(open(os.path.join(CONFIG, "tweaks.json"))).get("home-pages")))
        except (OSError, ValueError):
            home_box.setChecked(False)

        def toggle_home(on):
            subprocess.Popen(["python3", "/usr/lib/devium/look_tweaks.py", "set", f"home-pages={'on' if on else 'off'}"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        home_box.toggled.connect(toggle_home)
        page.add(card(label(T("Home screen pages"), "h2"),
                      label("Optional: turn your desktop into pages of apps and widgets that you swipe between, like an "
                            "iPhone. Swipe with the touchpad or mouse, or click the dots. Press and hold to edit.",
                            "subtitle"), home_box))
    if KDE and os.path.isdir("/usr/share/plasma/plasmoids/org.devium.clock"):
        page.add(widgets_card(page))
    elif (XFCE or HYPR) and shutil.which("devium-desk-widgets"):
        page.add(desk_widgets_card(page))
    if KDE:
        page.add(card(label(T("More looks"), "h2"),
                      label("Light or dark theme, icons, wallpaper and fonts are in System Settings.", "subtitle"),
                      row(button(T("Colours and theme"), lambda: ui.launch("systemsettings", "kcm_colors"),
                                 icon="preferences-desktop-color"),
                          button(T("Wallpaper"), lambda: ui.launch("systemsettings", "kcm_wallpaper"),
                                 icon="preferences-desktop-wallpaper"))))
    page.finish()
    return page


# ============================================================================ Phone link (KDE Connect)
KDECONNECT_ANDROID = "https://play.google.com/store/apps/details?id=org.kde.kdeconnect_tp"
KDECONNECT_FDROID = "https://f-droid.org/packages/org.kde.kdeconnect_tp/"
KDECONNECT_IOS = "https://apps.apple.com/app/kde-connect/id1580245991"


def make_phone_page(win):
    page = Page(T("Phone link"),
                T("Connect your phone to Devium: send files both ways, see your phone's notifications here, "
                  "share the clipboard, and use your phone as a remote or touchpad."))
    page.state = label("", rich=True)
    page.add(page.state)

    qr_row = QHBoxLayout()
    for title, url in (("Android", KDECONNECT_ANDROID), ("iPhone", KDECONNECT_IOS)):
        col = QVBoxLayout()
        pic = QLabel()
        pix = ui.qr_pixmap(url, 170)
        if pix:
            pic.setPixmap(pix)
        else:
            pic.setText(url)
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(pic)
        cap = QLabel(f"<b>{title}</b>")
        cap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(cap)
        qr_row.addLayout(col)
    qr_row.addStretch(1)

    def install():
        root(page, T("Phone link"), "phone", done=lambda c: refresh())

    def open_app():
        ui.launch("kdeconnect-app") or ui.launch("kdeconnect-settings")

    page.install_btn = button(T("Set up Phone link"), install, True, "smartphone")
    page.open_btn = button(T("Open KDE Connect"), open_app, icon="kdeconnect")
    steps = label("<b>1.</b> Press <b>Set up Phone link</b> (installs KDE Connect, about 30 MB).<br>"
                  "<b>2.</b> Scan a code below with your phone and install <b>KDE Connect</b>.<br>"
                  "<b>3.</b> Make sure the phone is on the <b>same Wi-Fi</b> as this computer.<br>"
                  f"<b>4.</b> Open KDE Connect on the phone, tap <b>{os.uname().nodename}</b>, then "
                  "<b>Pair</b>, and accept here.", rich=True)
    page.add(card(label(T("Connect your phone"), "h2"), steps, qr_row,
                  label(f"Android without Google Play: <a href='{KDECONNECT_FDROID}'>F-Droid</a>", rich=True),
                  row(page.install_btn, page.open_btn)))
    page.add(card(label(T("What you can do"), "h2"),
                  label("• Send a file: right-click it > Send to phone (or share > KDE Connect on the phone)<br>"
                        "• Phone notifications and texts pop up on Devium<br>"
                        "• Copy on one, paste on the other<br>"
                        "• Pause music when a call comes in<br>"
                        "• Use the phone as a touchpad, keyboard or slideshow remote<br>"
                        "• Ring your phone when you can't find it", rich=True)))

    def refresh():
        have = shutil.which("kdeconnectd") or os.path.exists("/usr/lib/kdeconnectd")
        page.install_btn.setVisible(not have)
        page.open_btn.setVisible(bool(have))
        devs = run(["kdeconnect-cli", "-a", "--name-only"]).strip().splitlines() if shutil.which("kdeconnect-cli") else []
        if devs:
            page.state.setText("📱 <b>" + T("Connected:") + "</b> " + ", ".join(devs))
        elif have:
            page.state.setText(T("KDE Connect is ready. Pair your phone with the steps below."))
        else:
            page.state.setText(T("Phone link isn't set up yet."))

    page.on_show = refresh
    page.finish()
    return page


# ============================================================================ Backup and move
def make_backup_page(win):
    page = Page(T("Backup and move"),
                T("Back up your files and settings to a USB drive, put them back after a reinstall, or move "
                  "your whole Devium setup to a new PC."))
    page.drives = QComboBox()
    page.drives.setMinimumWidth(320)
    page.last = label("", "subtitle")

    def find():
        page.drives.clear()
        for line in run(["devium-backup", "drives"], timeout=20).splitlines():
            path, lab, free, size = line.split("\t")
            page.drives.addItem(f"{lab}  ({human(int(free))} free of {human(int(size))})  {path}", path)
        if not page.drives.count():
            page.drives.addItem(T("No USB drive found. Plug one in and press Look again."), None)
        update_last()

    def update_last():
        p = page.drives.currentData()
        stamp = os.path.join(p, "DeviumBackup", "devium-move.json") if p else ""
        if stamp and os.path.exists(stamp):
            when = datetime.datetime.fromtimestamp(os.path.getmtime(stamp)).strftime("%d %B %Y, %H:%M")
            page.last.setText(T("Last backup on this drive:") + f" {when}")
        else:
            page.last.setText(T("No backup on this drive yet."))

    page.drives.currentIndexChanged.connect(lambda _i: update_last())

    def need_home_size():
        try:
            out = run(["du", "-sb", "--exclude=.cache", HOME], timeout=60).split()
            return int(out[0])
        except (IndexError, ValueError):
            return 0

    def do_backup():
        p = page.drives.currentData()
        if not p:
            return
        need = need_home_size()
        free = shutil.disk_usage(p).free
        if need and need > free and not os.path.exists(os.path.join(p, "DeviumBackup")):
            QMessageBox.warning(page, T("Backup"), f"Your files need about {human(need)}, but the drive only "
                                                   f"has {human(free)} free.")
            return
        RunDialog(page, T("Backup"), "devium-backup", ["backup", p], done=lambda c: update_last()).exec()

    def do_restore():
        p = page.drives.currentData()
        if not p:
            p = QFileDialog.getExistingDirectory(page, T("Find your DeviumBackup folder"), "/run/media")
            if not p:
                return
        if QMessageBox.question(page, T("Restore"),
                                "Copy your files and settings back from this backup, and reinstall your apps?\n\n"
                                "Nothing on this computer is deleted; files with the same name are replaced by "
                                "the backup's copy.") != QMessageBox.StandardButton.Yes:
            return
        RunDialog(page, T("Restore"), "devium-backup", ["restore", p]).exec()

    def do_export():
        name = f"devium-{os.uname().nodename}-{datetime.date.today():%Y-%m-%d}.devium"
        start = page.drives.currentData() or os.path.join(HOME, "Desktop")
        path, _f = QFileDialog.getSaveFileName(page, T("Save your Devium setup"), os.path.join(start, name),
                                               "Devium setup (*.devium)")
        if path:
            RunDialog(page, T("Move to a new PC"), "devium-backup", ["export", path]).exec()

    def do_import():
        path, _f = QFileDialog.getOpenFileName(page, T("Open a Devium setup file"),
                                               page.drives.currentData() or HOME, "Devium setup (*.devium *.tar.gz)")
        if path:
            RunDialog(page, T("Move to a new PC"), "devium-backup", ["import", path]).exec()

    page.add(card(label(T("Back up to a USB drive"), "h2"),
                  label("Copies your home folder (documents, pictures, projects, settings) and a list of your apps "
                        "to a DeviumBackup folder on the drive. The next backup only copies what changed, so it's "
                        "quick. Caches and the bin are skipped.", "subtitle"),
                  row(QLabel(T("Drive:")), page.drives, button(T("Look again"), find, icon="view-refresh"),
                      stretch=False),
                  page.last,
                  row(button(T("Back up now"), do_backup, True, "document-save"),
                      button(T("Restore from backup"), do_restore, icon="document-revert"))))
    page.add(card(label(T("Move to a new PC"), "h2"),
                  label("Saves your apps, Flatpaks, VS Code extensions, Devium Configure choices, dock, accent "
                        "colour, terminal and shell settings to one small .devium file. Open it on the new PC "
                        "(after installing Devium) and everything is set up the same. Your personal files aren't "
                        "in it; use a backup for those.", "subtitle"),
                  row(button(T("Save my setup to a file"), do_export, True, "document-export"),
                      button(T("Import a setup file"), do_import, icon="document-import"))))
    page.add(card(label(T("Restore points"), "h2"),
                  label("For the system itself (not your files), Timeshift takes restore points before every "
                        "update, and Updates has an undo button.", "subtitle"),
                  row(button("Timeshift", lambda: ui.launch("timeshift-launcher") or ui.launch("timeshift-gtk"),
                             icon="timeshift"))))
    page.on_show = lambda: (page.drives.count() == 0) and find()
    page.finish()
    return page


# ============================================================================ Drivers
def detect_drivers():
    """What this computer has that may want a driver: [(id, title, why, installed?)]"""
    out = []
    pci_raw = run(["lspci", "-nn"])
    pci = pci_raw.lower()
    usb = run(["lsusb"]).lower()

    def have(*pkgs):
        return all(installed(p) for p in pkgs)

    gpu_lines = [l for l in pci.splitlines() if re.search(r"vga|3d controller|display controller", l)]
    if any("[10de:" in l for l in gpu_lines):
        name = next((l.split(": ", 1)[-1] for l in pci_raw.splitlines() if "[10de:" in l.lower()
                     and re.search(r"vga|3d|display", l, re.I)), "NVIDIA graphics")
        name = re.sub(r"\s*\[[0-9a-f]{4}:[0-9a-f]{4}\].*", "", name)
        old = re.search(r"geforce (gtx )?(9\d\d|10\d\d|7\d\d)\b|quadro [kmp]\d", name.lower())
        why = (f"{name.strip()}\nThe NVIDIA driver gives you full speed, games and external screens."
               + ("\nThis card is older (before GTX 16xx): in a terminal run  yay -S nvidia-580xx-dkms  instead."
                  if old else ""))
        out.append(("nvidia", "NVIDIA graphics driver", why, have("nvidia-utils"), not old))
    if any("[8086:" in l for l in gpu_lines):
        out.append(("intel-video", "Intel graphics: video and Vulkan",
                    "Smooth video playback (hardware decoding) and Vulkan for games.",
                    have("intel-media-driver", "vulkan-intel"), True))
    if any("[1002:" in l for l in gpu_lines):
        out.append(("amd-video", "AMD graphics: Vulkan", "Vulkan for games and apps (Mesa is already installed).",
                    have("vulkan-radeon"), True))
    if re.search(r"network controller.*\[14e4:", pci):
        out.append(("broadcom", "Broadcom Wi-Fi driver",
                    "Many Broadcom Wi-Fi cards (common in older Dell, HP and MacBooks) need this to work.",
                    have("broadcom-wl-dkms") or have("broadcom-wl"), True))
    if re.search(r"multimedia audio controller.*\[8086:|audio device.*\[8086:", pci):
        out.append(("sound", "Laptop sound firmware",
                    "Newer Intel laptops need this for speakers and the built-in microphone.",
                    have("sof-firmware", "alsa-ucm-conf"), True))
    if re.search(r"fingerprint|synaptics.*(00bd|00c[0-9])|goodix|elan.*(0c|fp)|validity|06cb:", usb):
        out.append(("fingerprint", "Fingerprint reader",
                    "Log in and use sudo with your finger. Set it up afterwards in System Settings > Users.",
                    have("fprintd"), True))
    virt = run(["systemd-detect-virt"]).strip()
    return out, virt


def make_drivers_page(win):
    page = Page(T("Drivers"), T("Devium looks at your hardware and finds the drivers it needs. Most hardware works "
                                "straight away; this page is for the few things that don't."))
    page.box = QVBoxLayout()
    holder = QWidget()
    holder.setLayout(page.box)
    page.add(holder)
    page.install_btn = button(T("Install selected drivers"), lambda: install(), True, "run-install")
    page.add(row(page.install_btn, button(T("Look again"), lambda: refresh(), icon="view-refresh")))
    page.hw = QTreeWidget()
    page.hw.setHeaderLabels([T("Your hardware")])
    page.hw.setRootIsDecorated(False)
    page.hw.setMinimumHeight(180)
    page.add(card(label(T("What's in this computer"), "h2"), page.hw))
    page.checks = []

    def clear():
        while page.box.count():
            w = page.box.takeAt(0).widget()
            if w:
                w.deleteLater()
        page.checks = []

    def refresh():
        clear()
        found, virt = detect_drivers()
        if virt and virt != "none":
            page.box.addWidget(card(label(f"✓ Running in a virtual machine ({virt}). Its guest tools are already "
                                          "installed.", "subtitle")))
        todo = [f for f in found if not f[3]]
        for did, title, why, installed, ok in found:
            box = QCheckBox(T(title) + ("   ✓ " + T("installed") if installed else ""))
            box.setChecked(not installed and ok)
            box.setEnabled(not installed and ok)
            page.checks.append((did, box))
            page.box.addWidget(card(box, label(why, "subtitle")))
        if not found or not todo:
            page.box.addWidget(card(label("✓ " + T("Everything has its driver. Nothing to install."), "h2")))
        page.install_btn.setEnabled(bool(todo))
        page.hw.clear()
        for line in run(["lspci"]).splitlines():
            if re.search(r"VGA|3D|Network|Ethernet|Audio|Wireless", line, re.I):
                page.hw.addTopLevelItem(QTreeWidgetItem([line.split(" ", 1)[-1]]))
        for line in run(["lsusb"]).splitlines():
            n = line.split(" ", 6)[-1]
            if not re.search(r"root hub|Linux Foundation", n):
                page.hw.addTopLevelItem(QTreeWidgetItem(["USB: " + n]))

    def install():
        ids = [d for d, b in page.checks if b.isChecked() and b.isEnabled()]
        if ids:
            root(page, T("Drivers"), "drivers", *ids, done=lambda c: refresh())

    page.on_show = lambda: page.checks or refresh()
    page.finish()
    return page


# ============================================================================ Health check
HEALTH = "/var/lib/devium/health.json"


def temps():
    """Temperatures from the kernel sensors (no password needed): [(name, °C)]"""
    out = []
    for hw in sorted(glob.glob("/sys/class/hwmon/hwmon*")):
        name = read(os.path.join(hw, "name"), "sensor")
        for t in sorted(glob.glob(os.path.join(hw, "temp*_input"))):
            try:
                c = int(read(t)) / 1000
            except ValueError:
                continue
            if c <= 0 or c > 130:
                continue
            lab = read(t.replace("_input", "_label"))
            nice = {"coretemp": "CPU", "k10temp": "CPU", "zenpower": "CPU", "amdgpu": "Graphics (AMD)",
                    "nouveau": "Graphics (NVIDIA)", "nvme": "SSD", "acpitz": "Motherboard", "iwlwifi_1": "Wi-Fi",
                    "drivetemp": "Disk", "thinkpad": "Laptop"}.get(name, name)
            out.append((f"{nice} {lab}".strip() if lab and lab not in nice else nice, c))
    seen, uniq = set(), []
    for n, c in out:   # one line per sensor name, the hottest reading
        if n in seen:
            continue
        seen.add(n)
        uniq.append((n, max(x[1] for x in out if x[0] == n)))
    return uniq[:10]


def make_health_page(win):
    page = Page(T("Health check"), T("Disk health, temperatures and battery wear in one place. Devium checks your "
                                     "disks every day and warns you before one fails."))
    page.disks = label("", rich=True)
    page.temps = label("", rich=True)
    page.battery = label("", rich=True)
    page.mem = label("", rich=True)
    page.add(card(label(T("Disks"), "h2"), page.disks,
                  row(button(T("Check disks now"), lambda: check(), True, "drive-harddisk"))))
    page.add(card(label(T("Temperatures"), "h2"), page.temps))
    page.add(card(label(T("Battery"), "h2"), page.battery))
    page.add(card(label(T("Storage and memory"), "h2"), page.mem,
                  row(button(T("Free up space"), lambda: win.go("speed"), icon="edit-clear"),
                      button(T("See what's big"), lambda: ui.launch("filelight") or ui.launch("baobab")
                             or ui.launch("qdirstat"), icon="filelight"))))

    def check():
        root(page, T("Health check"), "health", done=lambda c: refresh())

    def colour(c, warm, hot):
        return "#e89ca0" if c >= hot else "#e8cd96" if c >= warm else ui.ACCENT

    def refresh():
        # disks
        try:
            data = json.load(open(HEALTH))
        except (OSError, ValueError):
            data = None
        if not data or not data.get("disks"):
            page.disks.setText("Not checked yet. Press <b>Check disks now</b> (asks for your password the first time)."
                               if not data or "error" not in data else data["error"])
        else:
            html = []
            for d in data["disks"]:
                status = ("<span style='color:#e89ca0'><b>⚠ " + T("Problem") + "</b></span>" if not d.get("ok", True)
                          else "<span style='color:%s'><b>✓ %s</b></span>" % (ui.ACCENT, T("Healthy"))
                          if d.get("supported") else T("can't be checked (USB or virtual disk)"))
                bits = [f"{d['type']} {d.get('size', '')}"]
                if d.get("life_left") is not None:
                    bits.append(f"{d['life_left']}% life left")
                if d.get("temp"):
                    bits.append(f"{d['temp']} °C")
                if d.get("hours"):
                    bits.append(f"used {d['hours']:,} hours")
                line = f"<b>{d.get('model') or d['name']}</b>: {status} &nbsp;·&nbsp; " + " · ".join(bits)
                if d.get("warnings"):
                    line += "<br>&nbsp;&nbsp;<span style='color:#e89ca0'>" + "; ".join(d["warnings"]) + \
                            " — back up your files soon (Backup and move).</span>"
                html.append(line)
            when = datetime.datetime.fromtimestamp(data.get("checked", 0)).strftime("%d %B, %H:%M")
            page.disks.setText("<br>".join(html) + f"<br><small>{T('Last checked')}: {when}</small>")
        # temperatures
        ts = temps()
        page.temps.setText("<br>".join(f"{n}: <b style='color:{colour(c, 75, 90)}'>{c:.0f} °C</b>" for n, c in ts)
                           if ts else T("No temperature sensors found (normal in a virtual machine)."))
        # battery
        bats = sorted(glob.glob("/sys/class/power_supply/BAT*"))
        if not bats:
            page.battery.setText(T("No battery (a desktop computer or a virtual machine)."))
        else:
            out = []
            for b in bats:
                full = read(f"{b}/energy_full") or read(f"{b}/charge_full")
                design = read(f"{b}/energy_full_design") or read(f"{b}/charge_full_design")
                if full and design and int(design):
                    h = int(full) * 100 / int(design)
                    tip = (" — " + T("worn out; a new battery would help") if h < 60 else
                           " — " + T("a charge limit in Battery helps it last") if h < 85 else "")
                    out.append(f"{os.path.basename(b)}: <b style='color:{colour(100 - h, 25, 40)}'>{h:.0f}%</b> "
                               f"{T('of its original capacity')}{tip}")
                cyc = read(f"{b}/cycle_count")
                if cyc and cyc != "0":
                    out.append(f"{cyc} {T('charge cycles')}")
            page.battery.setText("<br>".join(out) or T("Battery health isn't reported by this laptop."))
        # storage + memory
        du = shutil.disk_usage("/")
        pct = du.used * 100 / du.total
        mem = {l.split(":")[0]: int(l.split()[1]) * 1024 for l in read("/proc/meminfo").splitlines() if ":" in l}
        swap_used = mem.get("SwapTotal", 0) - mem.get("SwapFree", 0)
        page.mem.setText(f"{T('Disk')}: <b style='color:{colour(pct, 80, 92)}'>{human(du.free)} {T('free')}</b> "
                         f"of {human(du.total)} ({pct:.0f}% used)<br>"
                         f"{T('Memory')}: {human(mem['MemTotal'] - mem['MemAvailable'])} used of "
                         f"{human(mem['MemTotal'])}" + (f", {human(swap_used)} compressed" if swap_used > 0 else ""))

    page.on_show = refresh
    page.finish()
    return page


# ============================================================================ Developer extras
TEMPLATES = [
    ("python", "Python app (with tests)"),
    ("web", "Website (HTML, CSS, JavaScript)"),
    ("node", "Node.js app"),
    ("flask", "Python web app (Flask)"),
    ("rust", "Rust app"),
    ("go", "Go app"),
    ("cpp", "C++ app (CMake)"),
    ("c", "C app (Makefile)"),
    ("java", "Java app"),
    ("discord-bot", "Discord bot (Python)"),
]

DEVPACKS = [
    ("cli", "Modern terminal tools", "ripgrep, fd, fzf, bat, eza, zoxide, jq, yq, tree, httpie", "ripgrep"),
    ("neovim", "Neovim", "The fast terminal editor, ready for plugins", "neovim"),
    ("tmux", "tmux", "Split one terminal into many, and keep sessions running", "tmux"),
    ("lazygit", "Lazygit + delta", "A visual Git tool, and nicer diffs", "lazygit"),
    ("mise", "mise, direnv, just", "Per-project language versions, env files and task runner", "mise"),
    ("act", "act", "Run your GitHub Actions on your own computer", "act"),
    ("db", "Databases", "DBeaver and DB Browser for SQLite", "dbeaver"),
    ("api", "API testing", "httpie and websocat, for testing web APIs from the terminal", "websocat"),
    ("k8s", "Kubernetes", "kubectl, k9s and helm", "kubectl"),
    ("meld", "Meld", "Compare files and folders side by side", "meld"),
]


def installed(pkg):
    try:
        return subprocess.run(["pacman", "-Q", pkg], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL).returncode == 0
    except OSError:
        return False


class NewProjectDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(T("New project"))
        self.resize(460, 220)
        f = QFormLayout(self)
        self.name = QLineEdit()
        self.name.setPlaceholderText("my-app")
        self.kind = QComboBox()
        for k, t in TEMPLATES:
            self.kind.addItem(T(t), k)
        self.editor = QCheckBox(T("Open it in my code editor"))
        self.editor.setChecked(True)
        f.addRow(T("Name:"), self.name)
        f.addRow(T("Type:"), self.kind)
        f.addRow("", self.editor)
        f.addRow("", label(T("It goes in ~/Projects, with Git set up and a README."), "subtitle"))
        go = button(T("Create"), self.create, True)
        f.addRow("", go)

    def create(self):
        n = self.name.text().strip()
        if not re.fullmatch(r"[A-Za-z0-9._-]+", n):
            QMessageBox.warning(self, T("New project"), T("Use letters, numbers, - _ and . only."))
            return
        args = [n, "--template", self.kind.currentData()] + ([] if self.editor.isChecked() else ["--no-open"])
        RunDialog(self, T("New project"), "devium-new-project", args).exec()
        self.accept()


def ports():
    """Programs listening on a network port: [(port, address, program, pid)]"""
    out = []
    for line in run(["ss", "-ltnpH"]).splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        addr, _, port = local.rpartition(":")
        m = re.search(r'\("([^"]+)",pid=(\d+)', line)
        out.append((int(port) if port.isdigit() else 0, addr.strip("[]"),
                    m.group(1) if m else T("(system)"), m.group(2) if m else ""))
    seen, uniq = set(), []
    for p in sorted(out):
        if (p[0], p[3]) not in seen:
            seen.add((p[0], p[3]))
            uniq.append(p)
    return uniq


def add_developer_extras(page):
    """Extra cards for the Developer page: project starters, ports and servers, tool packs."""
    page.add(card(label(T("Start a new project"), "h2"),
                  label("Python, website, Node.js, Flask, Rust, Go, C, C++, Java or a Discord bot: a ready-to-run "
                        "project with Git, a README and the right .gitignore. In a terminal: "
                        "devium-new-project my-app --template rust", "subtitle"),
                  row(button(T("New project…"), lambda: NewProjectDialog(page).exec(), True, "folder-new"))))

    page.ports = QTreeWidget()
    page.ports.setHeaderLabels([T("Port"), T("Open in browser"), T("Program"), "PID"])
    page.ports.setRootIsDecorated(False)
    page.ports.setMaximumHeight(200)
    page.ports.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    page.ports.itemDoubleClicked.connect(lambda it, _c: ui.open_link(f"http://localhost:{it.text(0)}", page))

    def load_ports():
        page.ports.clear()
        for port, addr, prog, pid in ports():
            local = addr in ("127.0.0.1", "::1", "0.0.0.0", "*", "::") or addr.startswith("127.")
            it = QTreeWidgetItem([str(port), f"localhost:{port}" if local else addr, prog, pid])
            page.ports.addTopLevelItem(it)

    def stop_port():
        for it in page.ports.selectedItems():
            pid = it.text(3)
            if not pid:
                QMessageBox.information(page, T("Ports"), T("That one belongs to the system, so it's left alone."))
                continue
            if QMessageBox.question(page, T("Stop"), f"Stop {it.text(2)} (port {it.text(0)})?") == \
                    QMessageBox.StandardButton.Yes:
                subprocess.run(["kill", pid])
        QTimer.singleShot(600, load_ports)

    page.add(card(label(T("Ports and servers"), "h2"),
                  label("What's running on which port (like your dev server on localhost:3000). Double-click to "
                        "open it in the browser.", "subtitle"),
                  page.ports,
                  row(button(T("Refresh"), load_ports, icon="view-refresh"),
                      button(T("Stop selected"), stop_port, icon="process-stop"))))

    grid = QGridLayout()
    page.pack_boxes = []
    for i, (pid, name, desc, probe) in enumerate(DEVPACKS):
        b = QCheckBox(f"{T(name)}" + ("   ✓" if installed(probe) else ""))
        b.setToolTip(desc)
        b.setEnabled(not installed(probe))
        page.pack_boxes.append((pid, b))
        cell = QVBoxLayout()
        cell.addWidget(b)
        cell.addWidget(label(T(desc), "subtitle"))
        w = QWidget()
        w.setLayout(cell)
        grid.addWidget(w, i // 2, i % 2)
    gw = QWidget()
    gw.setLayout(grid)

    def install_packs():
        ids = [p for p, b in page.pack_boxes if b.isChecked() and b.isEnabled()]
        if ids:
            root(page, T("Developer tools"), "devpack", *ids)

    page.add(card(label(T("More developer tools"), "h2"), gw,
                  row(button(T("Install selected"), install_packs, True, "run-install"))))
    page.add(card(label(T("Handy shortcuts"), "h2"),
                  label("<b>Meta+Space</b> Devium Spotlight (try <code>&gt; npm run dev</code> or <code>2**10</code>)"
                        "<br><b>support learn</b> a 10-lesson terminal tutorial"
                        "<br><b>support coding</b> commands for Git, Python, Node, Docker…"
                        "<br><b>devium-new-project</b> start a project from a template", rich=True)))
    return load_ports
