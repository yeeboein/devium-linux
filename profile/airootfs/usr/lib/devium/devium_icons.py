#!/usr/bin/env python3
"""Devium icons that follow you:

  devium_icons.py all        both of the below (what Devium runs after you change the accent colour, and at login)
  devium_icons.py accent     the Devium app icons use your accent colour (Devium Tools > Look) instead of the blue
  devium_icons.py webapps    websites installed as apps (Brave, Chrome, Chromium... "Install as app") get their
                             favicon on the Devium gradient, like every other app icon

Everything is written to your own folder (~/.local/share/icons/Devium and Devium-Dark), never to the system, and the
first line of each function says how to undo it: pick the Devium blue again, or delete those two folders.
"""
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from urllib.parse import urlparse

HOME = os.path.expanduser("~")
DATA = os.environ.get("XDG_DATA_HOME", os.path.join(HOME, ".local/share"))
CONFIG = os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))
SYS_ICONS = os.environ.get("DEVIUM_SYS_ICONS", "/usr/share/icons")
THEMES = ("Devium", "Devium-Dark")
DEFAULT = ("#8fb4d8", "#b4b8e0")
MARK = ".devium-managed"          # in a folder we created: it is safe for us to rebuild it
WEB_DIR = "256x256/apps"


def accent():
    try:
        a, b = open(os.path.join(CONFIG, "devium", "accent")).read().split()[:2]
        if re.fullmatch(r"#[0-9a-fA-F]{6}", a) and re.fullmatch(r"#[0-9a-fA-F]{6}", b):
            return a.lower(), b.lower()
    except (OSError, ValueError):
        pass
    return DEFAULT


def user_theme(name):
    return os.path.join(DATA, "icons", name)


def write_index(name, with_web):
    """Our own index.theme (the system one, plus the folder of website icons when there are any)."""
    src = os.path.join(SYS_ICONS, name, "index.theme")
    try:
        text = open(src, encoding="utf-8").read()
    except OSError:
        return
    if with_web and WEB_DIR not in text:
        text = re.sub(r"^(Directories=.*)$", r"\1," + WEB_DIR, text, count=1, flags=re.M)
        text += f"\n[{WEB_DIR}]\nSize=256\nType=Fixed\nContext=Applications\n"
    with open(os.path.join(user_theme(name), "index.theme"), "w", encoding="utf-8") as f:
        f.write(text)


def reset_managed(name):
    """Forget what we made before (only in a folder with our mark), so old colours and old website icons go away."""
    base = user_theme(name)
    if os.path.isfile(os.path.join(base, MARK)):
        shutil.rmtree(base, ignore_errors=True)
    elif os.path.isdir(base):
        return False        # a folder that is not ours: leave it alone
    return True


# ----------------------------------------------------------------------------- accent colour
def recolour_themes():
    """Copy each Devium icon theme into your folder with the accent colours in the gradient (undo: the Devium blue)."""
    a, b = accent()
    for name in THEMES:
        if not reset_managed(name):
            continue
        src = os.path.join(SYS_ICONS, name)
        if not os.path.isdir(src) or (a, b) == DEFAULT:
            continue
        dst = user_theme(name)
        os.makedirs(dst, exist_ok=True)
        for sub in ("scalable",):
            if os.path.isdir(os.path.join(src, sub)):
                shutil.copytree(os.path.join(src, sub), os.path.join(dst, sub), symlinks=True, dirs_exist_ok=True)
        for path in glob.glob(os.path.join(dst, "scalable", "*", "*.svg")):
            if os.path.islink(path):
                continue
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            new = re.sub(r'(<stop offset="0" stop-color=")#[0-9a-fA-F]{6}', r"\g<1>" + a, text)
            new = re.sub(r'(<stop offset="1" stop-color=")#[0-9a-fA-F]{6}', r"\g<1>" + b, new)
            if new != text:
                open(path, "w", encoding="utf-8").write(new)
        open(os.path.join(dst, MARK), "w").close()
        write_index(name, False)


# ----------------------------------------------------------------------------- websites installed as apps
def web_apps():
    """[(icon name, site address or "")] for the 'Install as app' shortcuts of Chromium-based browsers."""
    apps = []
    for f in glob.glob(os.path.join(DATA, "applications", "*.desktop")):
        try:
            text = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        entry = text.split("\n[", 1)[0]
        exec_line = re.search(r"^Exec=(.*)$", entry, re.M)
        icon = re.search(r"^Icon=(.*)$", entry, re.M)
        if not exec_line or not icon:
            continue
        cmd = exec_line.group(1)
        if "--app-id=" not in cmd and not re.search(r"--app=https?://", cmd):
            continue
        name = icon.group(1).strip()
        if not name or name.startswith("/"):
            continue
        url = re.search(r"--app=(https?://\S+)", cmd)
        apps.append((name, url.group(1) if url else ""))
    return apps


