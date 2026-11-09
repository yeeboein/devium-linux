"""Shared look for the Devium apps (PyQt6)."""
import os
import shutil
import subprocess

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

LOGO = "/usr/share/devium/logo.png"
ACCENT = "#8fb4d8"
ACCENT2 = "#b4b8e0"

STYLE = f"""
QWidget {{ font-size: 10.5pt; }}
QLabel#title {{ font-size: 20pt; font-weight: 700; }}
QLabel#subtitle {{ color: #8a93a6; }}
QLabel#h2 {{ font-size: 13pt; font-weight: 600; margin-top: 6px; }}
QPushButton {{ padding: 7px 14px; border-radius: 8px; }}
QPushButton#primary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:1 {ACCENT2});
    color: #1b2026; font-weight: 600; border: none;
}}
QPushButton#primary:disabled {{ background: palette(mid); color: #8a93a6; }}
QPushButton#tile {{
    text-align: left; padding: 12px 14px; border-radius: 12px;
    border: 1px solid palette(mid); background: palette(base);
}}
QPushButton#tile:hover {{ border: 1px solid {ACCENT}; }}
QListWidget#nav {{ border: none; background: transparent; font-size: 11pt; }}
QListWidget#nav::item {{ padding: 9px 12px; border-radius: 8px; margin: 1px 4px; }}
QListWidget#nav::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:1 {ACCENT2});
    color: #1b2026;
}}
QProgressBar {{ border-radius: 6px; height: 12px; text-align: center; }}
QProgressBar::chunk {{
    border-radius: 6px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:1 {ACCENT2});
}}
"""


def app_icon() -> QIcon:
    return QIcon.fromTheme("devium", QIcon(LOGO))


def header(title: str, subtitle: str, size: int = 56) -> QWidget:
    w = QWidget()
    row = QHBoxLayout(w)
    row.setContentsMargins(0, 0, 0, 8)
    logo = QLabel()
    logo.setPixmap(QPixmap(LOGO).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation))
    row.addWidget(logo)
    col = QVBoxLayout()
    t = QLabel(title)
    t.setObjectName("title")
    s = QLabel(subtitle)
    s.setObjectName("subtitle")
    s.setWordWrap(True)
    col.addWidget(t)
    col.addWidget(s)
    row.addLayout(col, 1)
    return w


def is_live() -> bool:
    """True when running from the live ISO."""
    return os.path.isdir("/run/archiso")


# KDE app -> Xfce equivalent, used when the KDE app isn't installed (Xfce edition)
ALTERNATIVES = {
    "systemsettings": ["xfce4-settings-manager"],
    "konsole": ["xfce4-terminal"],
    "kate": ["mousepad"],
    "dolphin": ["thunar"],
    "spectacle": ["xfce4-screenshooter", "-r"],
    "plasma-systemmonitor": ["xfce4-taskmanager"],
    "plasma-discover": ["xdg-open", "https://flathub.org"],
}


def edition():
    try:
        for line in open("/etc/devium-release"):
            if line.startswith("DEVIUM_EDITION="):
                return line.strip().split("=", 1)[1]
    except OSError:
        pass
    return "kdeplasma"


def style_app(app):
    """Devium look for the Devium apps. KDE already gives Qt apps Devium's colours;
    elsewhere (Xfce) set the Devium palette ourselves."""
    import os
    if "KDE" not in os.environ.get("XDG_CURRENT_DESKTOP", ""):
        from PyQt6.QtGui import QColor, QPalette
        app.setStyle("Fusion")
        pal = QPalette()
        C = QPalette.ColorRole
        for role, c in [(C.Window, "#2b323b"), (C.WindowText, "#dde3ea"), (C.Base, "#242a32"),
                        (C.AlternateBase, "#29303a"), (C.Text, "#dde3ea"), (C.Button, "#343d48"),
                        (C.ButtonText, "#dde3ea"), (C.Mid, "#3b4450"), (C.Highlight, "#8fb4d8"),
                        (C.HighlightedText, "#1b2026"), (C.Link, "#8fb4d8"), (C.ToolTipBase, "#242a32"),
                        (C.ToolTipText, "#dde3ea"), (C.PlaceholderText, "#8a93a6")]:
            pal.setColor(role, QColor(c))
        app.setPalette(pal)
    app.setStyleSheet(STYLE)


def launch(*cmd: str) -> bool:
    """Start a program in the background. Returns False if it isn't installed."""
    if not shutil.which(cmd[0]) and cmd[0] in ALTERNATIVES:
        alt = ALTERNATIVES[cmd[0]]
        cmd = tuple(alt) + (cmd[1:] if cmd[0] not in ("spectacle", "plasma-discover") else ())
    if not shutil.which(cmd[0]):
        return False
    subprocess.Popen(list(cmd), start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


HELPER = ["pkexec", "/usr/lib/devium/devium-helper"]


# ---------------------------------------------------------------------------- developers
DEVELOPERS = [
    # name, role, picture, link
    ("Yeeboein", "Owner", "/usr/share/devium/credits/yeeboein.png", "https://github.com/yeeboein"),
]
CREDITS = [
    ("ArchPill", "Dynamic-Island-style pill", "https://github.com/yeeboein/archpill"),
    ("KDElite", "Lighter KDE Plasma", "https://github.com/yeeboein/kdelite"),
    ("Arch Linux", "The base system", "https://archlinux.org"),
    ("KDE Plasma", "The desktop", "https://kde.org/plasma-desktop"),
]


def round_pixmap(path, size):
    from PyQt6.QtGui import QPainter, QPainterPath
    src = QPixmap(path)
    if src.isNull():
        src = QPixmap(LOGO)
    src = src.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                     Qt.TransformationMode.SmoothTransformation)
    out = QPixmap(size, size)
    out.fill(Qt.GlobalColor.transparent)
    p = QPainter(out)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    clip = QPainterPath()
    clip.addEllipse(0, 0, size, size)
    p.setClipPath(clip)
    p.fillRect(0, 0, size, size, Qt.GlobalColor.white)
    p.drawPixmap(0, 0, src)
    p.end()
    return out


