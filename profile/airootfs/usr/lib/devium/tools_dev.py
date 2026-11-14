"""Devium Tools pages added after beta15's first batch:
  Coding tools: dev doctor, one-click databases, local HTTPS, .env files, secret guard, snippets,
                share a local site, language versions, long-command notifications, offline docs
  Clean up:     find what takes space and remove it safely
  Guest account card (on the Privacy page)
Uses the small helpers devium-tools hands to tools_extra (Page, card, row, button, ...)."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

from PyQt6.QtCore import QProcess, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog, QHBoxLayout, QHeaderView,
                             QInputDialog, QLabel, QLineEdit, QListWidget, QMessageBox, QPlainTextEdit, QSpinBox,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

import devium_ui as ui
import tools_extra as X
from devium_i18n import T

HOME = os.path.expanduser("~")
CONFIG = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config")), "devium")
PROJECTS = os.environ.get("PROJECTS_DIR", os.path.join(HOME, "Projects"))
HOOKS = "/usr/lib/devium/git-hooks"
USER = os.environ.get("USER") or subprocess.run(["id", "-un"], capture_output=True, text=True).stdout.strip()


def sh(cmd, timeout=20, cwd=None):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def copy(text):
    QGuiApplication.clipboard().setText(text)


def engine():
    return "docker" if shutil.which("docker") else "podman" if shutil.which("podman") else None


# ============================================================================ one-click databases
DATABASES = [
    # id, name, image, port, env, volume path, connection string
    ("postgres", "PostgreSQL", "docker.io/library/postgres:17", 5432,
     {"POSTGRES_PASSWORD": "devium", "POSTGRES_USER": "devium", "POSTGRES_DB": "devium"}, "/var/lib/postgresql/data",
     "postgresql://devium:devium@localhost:5432/devium"),
    ("mysql", "MySQL", "docker.io/library/mysql:8.4", 3306,
     {"MYSQL_ROOT_PASSWORD": "devium", "MYSQL_DATABASE": "devium", "MYSQL_USER": "devium", "MYSQL_PASSWORD": "devium"},
     "/var/lib/mysql", "mysql://devium:devium@localhost:3306/devium"),
    ("redis", "Redis", "docker.io/library/redis:7", 6379, {}, "/data", "redis://localhost:6379"),
    ("mongo", "MongoDB", "docker.io/library/mongo:8", 27017,
     {"MONGO_INITDB_ROOT_USERNAME": "devium", "MONGO_INITDB_ROOT_PASSWORD": "devium"}, "/data/db",
     "mongodb://devium:devium@localhost:27017"),
]


def db_state(eng, did):
    out = sh([eng, "ps", "-a", "--filter", f"name=^devium-{did}$", "--format", "{{.Status}}"]).strip()
    return "running" if out.startswith("Up") else ("stopped" if out else "none")


def make_db_card(page):
    status = {}
    rows = QVBoxLayout()
    note = X.label("", "subtitle")

    def refresh():
        eng = engine()
        note.setText(("Uses " + eng + ". Data is kept between restarts (in a container volume). "
                      "Password for all of them: devium (for your own computer only).") if eng else
                     "Needs Docker or Podman: install one on the Developer page first.")
        for did, *_ in DATABASES:
            st = db_state(eng, did) if eng else "none"
            lab, start, stop, rm = status[did]
            lab.setText({"running": "<span style='color:%s'>● running</span>" % ui.ACCENT,
                         "stopped": "○ stopped", "none": "not created"}[st])
            start.setEnabled(bool(eng) and st != "running")
            stop.setEnabled(st == "running")
            rm.setEnabled(st != "none")

    def start(db):
        did, name, image, port, env, vol, url = db
        eng = engine()
        if db_state(eng, did) == "stopped":
            args = [eng, "start", f"devium-{did}"]
        else:
            args = [eng, "run", "-d", "--name", f"devium-{did}", "--restart", "unless-stopped",
                    "-p", f"127.0.0.1:{port}:{port}", "-v", f"devium-{did}:{vol}"]
            for k, v in env.items():
                args += ["-e", f"{k}={v}"]
            args.append(image)
        X.RunDialog(page, f"{name}", args[0], args[1:], done=lambda c: refresh()).exec()

    def stop(did):
        sh([engine(), "stop", f"devium-{did}"], timeout=60)
        refresh()

    def remove(did, name):
        if QMessageBox.question(page, name, f"Delete {name} and all its data?") == QMessageBox.StandardButton.Yes:
            eng = engine()
            sh([eng, "rm", "-f", f"devium-{did}"], timeout=60)
            sh([eng, "volume", "rm", f"devium-{did}"], timeout=60)
            refresh()

    for db in DATABASES:
        did, name, image, port, env, vol, url = db
        lab = QLabel()
        lab.setTextFormat(Qt.TextFormat.RichText)
        conn = QLineEdit(url)
        conn.setReadOnly(True)
        conn.setMinimumWidth(240)
        b_start = X.button(T("Start"), lambda _c=False, db=db: start(db), icon="media-playback-start")
        b_stop = X.button(T("Stop"), lambda _c=False, did=did: stop(did), icon="media-playback-stop")
        b_rm = X.button(T("Delete"), lambda _c=False, did=did, name=name: remove(did, name), icon="edit-delete")
        b_rm.setToolTip(T("Delete it and its data"))
        b_copy = X.button(T("Copy"), lambda _c=False, url=url: copy(url), icon="edit-copy")
        b_copy.setToolTip(T("Copy the connection string"))
        status[did] = (lab, b_start, b_stop, b_rm)
        name_lab = QLabel(f"<b>{name}</b>")
        name_lab.setMinimumWidth(95)
        lab.setMinimumWidth(80)
        rows.addLayout(X.row(name_lab, lab, conn, stretch=False))
        rows.addLayout(X.row(QLabel(""), b_copy, b_start, b_stop, b_rm))
    holder = QWidget()
    holder.setLayout(rows)
    page.add(X.card(X.label(T("Databases in one click"), "h2"),
                    X.label("Start a database for your project without installing it on your system. "
                            "Copy the connection string into your app.", "subtitle"), holder, note))
    return refresh


# ============================================================================ local HTTPS
CERTS = os.path.join(HOME, ".local/share/devium/certs")


def make_https_card(page):
    state = X.label("", "subtitle")
    state.setTextFormat(Qt.TextFormat.RichText)

    def refresh():
        pem = os.path.join(CERTS, "localhost.pem")
        if os.path.exists(pem):
            state.setText(f"✓ Ready. Certificate: <code>~/.local/share/devium/certs/localhost.pem</code>, "
                          f"key: <code>localhost-key.pem</code><br>"
                          "Vite: <code>server: { https: { cert, key } }</code> · "
                          "Python: <code>uvicorn app:app --ssl-certfile …pem --ssl-keyfile …key.pem</code> · "
                          "Node: <code>https.createServer({ cert, key }, app)</code>")
        else:
            state.setText("Not set up yet.")

    def setup():
        X.root(page, T("Local HTTPS"), "local-https", USER, done=lambda c: refresh())

    page.add(X.card(X.label(T("HTTPS on localhost"), "h2"),
                    X.label("Some features (camera, service workers, secure cookies, OAuth) only work over HTTPS. "
                            "This makes a certificate your browsers trust for localhost, so https://localhost "
                            "works with no warnings. Only this computer trusts it.", "subtitle"),
                    state, X.row(X.button(T("Set up local HTTPS"), setup, True, "security-high"),
                                 X.button(T("Open folder"), lambda: ui.launch("xdg-open", CERTS)
                                          if os.path.isdir(CERTS) else None, icon="folder"))))
    return refresh


# ============================================================================ .env files
def find_envs():
    out = []
    if not os.path.isdir(PROJECTS):
        return out
    for top, dirs, files in os.walk(PROJECTS):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", ".venv", "venv", "target", "__pycache__")]
        if top.count(os.sep) - PROJECTS.count(os.sep) > 4:
            dirs[:] = []
        for f in files:
            if re.fullmatch(r"\.env(\..+)?", f) and not f.endswith((".example", ".sample", ".template")):
                out.append(os.path.join(top, f))
    return out


def env_status(path):
    d, f = os.path.split(path)
    if not sh(["git", "-C", d, "rev-parse", "--is-inside-work-tree"]).strip():
        return "not in Git", 0
    if subprocess.run(["git", "-C", d, "ls-files", "--error-unmatch", f], capture_output=True).returncode == 0:
        return "COMMITTED", 2
    if subprocess.run(["git", "-C", d, "check-ignore", "-q", f], capture_output=True).returncode == 0:
        return "ignored ✓", 0
    return "not ignored", 1


def make_env_card(page):
    tree = QTreeWidget()
    tree.setHeaderLabels([T("File"), T("Git"), T("Keys")])
    tree.setRootIsDecorated(False)
    tree.setMaximumHeight(170)
    tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    view = QPlainTextEdit()
    view.setReadOnly(True)
    view.setMaximumHeight(110)
    view.setPlaceholderText(T("Pick a file to see its keys (values are hidden)."))

    def refresh():
        tree.clear()
        for p in find_envs():
            st, level = env_status(p)
            try:
                keys = [l.split("=", 1)[0].strip() for l in open(p, errors="ignore")
                        if "=" in l and not l.lstrip().startswith("#")]
            except OSError:
                keys = []
            it = QTreeWidgetItem([p.replace(HOME, "~", 1), st, str(len(keys))])
            it.setData(0, Qt.ItemDataRole.UserRole, (p, keys))
            if level:
                for c in range(3):
                    it.setForeground(c, Qt.GlobalColor.red if level == 2 else Qt.GlobalColor.darkYellow)
            tree.addTopLevelItem(it)
        if not tree.topLevelItemCount():
            tree.addTopLevelItem(QTreeWidgetItem([T("No .env files in ~/Projects"), "", ""]))

    def picked():
        it = tree.currentItem()
        data = it.data(0, Qt.ItemDataRole.UserRole) if it else None
        if data:
            view.setPlainText("\n".join(f"{k}=••••••" for k in data[1]) or "(empty)")

    def ignore():
        it = tree.currentItem()
        data = it.data(0, Qt.ItemDataRole.UserRole) if it else None
        if not data:
            return
        p = data[0]
        d, f = os.path.split(p)
        top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).strip() or d
        rel = os.path.relpath(p, top)
        gi = os.path.join(top, ".gitignore")
        lines = open(gi).read().splitlines() if os.path.exists(gi) else []
        if ".env" not in lines and rel not in lines:
            with open(gi, "a") as fh:
                fh.write(("\n" if lines and lines[-1] else "") + "# secrets (added by Devium)\n.env\n.env.*\n!.env.example\n")
        if env_status(p)[1] == 2:   # already committed: stop tracking it (the file stays on disk)
            sh(["git", "-C", top, "rm", "--cached", "-q", rel])
            QMessageBox.information(page, ".env",
                                    "Done. The file stays on your computer but Git stops tracking it; commit the "
                                    "change. It's still in your Git history, so change any passwords or keys in it.")
        refresh()

    def example():
        it = tree.currentItem()
        data = it.data(0, Qt.ItemDataRole.UserRole) if it else None
        if data:
            out = os.path.join(os.path.dirname(data[0]), ".env.example")
            with open(out, "w") as fh:
                fh.write("".join(f"{k}=\n" for k in data[1]))
            QMessageBox.information(page, ".env", f"Made {out.replace(HOME, '~')} with the key names and no "
                                                  "values: safe to commit, so others know what to fill in.")

    tree.itemSelectionChanged.connect(picked)
    page.add(X.card(X.label(T(".env files"), "h2"),
                    X.label("Your projects' secret files. Red means it's committed to Git (anyone with the repo can "
                            "read it); yellow means Git could commit it by accident.", "subtitle"),
                    tree, view,
                    X.row(X.button(T("Keep it out of Git"), ignore, True, "security-high"),
                          X.button(T("Make .env.example"), example, icon="document-new"),
                          X.button(T("Refresh"), refresh, icon="view-refresh"))))
    return refresh


# ============================================================================ secret guard
def guard_on():
    return HOOKS in sh(["git", "config", "--global", "core.hooksPath"])


def set_guard(on):
    if on:
        subprocess.run(["git", "config", "--global", "core.hooksPath", HOOKS])
    else:
        subprocess.run(["git", "config", "--global", "--unset", "core.hooksPath"])


def make_guard_card(page):
    box = QCheckBox(T("Stop commits that contain passwords, API keys or private keys"))
    box.setChecked(guard_on())
    box.toggled.connect(set_guard)
    leaks = X.label("", "subtitle")

    def refresh():
        box.blockSignals(True)
        box.setChecked(guard_on())
        box.blockSignals(False)
        leaks.setText("Using gitleaks (thorough)." if shutil.which("gitleaks") else
                      "Using Devium's built-in check (GitHub/AWS/Discord/Stripe tokens, private keys, .env files). "
                      "Install gitleaks for a more thorough one.")

    page.add(X.card(X.label(T("Secret guard"), "h2"),
                    X.label("Checks every commit in every repo before it's made. Your projects' own Git hooks still "
                            "run. Sure it's not a secret? git commit --no-verify skips it once.", "subtitle"),
                    box, leaks,
                    X.row(X.button(T("Install gitleaks"), lambda: X.root(page, "gitleaks", "devpack", "gitleaks",
                                                                         done=lambda c: refresh()),
                                   icon="run-install"))))
    return refresh


# ============================================================================ snippets
def snippets():
    try:
        return json.loads(sh(["snip", "--json"]) or "{}")
    except ValueError:
        return {}


def make_snippets_card(page):
    lst = QListWidget()
    lst.setMaximumHeight(150)
    text = QPlainTextEdit()
    text.setMaximumHeight(130)
    text.setFont(QFont("monospace"))

    def refresh():
        cur = lst.currentItem().text() if lst.currentItem() else None
        lst.clear()
        for k in sorted(snippets()):
            lst.addItem(k)
            if k == cur:
                lst.setCurrentRow(lst.count() - 1)

    def picked():
        it = lst.currentItem()
        if it:
            text.setPlainText(snippets().get(it.text(), ""))

    def save_cur():
        it = lst.currentItem()
        if it:
            subprocess.run(["snip", "add", it.text()], input=text.toPlainText(), text=True)

    def add():
        name, ok = QInputDialog.getText(page, T("New snippet"), T("Name (e.g. docker-compose):"))
        name = name.strip().replace(" ", "-")
        if ok and name:
            subprocess.run(["snip", "add", name], input=QGuiApplication.clipboard().text() or "…", text=True)
            refresh()
            for i in range(lst.count()):
                if lst.item(i).text() == name:
                    lst.setCurrentRow(i)

    def delete():
        it = lst.currentItem()
        if it and QMessageBox.question(page, T("Delete"), f"Delete '{it.text()}'?") == QMessageBox.StandardButton.Yes:
            subprocess.run(["snip", "rm", it.text()], capture_output=True)
            text.clear()
            refresh()

    lst.itemSelectionChanged.connect(picked)
    split = QHBoxLayout()
    split.addWidget(lst, 1)
    split.addWidget(text, 2)
    holder = QWidget()
    holder.setLayout(split)
    page.add(X.card(X.label(T("Snippets"), "h2"),
                    X.label("Code you reuse. Find them in Spotlight (Meta+Space, then: snip docker) or in the "
                            "terminal (snip NAME copies it). New snippets start with what's on your clipboard.",
                            "subtitle"),
                    holder,
                    X.row(X.button(T("New"), add, True, "list-add"), X.button(T("Save"), save_cur, icon="document-save"),
                          X.button(T("Copy"), lambda: copy(text.toPlainText()), icon="edit-copy"),
                          X.button(T("Delete"), delete, icon="edit-delete"))))
    return refresh


# ============================================================================ share a local site
def make_share_card(page):
    port = QSpinBox()
    port.setRange(1, 65535)
    port.setValue(3000)
    link = QLineEdit()
    link.setReadOnly(True)
    link.setPlaceholderText(T("The public link appears here"))
    qr = QLabel()
    state = X.label("", "subtitle")
    page.share_proc = None

    def start():
        if not shutil.which("cloudflared"):
            X.root(page, T("Share"), "devpack", "share")
            if not shutil.which("cloudflared"):
                return
        stop()
        p = QProcess(page)
        p.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        def got():
            out = bytes(p.readAllStandardOutput()).decode(errors="replace")
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", out)
            if m and not link.text():
                link.setText(m.group(0))
                pix = ui.qr_pixmap(m.group(0), 150)
                if pix:
                    qr.setPixmap(pix)
                state.setText(f"Sharing localhost:{port.value()}. Anyone with the link can see it until you press Stop.")
        p.readyReadStandardOutput.connect(got)
        p.finished.connect(lambda *_: state.setText(T("Stopped.")))
        link.clear()
        qr.clear()
        state.setText(T("Getting a link…"))
        p.start("cloudflared", ["tunnel", "--no-autoupdate", "--url", f"http://localhost:{port.value()}"])
        page.share_proc = p

    def stop():
        if page.share_proc and page.share_proc.state() != QProcess.ProcessState.NotRunning:
            page.share_proc.terminate()
            page.share_proc.waitForFinished(3000)
        link.clear()
        qr.clear()

    page.add(X.card(X.label(T("Share a local site"), "h2"),
                    X.label("Give your localhost a temporary public link: show a friend, or open it on your phone "
                            "(scan the code). Free, no account (Cloudflare quick tunnels).", "subtitle"),
                    X.row(QLabel(T("Port:")), port, X.button(T("Share"), start, True, "document-share"),
                          X.button(T("Stop"), stop, icon="process-stop")),
                    X.row(link, X.button("", lambda: copy(link.text()), icon="edit-copy"),
                          X.button("", lambda: link.text() and ui.open_link(link.text(), page), icon="internet-web-browser"),
                          stretch=False),
                    qr, state))
    return lambda: None


# ============================================================================ language versions (mise)
LANGS = [("python", "Python"), ("node", "Node.js"), ("go", "Go"), ("rust", "Rust"), ("java", "Java"),
         ("bun", "Bun"), ("deno", "Deno"), ("ruby", "Ruby")]


class Fetch(QThread):
    done = pyqtSignal(list)

    def __init__(self, lang):
        super().__init__()
        self.lang = lang

    def run(self):
        out = sh(["mise", "ls-remote", self.lang], timeout=40).split()
        stable = [v for v in out if re.fullmatch(r"\d+(\.\d+){0,2}", v)]
        # newest first, one per minor version
        seen, pick = set(), []
        for v in reversed(stable):
            key = ".".join(v.split(".")[:2])
            if key not in seen:
                seen.add(key)
                pick.append(v)
        self.done.emit(pick[:25])


def make_versions_card(page):
    folder = QLineEdit(PROJECTS)
    lang = QComboBox()
    for k, n in LANGS:
        lang.addItem(n, k)
    ver = QComboBox()
    ver.setMinimumWidth(130)
    state = X.label("", "subtitle")
    state.setTextFormat(Qt.TextFormat.RichText)

    def have():
        return bool(shutil.which("mise"))

    def load_versions():
        ver.clear()
        if not have():
            return
        ver.addItem(T("loading…"))
        page.fetch = Fetch(lang.currentData())
        page.fetch.done.connect(lambda vs: (ver.clear(), ver.addItems(vs or ["latest"])))
        page.fetch.start()

    def current():
        if not have():
            state.setText("Needs mise. Press <b>Install mise</b> (it also adds direnv and just).")
            return
        out = sh(["mise", "current"], cwd=folder.text() if os.path.isdir(folder.text()) else HOME).strip()
        state.setText("In this folder: <code>" + (out.replace("\n", "</code> · <code>") or "system versions") + "</code>")

    def browse():
        d = QFileDialog.getExistingDirectory(page, T("Pick a project folder"), folder.text())
        if d:
            folder.setText(d)
            current()

    def use():
        if not os.path.isdir(folder.text()) or not ver.currentText() or ver.currentText().startswith(T("loading")):
            return
        X.RunDialog(page, T("Language versions"), "mise",
                    ["use", "--cd", folder.text(), f"{lang.currentData()}@{ver.currentText()}"],
                    done=lambda c: current()).exec()

    lang.currentIndexChanged.connect(lambda _i: load_versions())
    folder.editingFinished.connect(current)
    page.add(X.card(X.label(T("Language versions per project"), "h2"),
                    X.label("One project on Python 3.11, another on 3.13? Pick the folder and version. It's saved in "
                            "the project (mise.toml) and switches by itself when you cd into it.", "subtitle"),
                    X.row(QLabel(T("Folder:")), folder, X.button("…", browse), stretch=False),
                    X.row(lang, ver, X.button(T("Use in this folder"), use, True, "dialog-ok"),
                          X.button(T("Install mise"), lambda: X.root(page, "mise", "devpack", "mise",
                                                                     done=lambda c: (load_versions(), current())),
                                   icon="run-install")),
                    state))

    def refresh():
        current()
        if have() and not ver.count():
            load_versions()
    return refresh


# ============================================================================ long-command notifications
NOTIFY_FILE = os.path.join(CONFIG, "notify-after")


def make_notify_card(page):
    box = QCheckBox(T("Tell me when a long terminal command finishes"))
    secs = QSpinBox()
    secs.setRange(5, 3600)
    secs.setSuffix(" s")
    try:
        v = int(open(NOTIFY_FILE).read().strip())
    except (OSError, ValueError):
        v = 30
    box.setChecked(v > 0)
    secs.setValue(v if v > 0 else 30)

    def save():
        os.makedirs(CONFIG, exist_ok=True)
        with open(NOTIFY_FILE, "w") as f:
            f.write(str(secs.value() if box.isChecked() else 0))
        secs.setEnabled(box.isChecked())

    box.toggled.connect(lambda _b: save())
    secs.valueChanged.connect(lambda _v: save())
    secs.setEnabled(box.isChecked())
    page.add(X.card(X.label(T("Build notifications"), "h2"),
                    X.label("Start a build, install or test run, switch to something else, and get a notification "
                            "when it's done (or failed). Editors, dev servers and ssh are skipped. Applies to new "
                            "terminals.", "subtitle"),
                    X.row(box, QLabel(T("after")), secs)))
    return lambda: None


# ============================================================================ Coding tools page
def make_coding_page(win):
    page = X.Page(T("Coding tools"), T("Handy tools for coding: check your setup, start databases, keep secrets out "
                                       "of Git, share your work and more."))
    page.add(X.card(X.label(T("Dev doctor"), "h2"),
                    X.label("Checks Git, your SSH key and GitHub, languages, Docker, PATH and your projects, and "
                            "tells you how to fix anything missing. In a terminal: support dev", "subtitle"),
                    X.row(X.button(T("Check my setup"), lambda: X.in_terminal("support dev"), True, "tools-wizard"))))
    refreshers = [make_db_card(page), make_guard_card(page), make_env_card(page), make_https_card(page),
                  make_share_card(page), make_versions_card(page), make_snippets_card(page), make_notify_card(page)]
    page.add(X.card(X.label(T("Offline docs"), "h2"),
                    X.label("Zeal: docs for Python, JavaScript, Rust, Go, C++, React and 200 more that work without "
                            "internet. In Spotlight: docs python:split", "subtitle"),
                    X.row(X.button(T("Open Zeal"), lambda: ui.launch("zeal"), icon="zeal"),
                          X.button(T("Install Zeal"), lambda: X.root(page, "Zeal", "devpack", "zeal"), icon="run-install"))))
    page.finish()
    page.on_show = lambda: [r() for r in refreshers]
    return page


# ============================================================================ Clean up
def du(path):
    try:
        out = subprocess.run(["du", "-sb", path], capture_output=True, text=True, timeout=120).stdout.split()
        return int(out[0]) if out else 0
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return 0


def old(path, days):
    try:
        return time.time() - os.path.getmtime(path) > days * 86400
    except OSError:
        return False


class Scan(QThread):
    """Look for things that take space. Emits [(id, title, why, size, paths or None, kind)]."""
    found = pyqtSignal(list)

    def run(self):
        items = []
        cache = os.path.join(HOME, ".cache")
        if os.path.isdir(cache):
            parts = [os.path.join(cache, d) for d in os.listdir(cache) if d not in ("devium",)]
            items.append(("cache", "App caches", "Thumbnails, browser and app caches. Apps rebuild them as needed.",
                          sum(du(p) for p in parts), parts, "user"))
        trash = os.path.join(HOME, ".local/share/Trash")
        if os.path.isdir(trash):
            items.append(("trash", "The bin", "Files you already deleted.", du(trash),
                          [os.path.join(trash, "files"), os.path.join(trash, "info")], "user"))
        # build folders in projects not touched for 30 days
        builds = []
        for top, dirs, files in os.walk(HOME):
            rel = top[len(HOME):].count(os.sep)
            dirs[:] = [d for d in dirs if not d.startswith(".") or d == ".venv"]
            if rel > 6:
                dirs[:] = []
                continue
            for d in list(dirs):
                full = os.path.join(top, d)
                if d == "node_modules" or (d == "target" and os.path.exists(os.path.join(top, "Cargo.toml"))) or \
                        (d in (".venv", "venv") and os.path.exists(os.path.join(full, "pyvenv.cfg"))) or \
                        (d == "build" and os.path.exists(os.path.join(top, "CMakeLists.txt"))):
                    dirs.remove(d)
                    if old(top, 30) and old(full, 30):
                        builds.append(full)
        if builds:
            items.append(("builds", "Old build folders",
                          "node_modules, Rust target, Python .venv and CMake build folders in projects you haven't "
                          "touched for 30 days. They come back with npm install / cargo build.",
                          sum(du(b) for b in builds), builds, "user"))
        dl = os.path.join(HOME, "Downloads")
        if os.path.isdir(dl):
            olddl, by_hash, dupes = [], {}, []
            for f in os.listdir(dl):
                p = os.path.join(dl, f)
                if not os.path.isfile(p):
                    continue
                if re.search(r"\.(iso|img|zip|tar\.\w+|7z|rar|exe|msi|deb|rpm|AppImage|dmg)$", f, re.I) and old(p, 30):
                    olddl.append(p)
                try:
                    if os.path.getsize(p) > 1024 * 1024:
                        h = hashlib.sha1()
                        with open(p, "rb") as fh:
                            h.update(fh.read(4 * 1024 * 1024))
                        key = (os.path.getsize(p), h.hexdigest())
                        if key in by_hash:
                            dupes.append(p)
                        else:
                            by_hash[key] = p
                except OSError:
                    pass
            if olddl:
                items.append(("olddl", "Old installers and archives in Downloads",
                              "ISOs, zips and installers you downloaded more than 30 days ago.",
                              sum(os.path.getsize(p) for p in olddl), olddl, "user"))
            if dupes:
                items.append(("dupes", "Duplicate downloads", "The same file downloaded more than once "
                              "(the first copy is kept).", sum(os.path.getsize(p) for p in dupes), dupes, "user"))
        big = []
        for top, dirs, files in os.walk(HOME):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
            for f in files:
                p = os.path.join(top, f)
                try:
                    if os.path.getsize(p) > 500 * 1024 * 1024 and old(p, 90):
                        big.append(p)
                except OSError:
                    pass
        if big:
            items.append(("big", "Big files you haven't changed in 3 months",
                          "Over 500 MB each. Only the ones you tick below are deleted.",
                          sum(os.path.getsize(p) for p in big), big, "pick"))
        eng = engine()
        if eng:
            out = sh([eng, "system", "df", "--format", "{{.Type}}\t{{.Reclaimable}}"], timeout=30)
            size = 0
            for line in out.splitlines():
                m = re.search(r"([\d.]+)\s*([kMGT]?B)", line.split("\t")[-1])
                if m:
                    size += float(m.group(1)) * {"B": 1, "kB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12}[m.group(2)]
            if size > 50e6:
                items.append(("docker", f"Unused {eng} images and build cache",
                              "Stopped containers, images nothing uses and old build layers.", int(size), None, "user"))
        if shutil.which("flatpak"):
            items.append(("flatpak-user", "Unused Flatpak runtimes (yours)",
                          "Shared files no app of yours needs any more.", 0, None, "user"))
        pkg = du("/var/cache/pacman/pkg")
        logs = re.search(r"take up ([\d.]+)([KMGT])", sh(["journalctl", "--disk-usage"]))
        logsize = int(float(logs.group(1)) * {"K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}[logs.group(2)]) if logs else 0
        items.append(("system", "System: old package versions, unused system Flatpaks, logs, crash dumps",
                      "Keeps the newest package version so updates can still be undone. Asks for your password.",
                      pkg + max(0, logsize - 200 * 1024 * 1024), None, "root"))
        self.found.emit(items)


def make_clean_page(win):
    page = X.Page(T("Clean up"), T("Find what's taking space and remove it safely. Nothing is deleted until you "
                                   "press Clean, and only what you tick."))
    page.summary = X.label("", "h2")
    page.add(page.summary)
    tree = QTreeWidget()
    tree.setHeaderLabels([T("What"), T("Size")])
    tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    tree.setMinimumHeight(360)
    page.add(tree)
    why_lab = X.label("", "subtitle")
    page.add(why_lab)

    def picked():
        it = tree.currentItem()
        while it and it.parent():
            it = it.parent()
        if it:
            iid = it.data(0, Qt.ItemDataRole.UserRole)
            why_lab.setText(next((T(x[2]) for x in page.items if x[0] == iid), ""))
    tree.itemSelectionChanged.connect(picked)
    page.scan_btn = X.button(T("Look again"), lambda: scan(), icon="view-refresh")
    page.clean_btn = X.button(T("Clean selected"), lambda: clean(), True, "edit-clear")
    page.add(X.row(page.clean_btn, page.scan_btn,
                   X.button(T("See what's big (Filelight)"), lambda: ui.launch("filelight") or ui.launch("baobab"),
                            icon="filelight")))
    page.items = []

    def human(n):
        return X.human(n) if n else ""

    def show(items):
        page.items = items
        tree.clear()
        total = 0
        for iid, title, why, size, paths, kind in items:
            it = QTreeWidgetItem([T(title), human(size)])
            it.setToolTip(0, T(why))
            it.setData(0, Qt.ItemDataRole.UserRole, iid)
            it.setFlags(it.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            safe = kind == "user" and iid not in ("cache",)
            it.setCheckState(0, Qt.CheckState.Checked if safe and size else Qt.CheckState.Unchecked)
            if paths and iid in ("big", "builds", "dupes", "olddl"):
                for p in paths[:200]:
                    ch = QTreeWidgetItem([p.replace(HOME, "~", 1), human(du(p) if os.path.isdir(p) else os.path.getsize(p))])
                    ch.setData(0, Qt.ItemDataRole.UserRole, p)
                    ch.setFlags(ch.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    ch.setCheckState(0, Qt.CheckState.Unchecked if iid == "big" else Qt.CheckState.Checked)
                    it.addChild(ch)
            tree.addTopLevelItem(it)
            total += size
        why_lab.setText(T("Click a line to see what it is. Ticked lines are removed when you press Clean selected."))
        page.summary.setText(f"{human(total) or '0 B'} " + T("could be freed") +
                             f" · {X.human(shutil.disk_usage(HOME).free)} {T('free now')}")
        page.scan_btn.setEnabled(True)
        page.clean_btn.setEnabled(True)

    def scan():
        page.summary.setText(T("Looking… (this can take a minute)"))
        page.scan_btn.setEnabled(False)
        page.clean_btn.setEnabled(False)
        tree.clear()
        page.scanner = Scan()
        page.scanner.found.connect(show)
        page.scanner.start()

    def remove(p):
        try:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.lexists(p):
                os.remove(p)
        except OSError:
            pass

    def clean():
        chosen = []
        for i in range(tree.topLevelItemCount()):
            it = tree.topLevelItem(i)
            iid = it.data(0, Qt.ItemDataRole.UserRole)
            item = next(x for x in page.items if x[0] == iid)
            kids = [it.child(j) for j in range(it.childCount())]
            if kids:
                picked = [k.data(0, Qt.ItemDataRole.UserRole) for k in kids if k.checkState(0) == Qt.CheckState.Checked]
                if picked and (it.checkState(0) != Qt.CheckState.Unchecked or iid == "big"):
                    chosen.append((iid, picked))
            elif it.checkState(0) == Qt.CheckState.Checked:
                chosen.append((iid, item[4]))
        if not chosen:
            return
        names = ", ".join(T(next(x[1] for x in page.items if x[0] == c[0])) for c in chosen)
        if QMessageBox.question(page, T("Clean up"), T("Delete these now?") + f"\n\n{names}") != \
                QMessageBox.StandardButton.Yes:
            return
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            for iid, paths in chosen:
                if iid == "trash":
                    for d in paths or []:
                        if os.path.isdir(d):
                            for f in os.listdir(d):
                                remove(os.path.join(d, f))
                elif iid == "docker":
                    sh([engine(), "system", "prune", "-f"], timeout=300)
                elif iid == "flatpak-user":
                    sh(["flatpak", "uninstall", "--user", "--unused", "-y", "--noninteractive"], timeout=300)
                elif iid == "system":
                    continue
                else:
                    for p in paths or []:
                        if p.startswith(HOME + os.sep):     # only ever inside your home folder
                            remove(p)
        finally:
            QApplication.restoreOverrideCursor()
        if any(c[0] == "system" for c in chosen):
            X.root(page, T("Clean up"), "clean-system")
        scan()

    page.on_show = lambda: page.items or scan()
    page.finish()
    return page


# ============================================================================ Guest account (Privacy page)
def add_guest_card(page):
    box = QCheckBox(T("Guest account"))

    def exists():
        return subprocess.run(["id", "guest"], capture_output=True).returncode == 0

    box.setChecked(exists())

    def toggled(on):
        r = subprocess.run(["pkexec", "/usr/lib/devium/devium-helper", "guest", "on" if on else "off"])
        if r.returncode != 0 or exists() != on:
            box.blockSignals(True)
            box.setChecked(exists())
            box.blockSignals(False)

    box.toggled.connect(toggled)
    w = X.card(box, X.label("Let a friend use this computer without seeing your files or changing your settings. "
                            "They press Guest on the login screen (no password). Everything they do is deleted when "
                            "they log out, and Guest can't install apps or change system settings.", "subtitle"))
    page.col.insertWidget(page.col.count() - 1, w)
    return page