def find_source(name):
    """The biggest picture the browser saved for this app, or None."""
    best, best_size = None, 0
    pats = [os.path.join(DATA, "icons", "hicolor", "*", "apps", name + ".*"),
            os.path.join(DATA, "icons", name + ".*"),
            os.path.join(HOME, ".local/share/flatpak/exports/share/icons/hicolor", "*", "apps", name + ".*")]
    for pat in pats:
        for p in glob.glob(pat):
            if not p.lower().endswith((".png", ".ico", ".webp", ".jpg", ".jpeg")):
                continue      # SVG sources are skipped (PIL can't draw them); the PNG sizes are enough
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            m = re.search(r"/(\d+)x\d+/", p)
            score = int(m.group(1)) * 1000000 + size if m else size
            if score > best_size:
                best, best_size = p, score
    return best


def fetch_favicon(url):
    """Last resort: the site's own /favicon.ico (one small request to the site you installed)."""
    host = urlparse(url)
    if not host.netloc:
        return None
    try:
        req = urllib.request.Request(f"{host.scheme}://{host.netloc}/favicon.ico", headers={"User-Agent": "Devium icons"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = r.read(2_000_000)
    except Exception:
        return None
    cache = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.join(HOME, ".cache")), "devium", "favicons")
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, hashlib.sha1(host.netloc.encode()).hexdigest() + ".ico")
    with open(path, "wb") as f:
        f.write(data)
    return path


def tile(favicon_path, a, b):
    """The Devium tile (accent gradient, rounded square) with the favicon in the middle, 256 x 256."""
    from PIL import Image, ImageDraw, ImageFilter
    S = 256
    ca = tuple(int(a[i:i + 2], 16) for i in (1, 3, 5))
    cb = tuple(int(b[i:i + 2], 16) for i in (1, 3, 5))
    grad = Image.new("RGBA", (S, S))
    px = grad.load()
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * (S - 1))
            px[x, y] = tuple(int(ca[i] * (1 - t) + cb[i] * t) for i in range(3)) + (255,)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((16, 16, 240, 240), 56, fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((18, 18, 238, 238), 54, outline=(255, 255, 255, 64), width=2)
    fav = Image.open(favicon_path)
    try:                       # .ico files hold several sizes: take the biggest
        if getattr(fav, "ico", None):
            fav = fav.ico.getimage(max(fav.ico.sizes()))
    except Exception:
        pass
    fav = fav.convert("RGBA")
    box = fav.getbbox()
    if box:
        fav = fav.crop(box)
    k = 124 / max(fav.size)
    fav = fav.resize((max(1, int(fav.width * k)), max(1, int(fav.height * k))), Image.LANCZOS)
    pos = ((S - fav.width) // 2, (S - fav.height) // 2)
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shadow.paste((20, 24, 32, 90), (pos[0], pos[1] + 4), fav.getchannel("A"))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(5)))
    out.alpha_composite(fav, pos)
    return out


def web_icons():
    """Give every installed website-app a Devium-style icon (undo: delete ~/.local/share/icons/Devium*/256x256)."""
    try:
        import PIL  # noqa: F401
    except ImportError:
        return
    a, b = accent()
    apps = web_apps()
    for theme in THEMES:
        if not os.path.isdir(os.path.join(SYS_ICONS, theme)):
            continue
        base = user_theme(theme)
        if os.path.isdir(base) and not os.path.isfile(os.path.join(base, MARK)):
            continue          # not our folder
        webdir = os.path.join(base, WEB_DIR)
        shutil.rmtree(webdir, ignore_errors=True)
        made = 0
        for name, url in apps:
            src = find_source(name) or (fetch_favicon(url) if url else None)
            if not src:
                continue
            try:
                img = tile(src, a, b)
            except Exception:
                continue
            os.makedirs(webdir, exist_ok=True)
            img.save(os.path.join(webdir, name + ".png"))
            made += 1
        if made or os.path.isdir(base):
            os.makedirs(base, exist_ok=True)
            open(os.path.join(base, MARK), "w").close()
            write_index(theme, made > 0)
        if not made:
            shutil.rmtree(webdir, ignore_errors=True)
            if os.path.isdir(base) and sorted(os.listdir(base)) in ([MARK, "index.theme"], [MARK]):
                shutil.rmtree(base, ignore_errors=True)       # nothing of ours left in it


def tell_desktop():
    """Ask KDE (and anything that listens) to look at the icons again."""
    subprocess.run(["dbus-send", "--session", "--type=signal", "/KGlobalSettings",
                    "org.kde.KGlobalSettings.notifyChange", "int32:4", "int32:0"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("-h", "--help"):
        print(__doc__)
        return 0
    if what in ("all", "accent"):
        recolour_themes()
    if what in ("all", "webapps"):
        web_icons()
    if what in ("all", "accent", "webapps"):
        try:
            tell_desktop()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
