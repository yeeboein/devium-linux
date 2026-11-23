#!/usr/bin/env python3
"""Devium icons that follow you:

  devium_icons.py all        both of the below (what Devium runs after you change the accent colour, and at login)
  devium_icons.py accent     the Devium app icons use your accent colour (Devium Tools > Look) instead of the blue
  devium_icons.py webapps [-v]  websites installed as apps (Brave, Chrome, Chromium... "Install as app") get their
                             favicon on the Devium gradient (or just the favicon, or left alone: Devium Tools > Look).
                             -v says what it found and wrote

Everything is written to your own folders (~/.local/share/icons), never to the system. Undo: pick the Devium blue again;
for website icons choose "Leave as the browser made them" (the browser's own pictures are kept and put back).
"""
import glob
import hashlib
import json
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
WEB_DIR = "256x256/apps"     # beta19.5 only: cleaned up by web_icons()


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


def write_index(name, with_web=False):
    """Our own index.theme (a copy of the system one)."""
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


WEB_MODE_FILE = os.path.join(CONFIG, "devium", "webapp-icons")
ORIG_DIR = os.path.join(DATA, "devium", "webapp-icons", "orig")
STATE_FILE = os.path.join(DATA, "devium", "webapp-icons", "state.json")
HICOLOR = os.path.join(DATA, "icons", "hicolor")


def web_mode():
    """tile (the favicon on the Devium tile, the default), favicon (just the favicon), or off (leave the browser's icon)."""
    try:
        m = open(WEB_MODE_FILE).read().strip().lower()
    except OSError:
        return "tile"
    return m if m in ("tile", "favicon", "off") else "tile"


def set_web_mode(mode):
    os.makedirs(os.path.dirname(WEB_MODE_FILE), exist_ok=True)
    with open(WEB_MODE_FILE, "w") as f:
        f.write(mode + "\n")


def sha(path):
    try:
        return hashlib.sha1(open(path, "rb").read()).hexdigest()
    except OSError:
        return ""


def browser_icons(name):
    """{size: path} of the icon the browser saved for this app, in your own icon folder (where the menu finds it)."""
    found = {}
    for p in glob.glob(os.path.join(HICOLOR, "*", "apps", name + ".png")):
        m = re.search(r"/(\d+)x\d+/apps/", p)
        if m:
            found[int(m.group(1))] = p
    return found


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


def open_favicon(path):
    """The biggest picture in a favicon file (an .ico holds several), with the empty border cut off, as RGBA."""
    from PIL import Image
    fav = Image.open(path)
    try:
        if getattr(fav, "ico", None):
            fav = fav.ico.getimage(max(fav.ico.sizes()))
    except Exception:
        pass
    fav = fav.convert("RGBA")
    box = fav.getbbox()
    return fav.crop(box) if box else fav


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
    fav = open_favicon(favicon_path)
    k = 124 / max(fav.size)
    fav = fav.resize((max(1, int(fav.width * k)), max(1, int(fav.height * k))), Image.LANCZOS)
    pos = ((S - fav.width) // 2, (S - fav.height) // 2)
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shadow.paste((20, 24, 32, 90), (pos[0], pos[1] + 4), fav.getchannel("A"))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(5)))
    out.alpha_composite(fav, pos)
    return out


def plain(favicon_path):
    """Just the favicon, centred in a transparent square (256 x 256)."""
    from PIL import Image
    S = 256
    fav = open_favicon(favicon_path)
    k = 232 / max(fav.size)
    fav = fav.resize((max(1, int(fav.width * k)), max(1, int(fav.height * k))), Image.LANCZOS)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.alpha_composite(fav, ((S - fav.width) // 2, (S - fav.height) // 2))
    return out


def web_icons(verbose=False):
    """Websites installed as apps: put the favicon on the Devium tile (or just the favicon) in the icon the browser made,
    so the menu, dock and Spotlight all show it. The browser's own picture is kept and put back by "off"."""
    say = print if verbose else (lambda *_a: None)
    # beta19.5 put these in a Devium theme folder, which not every desktop reads: remove that, use the browser's icons
    for theme in THEMES:
        base = user_theme(theme)
        if os.path.isfile(os.path.join(base, MARK)):
            shutil.rmtree(os.path.join(base, "256x256"), ignore_errors=True)
            if os.path.isdir(os.path.join(base, "scalable")):
                write_index(theme, False)
            else:
                shutil.rmtree(base, ignore_errors=True)
    mode = web_mode()
    try:
        import PIL  # noqa: F401
    except ImportError:
        say("The Pillow picture library is missing, so no icons were made.")
        return
    try:
        state = json.load(open(STATE_FILE))
    except (OSError, ValueError):
        state = {}
    a, b = accent()
    apps = web_apps()
    say(f"Mode: {mode}. Websites installed as apps found: {len(apps)}")
    names = set()
    for name, url in apps:
        names.add(name)
        mine = state.setdefault(name, {})
        icons = browser_icons(name)
        os.makedirs(ORIG_DIR, exist_ok=True)
        # what is in the icon folder: ours (we know its checksum) or the browser's (keep a copy as the original)
        for size, path in icons.items():
            if mine.get(str(size)) != sha(path):
                shutil.copy2(path, os.path.join(ORIG_DIR, f"{name}-{size}.png"))
                mine.pop(str(size), None)
        origs = {}
        for f in glob.glob(os.path.join(ORIG_DIR, f"{name}-*.png")):
            m = re.search(r"-(\d+)\.png$", f)
            if m:
                origs[int(m.group(1))] = f
        targets = sorted(origs) if origs else []
        if not origs and url and mode != "off":
            fav = fetch_favicon(url)
            if fav:
                targets = [256]
                origs = {256: fav}
        say(f"  {name}: browser icon sizes {sorted(icons) or 'none'}, using {sorted(origs) or 'nothing'}")
        if not origs:
            say("    no picture found for this app (no icon saved by the browser, no address to fetch a favicon from)")
            continue
        source = origs[max(origs)]
        for size in targets:
            dest = os.path.join(HICOLOR, f"{size}x{size}", "apps", name + ".png")
            if mode == "off":
                if os.path.isfile(origs.get(size, "")) and mine.get(str(size)) == sha(dest):
                    shutil.copy2(origs[size], dest)
                mine.pop(str(size), None)
                continue
            try:
                img = tile(source, a, b) if mode == "tile" else plain(source)
                if size != 256:
                    from PIL import Image
                    img = img.resize((size, size), Image.LANCZOS)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                img.save(dest)
                mine[str(size)] = sha(dest)
                say(f"    wrote {dest}")
            except Exception as e:
                say(f"    could not make the {size} px icon: {e}")
    # apps that are gone: take our icons away (the browser removes its own)
    for name in [n for n in state if n not in names]:
        for size, h in state[name].items():
            dest = os.path.join(HICOLOR, f"{size}x{size}", "apps", name + ".png")
            if sha(dest) == h:
                try:
                    os.remove(dest)
                except OSError:
                    pass
        state.pop(name)
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


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
        web_icons("-v" in sys.argv or "--verbose" in sys.argv)
    if what in ("all", "accent", "webapps"):
        try:
            tell_desktop()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
