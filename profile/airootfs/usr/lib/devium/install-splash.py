#!/usr/bin/env python3
"""Small Devium splash shown while the installer starts (it can take a few seconds).
Closes itself when the installer's window appears (or after 45 seconds)."""
import math
import subprocess
import sys
import time

sys.path.insert(0, "/usr/lib/devium")

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

import devium_ui as ui


class Splash(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
                            | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, 300)
        self.logo = QPixmap(ui.LOGO).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
        self.t0 = time.time()
        self.seen = None
        tick = QTimer(self)
        tick.timeout.connect(self.update)
        tick.start(33)
        check = QTimer(self)
        check.timeout.connect(self.check)
        check.start(500)

    def check(self):
        running = subprocess.run(["pgrep", "-x", "calamares"], capture_output=True).returncode == 0
        if running and self.seen is None:
            self.seen = time.time()
        elapsed = time.time() - self.t0
        # the window shows a few seconds after the process starts
        if (self.seen and time.time() - self.seen > 6) or elapsed > 45 or (elapsed > 8 and not running):
            QApplication.quit()

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(36, 42, 50, 240))
        p.drawRoundedRect(self.rect(), 24, 24)
        t = time.time() - self.t0
        p.setOpacity(0.65 + 0.35 * math.sin(t * 2.4))      # the logo gently "breathes"
        p.drawPixmap((self.width() - self.logo.width()) // 2, 46, self.logo)
        p.setOpacity(1)
        p.setPen(QColor("#dde3ea"))
        f = p.font()
        f.setPointSize(13)
        f.setBold(True)
        p.setFont(f)
        p.drawText(0, 190, self.width(), 30, Qt.AlignmentFlag.AlignCenter, "Starting the Devium installer")
        for i in range(3):                                  # three pulsing dots
            a = 0.25 + 0.75 * abs(math.sin(t * 3 - i * 0.6))
            p.setBrush(QColor(143, 180, 216, int(255 * a)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(self.width() // 2 - 26 + i * 20, 240, 12, 12)


def main():
    app = QApplication(sys.argv)
    s = Splash()
    screen = app.primaryScreen().availableGeometry()
    s.move(screen.center().x() - s.width() // 2, screen.center().y() - s.height() // 2)
    s.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
