"""Shared look for the Devium apps (PyQt6)."""
import os
import shutil
import subprocess

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

LOGO = "/usr/share/devium/logo.png"
ACCENT = "#22d3ee"
ACCENT2 = "#8b5cf6"

STYLE = f"""
QWidget {{ font-size: 10.5pt; }}
QLabel#title {{ font-size: 20pt; font-weight: 700; }}
QLabel#subtitle {{ color: #8a93a6; }}
QLabel#h2 {{ font-size: 13pt; font-weight: 600; margin-top: 6px; }}
QPushButton {{ padding: 7px 14px; border-radius: 8px; }}
QPushButton#primary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:1 {ACCENT2});
    color: white; font-weight: 600; border: none;
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
    color: white;
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


def launch(*cmd: str) -> bool:
    """Start a program in the background. Returns False if it isn't installed."""
    if not shutil.which(cmd[0]):
        return False
    subprocess.Popen(list(cmd), start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


HELPER = ["pkexec", "/usr/lib/devium/devium-helper"]
