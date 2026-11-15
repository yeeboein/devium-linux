#!/usr/bin/env python3
"""Make the Devium folder and file icons, drawn like the app icons: a rounded square in the Devium gradient
with a white folder (or page) and the symbol (Documents, Downloads, Music, PDF, code...) cut into it.
Drawn from scratch in tools/devium_tiles.py, nothing to download.

Usage:  python3 tools/make-folder-icons.py
Writes: profile/airootfs/usr/share/icons/Devium/scalable/places/  and  .../scalable/mimetypes/
        (and the same in Devium-Dark). It also redraws the file manager app icons.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import devium_tiles as T  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "profile/airootfs/usr/share/icons")

# Dolphin and system-file-manager (the icon name Dolphin's menu entry uses) aren't here on purpose:
# they keep KDE's own Dolphin icon (the theme falls back to Breeze)
APP_NAMES = {
    "filemanager": ["thunar", "org.xfce.thunar", "Thunar", "pcmanfm-qt", "pcmanfm",
                    "nemo", "org.gnome.Nautilus", "yazi"],
}


def write_set(folder, table, draw):
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
    made = 0
    for kind, names in table.items():
        first = names[0] + ".svg"
        with open(os.path.join(folder, first), "w") as f:
            f.write(draw(kind))
        made += 1
        for n in names[1:]:
            os.symlink(first, os.path.join(folder, n + ".svg"))
    return made


def write(theme_dir):
    places = os.path.join(theme_dir, "scalable/places")
    n = write_set(places, T.FOLDER_NAMES, T.folder_svg)
    for name, full in (("user-trash", False), ("user-trash-full", True)):
        with open(os.path.join(places, name + ".svg"), "w") as f:
            f.write(T.trash_svg(full))
    os.symlink("user-trash.svg", os.path.join(places, "trashcan_empty.svg"))
    os.symlink("user-trash-full.svg", os.path.join(places, "trashcan_full.svg"))
    n += 2 + write_set(os.path.join(theme_dir, "scalable/mimetypes"), T.FILE_NAMES, T.file_svg)
    # the other file manager apps get a folder with a magnifier; Dolphin's Devium icon is removed
    for name in ("org.kde.dolphin", "dolphin", "system-file-manager"):
        p = os.path.join(theme_dir, "scalable/apps", name + ".svg")
        if os.path.lexists(p):
            os.remove(p)
    apps = os.path.join(theme_dir, "scalable/apps")
    if os.path.isdir(apps):
        for kind, names in APP_NAMES.items():
            for i, name in enumerate(names):
                p = os.path.join(apps, name + ".svg")
                if os.path.lexists(p):
                    os.remove(p)
                if i == 0:
                    with open(p, "w") as f:
                        f.write(T.CUSTOM_APPS[kind]())
                else:
                    os.symlink(names[0] + ".svg", p)
    return n


SECTIONS = {
    "scalable/places": "Places",
    "scalable/mimetypes": "MimeTypes",
}


def fix_index(theme_dir):
    """Make sure index.theme lists the places and mimetypes folders."""
    p = os.path.join(theme_dir, "index.theme")
    lines = open(p).read().splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Directories="):
            dirs = line.split("=", 1)[1].split(",")
            for d in SECTIONS:
                if d not in dirs:
                    dirs.append(d)
            lines[i] = "Directories=" + ",".join(dirs)
    text = "\n".join(lines) + "\n"
    for d, ctx in SECTIONS.items():
        if f"[{d}]" not in text:
            text += f"\n[{d}]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext={ctx}\n"
    open(p, "w").write(text)


def main():
    n = 0
    for theme in ("Devium", "Devium-Dark"):
        d = os.path.join(OUT, theme)
        n = write(d)
        fix_index(d)
    names = sum(len(v) for v in T.FOLDER_NAMES.values()) + sum(len(v) for v in T.FILE_NAMES.values()) + 4
    print(f"Made {n} folder and file icons ({names} names) in Devium and Devium-Dark")


if __name__ == "__main__":
    main()
