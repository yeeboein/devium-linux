#!/usr/bin/env python3
"""Make the Devium icon theme: every app icon is a rounded square in the Devium gradient with the
app's logo in white.

Glyph sources (downloaded when you run this; only the finished icons are kept in the repo):
  - Simple Icons (https://simpleicons.org, CC0-1.0): brand logos such as Firefox, Steam, Discord
  - Breeze icons (https://invent.kde.org/frameworks/breeze-icons, LGPL-3.0): KDE's own simple
    symbols for system apps (folder, terminal, settings...)
  - The Devium logo for Devium's own apps

Usage:  python3 tools/make-icons.py [--simple-icons DIR] [--breeze DIR]
Writes: profile/airootfs/usr/share/icons/Devium/  and  .../Devium-Dark/
"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "profile/airootfs/usr/share/icons")
LOGO = os.path.join(ROOT, "profile/airootfs/usr/share/devium/logo-white.png")

# Devium gradient (same as the apps and the theme)
TOP, BOTTOM = "#8fb4d8", "#b4b8e0"

# glyph source -> icon names that use it.  si: = Simple Icons, bz: = Breeze, devium = Devium logo
ICONS = {
    "devium": ["devium", "devium-install", "devium-setup", "devium-tools",
               "devium-updater", "devium-about"],
    # browsers
    "si:firefox": ["firefox", "org.mozilla.firefox"],
    "si:brave": ["brave", "brave-browser", "brave-desktop", "com.brave.Browser", "brave-origin"],
    "si:googlechrome": ["google-chrome", "com.google.Chrome"],
    "si:librewolf": ["librewolf", "io.gitlab.librewolf-community"],
    "si:vivaldi": ["vivaldi", "vivaldi-stable"],
    "bz:actions/16/globe": ["chromium", "helium", "helium-browser", "internet-web-browser",
                            "web-browser"],
    # file managers
    "bz:places/16/folder": ["system-file-manager", "org.kde.dolphin", "dolphin", "thunar",
                            "org.xfce.thunar", "Thunar", "pcmanfm-qt", "pcmanfm", "nemo",
                            "org.gnome.Nautilus", "yazi"],
    # terminals
    "bz:apps/16/utilities-terminal": ["utilities-terminal", "org.kde.konsole", "konsole", "kitty",
                                      "foot", "footclient", "org.xfce.terminal",
                                      "xfce4-terminal", "org.gnome.Console"],
    "si:alacritty": ["Alacritty", "alacritty"],
    "si:ghostty": ["com.mitchellh.ghostty", "ghostty"],
    "si:wezterm": ["org.wezfurlong.wezterm", "wezterm"],
    # editors
    "si:vscodium": ["vscodium", "codium", "com.vscodium.codium"],
    "bz:actions/16/code-context": ["code", "vscode", "visual-studio-code", "com.visualstudio.code",
                                   "code-oss", "com.visualstudio.code.oss"],
    "bz:actions/16/document-edit": ["kate", "org.kde.kate", "kwrite", "org.kde.kwrite",
                                    "accessories-text-editor", "mousepad", "org.xfce.mousepad"],
    "si:neovim": ["nvim", "neovim"],
    # gaming
    "si:steam": ["steam", "com.valvesoftware.Steam"],
    "bz:actions/16/games-config-options": ["net.davidotek.pupgui2", "protonup-qt"],
    "si:wine": ["com.usebottles.bottles", "wine"],
    "si:heroicgameslauncher": ["com.heroicgameslauncher.hgl", "heroic"],
    "si:lutris": ["lutris", "net.lutris.Lutris"],
    # apps
    "si:discord": ["discord", "com.discordapp.Discord"],
    "si:spotify": ["spotify", "spotify-client", "com.spotify.Client"],
    "si:libreoffice": ["libreoffice-startcenter", "libreoffice-writer", "libreoffice-calc",
                       "libreoffice-impress", "libreoffice-draw", "libreoffice-base",
                       "libreoffice-math", "org.libreoffice.LibreOffice",
                       "org.libreoffice.LibreOffice.startcenter", "org.libreoffice.LibreOffice.writer",
                       "org.libreoffice.LibreOffice.calc", "org.libreoffice.LibreOffice.impress"],
    "si:gimp": ["gimp", "org.gimp.GIMP"],
    "si:obsstudio": ["obs", "com.obsproject.Studio"],
    "si:thunderbird": ["thunderbird", "org.mozilla.Thunderbird"],
    "si:vlcmediaplayer": ["vlc", "org.videolan.VLC"],
    "bz:actions/16/media-playback-start": ["multimedia-video-player", "org.kde.haruna", "mpv"],
    "si:krita": ["krita", "org.kde.krita"],
    "si:kdenlive": ["kdenlive", "org.kde.kdenlive"],
    "si:telegram": ["telegram", "org.telegram.desktop"],
    "si:obsidian": ["obsidian", "md.obsidian.Obsidian"],
    "si:inkscape": ["inkscape", "org.inkscape.Inkscape"],
    "si:blender": ["blender", "org.blender.Blender"],
    "si:ollama": ["com.jeffser.Alpaca", "ollama"],
    "si:github": ["github-desktop", "io.github.shiftey.Desktop"],
    # KDE / system apps
    "bz:actions/16/package": ["plasmadiscover", "org.kde.discover", "system-software-install",
                              "octopi", "pamac"],
    "bz:devices/16/camera-photo": ["spectacle", "org.kde.spectacle", "applets-screenshooter",
                                   "org.xfce.screenshooter", "accessories-screenshot"],
    "bz:actions/16/configure": ["preferences-system", "systemsettings", "org.kde.systemsettings",
                                "xfce4-settings-manager", "org.xfce.settings.manager"],
    "bz:actions/16/speedometer": ["utilities-system-monitor", "org.kde.plasma-systemmonitor",
                                  "plasma-systemmonitor", "org.xfce.taskmanager", "htop", "btop"],
    "bz:actions/16/archive-extract": ["ark", "org.kde.ark", "file-roller", "xarchiver"],
    "bz:mimetypes/16/image-x-generic": ["gwenview", "org.kde.gwenview", "ristretto",
                                        "org.xfce.ristretto", "image-viewer"],
    "bz:actions/16/document-preview": ["okular", "org.kde.okular", "atril", "evince"],
    "bz:actions/16/system-search": ["krunner", "org.kde.krunner", "catfish"],
    "bz:actions/16/help-about": ["help-browser", "org.kde.kinfocenter", "kinfocenter",
                                 "help-about", "khelpcenter", "org.kde.khelpcenter"],
    "bz:actions/16/view-media-playlist": ["elisa", "org.kde.elisa", "audacious", "rhythmbox"],
}


def fetch_simple_icons(dest):
    meta = json.load(urllib.request.urlopen("https://registry.npmjs.org/simple-icons/latest"))
    data = urllib.request.urlopen(meta["dist"]["tarball"]).read()
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        members = [m for m in t.getmembers() if m.name.startswith("package/icons/")]
        t.extractall(dest, members=members, filter="data")
    return os.path.join(dest, "package/icons")


def fetch_breeze(dest):
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                    "https://github.com/KDE/breeze-icons.git", dest], check=True)
    subprocess.run(["git", "-C", dest, "sparse-checkout", "set", "icons/actions/16", "icons/apps/16",
                    "icons/places/16", "icons/mimetypes/16", "icons/devices/16"], check=True)
    return os.path.join(dest, "icons")


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
SHAPES = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "g"}


def strip_colour(el):
    """Make a Breeze shape plain (no colour classes), keeping see-through parts."""
    style = el.attrib.pop("style", "")
    el.attrib.pop("class", None)
    el.attrib.pop("color", None)
    fill = el.attrib.pop("fill", "")
    if "fill:none" in style.replace(" ", "") or fill == "none":
        el.set("fill", "none")
    m = re.search(r"(?:fill-)?opacity:\s*([\d.]+)", style)
    if m:
        el.set("opacity", m.group(1))
    for child in list(el):
        tag = child.tag.split("}")[-1]
        if tag in SHAPES:
            strip_colour(child)
        else:
            el.remove(child)


def breeze_glyph(path):
    root = ET.parse(path).getroot()
    vb = [float(x) for x in root.get("viewBox", "0 0 16 16").split()]
    parts = []
    for child in root:
        tag = child.tag.split("}")[-1]
        if tag in SHAPES:
            strip_colour(child)
            parts.append(ET.tostring(child, encoding="unicode"))
    inner = "".join(parts).replace(f' xmlns="{SVG_NS}"', "")
    return inner, vb[2]


def simple_glyph(path):
    root = ET.parse(path).getroot()
    d = root.find(f"{{{SVG_NS}}}path").get("d")
    return f'<path d="{d}"/>', 24.0


def devium_glyph():
    from PIL import Image
    im = Image.open(LOGO).convert("RGBA")
    im.thumbnail((192, 192), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return b64


def icon_svg(glyph, size, logo_png=None):
    """64x64 rounded square, Devium gradient, white glyph about half the size, soft shadow."""
    g = 34.0                       # glyph box size
    off = (64 - g) / 2
    if logo_png:
        art = (f'<image x="{off - 1}" y="{off - 1}" width="{g + 2}" height="{g + 2}" '
               f'xlink:href="data:image/png;base64,{logo_png}"/>')
        shadow = ""
    else:
        s = g / size
        shadow = (f'<g transform="translate({off} {off + 1.2}) scale({s:.4f})" fill="#2b323b" '
                  f'opacity="0.22">{glyph}</g>')
        art = f'<g transform="translate({off} {off}) scale({s:.4f})" fill="#ffffff">{glyph}</g>'
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="64" height="64" viewBox="0 0 64 64">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{TOP}"/><stop offset="1" stop-color="{BOTTOM}"/>'
        '</linearGradient></defs>'
        '<rect x="4" y="4" width="56" height="56" rx="14" ry="14" fill="url(#g)"/>'
        '<rect x="4.5" y="4.5" width="55" height="55" rx="13.5" ry="13.5" fill="none" '
        'stroke="#ffffff" stroke-opacity="0.25"/>'
        f'{shadow}{art}</svg>\n')


INDEX = """[Icon Theme]
Name={name}
Comment=Devium app icons: the Devium gradient with each app's logo in white
Inherits={inherits}
Example=devium
Directories=scalable/apps