def developers_widget():
    """Cards for each developer, then credits for the projects Devium is built on."""
    w = QWidget()
    col = QVBoxLayout(w)
    col.setContentsMargins(0, 0, 0, 0)
    t = QLabel("Developers")
    t.setObjectName("h2")
    col.addWidget(t)
    for name, role, pic, link in DEVELOPERS:
        card = QWidget()
        card.setObjectName("devcard")
        card.setStyleSheet(f"QWidget#devcard {{ border: 1px solid palette(mid); border-radius: 14px; }}")
        row = QHBoxLayout(card)
        row.setContentsMargins(12, 10, 12, 10)
        card.setMinimumHeight(92)
        img = QLabel()
        img.setFixedSize(64, 64)
        img.setPixmap(round_pixmap(pic, 64))
        row.addWidget(img)
        txt = QLabel(f"<b style='font-size:13pt'>{name}</b><br>"
                     f"<span style='color:{ACCENT}'>{role}</span><br>"
                     f"<a href='{link}' style='color:#8a93a6'>{link.replace('https://', '')}</a>")
        txt.linkActivated.connect(lambda url: open_link(url, w))
        row.addWidget(txt, 1)
        col.addWidget(card)
    c = QLabel("Built with")
    c.setObjectName("h2")
    col.addWidget(c)
    links = QLabel("<br>".join(f"<a href='{u}' style='color:{ACCENT}'>{n}</a> &nbsp;—&nbsp; {d}"
                               for n, d, u in CREDITS))
    links.linkActivated.connect(lambda url: open_link(url, w))
    links.setMinimumHeight(links.sizeHint().height() + 8)
    col.addWidget(links)
    return w


def devium_version():
    try:
        for line in open("/etc/devium-release"):
            if line.startswith("DEVIUM_VERSION="):
                return line.strip().split("=", 1)[1]
    except OSError:
        pass
    return "beta"


# ---------------------------------------------------------------------------- links / QR codes
def has_browser():
    """Is there a web browser to open links with? (The live ISO and fresh installs have none.)"""
    import subprocess
    try:
        out = subprocess.run(["xdg-settings", "get", "default-web-browser"],
                             capture_output=True, text=True, timeout=3).stdout.strip()
    except Exception:
        out = ""
    if out:
        return True
    return any(shutil.which(b) for b in ("firefox", "brave", "brave-origin", "chromium", "google-chrome-stable",
                                         "vivaldi-stable", "librewolf", "epiphany", "falkon"))


def qr_pixmap(text, size=220):
    """Draw a QR code for `text` (needs python-qrcode; returns None without it)."""
    try:
        import qrcode
    except ImportError:
        return None
    from PyQt6.QtGui import QColor, QPainter
    qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(text)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    cell = max(1, size // n)
    pix = QPixmap(cell * n, cell * n)
    pix.fill(QColor("white"))
    p = QPainter(pix)
    for y, row in enumerate(m):
        for x, on in enumerate(row):
            if on:
                p.fillRect(x * cell, y * cell, cell, cell, QColor("#1b2026"))
    p.end()
    return pix


def open_link(url, parent=None):
    """Open a link. With no browser installed, show a QR code to open it on your phone instead."""
    from PyQt6.QtWidgets import QDialog, QPushButton
    browser = has_browser()
    dlg = QDialog(parent)
    dlg.setWindowTitle("Open on your phone")
    lay = QVBoxLayout(dlg)
    lay.setContentsMargins(24, 20, 24, 18)
    title = QLabel("Scan with your phone's camera")
    title.setObjectName("h2")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lay.addWidget(title)
    img = QLabel()
    img.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pix = qr_pixmap(url)
    if pix:
        img.setPixmap(pix)
    else:
        img.setText("(QR code unavailable)")
    lay.addWidget(img)
    link = QLabel(url)
    link.setAlignment(Qt.AlignmentFlag.AlignCenter)
    link.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    link.setStyleSheet(f"color: {ACCENT};")
    lay.addWidget(link)
    if not browser:
        note = QLabel("No web browser is installed yet. Pick one in Devium Setup after installing.")
        note.setObjectName("subtitle")
        note.setWordWrap(True)
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(note)
    row = QHBoxLayout()
    if browser:
        op = QPushButton("Open in browser")
        op.setObjectName("primary")
        op.clicked.connect(lambda: (launch("xdg-open", url), dlg.accept()))
        row.addWidget(op)
    close = QPushButton("Close")
    close.clicked.connect(dlg.accept)
    row.addWidget(close)
    lay.addLayout(row)
    dlg.exec()