[scalable/apps]
Size=64
MinSize=16
MaxSize=512
Type=Scalable
Context=Applications
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--simple-icons")
    ap.add_argument("--breeze")
    a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="devium-icons-")
    si = a.simple_icons or fetch_simple_icons(os.path.join(tmp, "si"))
    bz = a.breeze or fetch_breeze(os.path.join(tmp, "bz"))

    apps = os.path.join(OUT, "Devium/scalable/apps")
    os.makedirs(apps, exist_ok=True)
    for f in os.listdir(apps):
        os.remove(os.path.join(apps, f))
    logo = devium_glyph()
    made = 0
    for src, names in ICONS.items():
        if src == "devium":
            svg = icon_svg(None, 0, logo)
        elif src.startswith("si:"):
            svg = icon_svg(*simple_glyph(os.path.join(si, src[3:] + ".svg")))
        else:
            # prefer Breeze's plain one-colour ("symbolic") version when there is one
            sym = os.path.join(bz, src[3:] + "-symbolic.svg")
            svg = icon_svg(*breeze_glyph(sym if os.path.exists(sym) else os.path.join(bz, src[3:] + ".svg")))
        first = names[0] + ".svg"
        with open(os.path.join(apps, first), "w") as f:
            f.write(svg)
        made += 1
        for n in names[1:]:   # other names for the same app point at the same picture
            os.symlink(first, os.path.join(apps, n + ".svg"))
    with open(os.path.join(OUT, "Devium/index.theme"), "w") as f:
        f.write(INDEX.format(name="Devium", inherits="breeze,Papirus,Adwaita,hicolor"))
    dark = os.path.join(OUT, "Devium-Dark")
    os.makedirs(dark, exist_ok=True)
    # a real copy (not a folder symlink, which some icon caches don't follow after a restart)
    import shutil
    target = os.path.join(dark, "scalable")
    if os.path.islink(target):
        os.remove(target)
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(os.path.join(OUT, "Devium/scalable"), target, symlinks=True)
    with open(os.path.join(dark, "index.theme"), "w") as f:
        f.write(INDEX.format(name="Devium Dark", inherits="breeze-dark,Papirus-Dark,Adwaita,hicolor"))
    total = sum(len(v) for v in ICONS.values())
    print(f"Made {made} icons ({total} app names) in {OUT}/Devium and Devium-Dark")


if __name__ == "__main__":
    sys.exit(main())
