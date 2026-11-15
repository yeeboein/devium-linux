#!/usr/bin/env python3
"""Make the Devium folder icons: a folder in the Devium gradient with a white symbol for each special
folder (Documents, Downloads, Music, Projects...). Drawn from scratch here, nothing to download.

Usage:  python3 tools/make-folder-icons.py
Writes: profile/airootfs/usr/share/icons/Devium/scalable/places/  (and the same in Devium-Dark)
Run tools/make-icons.py first if you regenerate everything (it keeps the places folder).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "profile/airootfs/usr/share/icons")
TOP, BOTTOM = "#8fb4d8", "#b4b8e0"          # Devium gradient (front of the folder)
BACK_TOP, BACK_BOTTOM = "#6d92b8", "#8a8fc4"  # a little darker for the back

# Symbols on a 24x24 grid. Lines are drawn as white strokes; "fill:" parts are solid white.
GLYPHS = {
    "plain": "",
    "documents": "M7 3h7l4 4v14H7z|M14 3v4h4|M9.5 12h5|M9.5 15.5h5",
    "download": "M12 4v11|M7.5 10.5 12 15l4.5-4.5|M5 19.5h14",
    "music": "M9 17V6l10-2v11|fill:M7 15a2 2 0 1 0 .01 0z|fill:M17 13a2 2 0 1 0 .01 0z",
    "pictures": "M4 6h16v12H4z|M4 16l5-5 4 4 2-2 5 5|fill:M15.5 8a1.5 1.5 0 1 0 .01 0z",
    "videos": "M4 6h16v12H4z|fill:M10 9v6l5-3z",
    "desktop": "M4 5h16v11H4z|M9 20h6|M12 16v4",
    "home": "M4 11.5 12 4.5l8 7|M6.5 9.5V20h11V9.5|M10 20v-5h4v5",
    "code": "M9 7l-5 5 5 5|M15 7l5 5-5 5|M13.5 5l-3 14",
    "templates": "M5 5h6v6H5z|M13 5h6v6h-6z|M5 13h6v6H5z|M13 13h6v6h-6z",
    "globe": "M12 4a8 8 0 1 0 .01 0z|M4 12h16|M12 4c3 3 3 13 0 16|M12 4c-3 3-3 13 0 16",
    "git": "M7 4a2 2 0 1 0 .01 0z|M7 16a2 2 0 1 0 .01 0z|M17 6a2 2 0 1 0 .01 0z|M7 8v8|M17 10c0 4-6 3-9 6",
    "cloud": "M7 18h10a4 4 0 0 0 .5-8 6 6 0 0 0-11.5 1.5A3.5 3.5 0 0 0 7 18z",
    "star": "M12 4l2.4 5 5.6.6-4.2 3.8 1.2 5.6L12 16.3 7 19l1.2-5.6L4 9.6l5.6-.6z",
    "games": "M7 9h10a3.5 3.5 0 0 1 3.4 4.3l-.8 3.3a2 2 0 0 1-3.5.8L14.5 16h-5l-1.6 1.4a2 2 0 0 1-3.5-.8l-.8-3.3A3.5 3.5 0 0 1 7 9z|M8.5 11.2v3|M7 12.7h3|fill:M15.5 11.5a1 1 0 1 0 .01 0z|fill:M17.5 13.5a1 1 0 1 0 .01 0z",
    "recent": "M12 4a8 8 0 1 0 .01 0z|M12 8v4l3 2",
    "lock": "M7 11h10v9H7z|M9 11V8a3 3 0 0 1 6 0v3",
}

NAMES = {
    "plain": ["folder", "inode-directory", "folder-open", "folder-blue", "folder-grey", "folder-new"],
    "home": ["user-home", "folder-home", "folder-blue-home"],
    "desktop": ["user-desktop", "folder-desktop"],
    "documents": ["folder-documents", "folder-text", "folder-document"],
    "download": ["folder-download", "folder-downloads"],
    "music": ["folder-music", "folder-sound", "folder-audio"],
    "pictures": ["folder-pictures", "folder-images", "folder-image", "folder-photos", "folder-picture"],
    "videos": ["folder-videos", "folder-video", "folder-movies"],
    "templates": ["folder-templates"],
    "globe": ["folder-publicshare", "folder-public", "folder-network", "folder-remote"],
    "code": ["folder-development", "folder-code", "folder-projects", "folder-script", "folder-source"],
    "git": ["folder-git", "folder-github", "folder-gitlab"],
    "cloud": ["folder-cloud", "folder-dropbox", "folder-onedrive", "folder-gdrive", "folder-nextcloud"],
    "star": ["folder-favorites", "folder-bookmark", "folder-important"],
    "games": ["folder-games", "folder-steam"],
    "recent": ["folder-recent"],
    "lock": ["folder-locked", "folder-private", "folder-encrypted"],
}


def glyph_svg(spec):
    if not spec:
        return ""
    parts = []
    for p in spec.split("|"):
        if p.startswith("fill:"):
            parts.append(f'<path d="{p[5:]}" fill="#ffffff" stroke="none"/>')
        else:
            parts.append(f'<path d="{p}"/>')
    # 24-unit symbol -> about 19 px, centred on the front of the folder
    return ('<g transform="translate(20.6 27.6) scale(0.95)" fill="none" stroke="#ffffff" stroke-width="2.3" '
            'stroke-linecap="round" stroke-linejoin="round">'
            # a soft shadow first
            f'<g transform="translate(0 0.8)" stroke="#2b323b" stroke-opacity="0.18">{"".join(parts)}</g>'
            f'{"".join(parts)}</g>')


def folder_svg(kind):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
        '<defs>'
        f'<linearGradient id="f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TOP}"/>'
        f'<stop offset="1" stop-color="{BOTTOM}"/></linearGradient>'
        f'<linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BACK_TOP}"/>'
        f'<stop offset="1" stop-color="{BACK_BOTTOM}"/></linearGradient>'
        '</defs>'
        # back of the folder with its tab
        '<path d="M6 15a5 5 0 0 1 5-5h11.5a3 3 0 0 1 2.1.9l3.6 3.6a3 3 0 0 0 2.1.9H53a5 5 0 0 1 5 5V48H6z" fill="url(#b)"/>'
        # a sheet of paper peeking out
        '<rect x="11" y="17" width="42" height="20" rx="3" fill="#eef2f7" opacity="0.9"/>'
        # shadow under the front
        '<rect x="4" y="23" width="56" height="33" rx="7" fill="#1b2026" opacity="0.18" transform="translate(0 1.5)"/>'
        # the front
        '<rect x="4" y="22" width="56" height="34" rx="7" fill="url(#f)"/>'
        '<rect x="4.5" y="22.5" width="55" height="33" rx="6.5" fill="none" stroke="#ffffff" stroke-opacity="0.35"/>'
        f'{glyph_svg(GLYPHS[kind])}</svg>\n')


def trash_svg(full):
    paper = ('<path d="M24 14l4-6 5 4 4-5 3 7z" fill="#eef2f7" opacity="0.95"/>' if full else "")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
        '<defs><linearGradient id="t" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{TOP}"/><stop offset="1" stop-color="{BOTTOM}"/></linearGradient></defs>'
        f'{paper}'
        '<rect x="12" y="13" width="40" height="7" rx="3.5" fill="url(#t)"/>'
        '<path d="M15 22h34l-2.8 31a4 4 0 0 1-4 3.6H21.8a4 4 0 0 1-4-3.6z" fill="url(#t)"/>'
        '<path d="M15.5 22.5h33" stroke="#ffffff" stroke-opacity="0.35"/>'
        '<g stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" opacity="0.9">'
        '<path d="M25 29v20"/><path d="M32 29v20"/><path d="M39 29v20"/></g>'
        '<rect x="27" y="9" width="10" height="5" rx="2" fill="url(#t)"/></svg>\n')


def write(theme_dir):
    places = os.path.join(theme_dir, "scalable/places")
    shutil.rmtree(places, ignore_errors=True)
    os.makedirs(places)
    count = 0
    for kind, names in NAMES.items():
        first = names[0] + ".svg"
        with open(os.path.join(places, first), "w") as f:
            f.write(folder_svg(kind))
        count += 1
        for n in names[1:]:
            os.symlink(first, os.path.join(places, n + ".svg"))
    for name, full in (("user-trash", False), ("user-trash-full", True)):
        with open(os.path.join(places, name + ".svg"), "w") as f:
            f.write(trash_svg(full))
    os.symlink("user-trash.svg", os.path.join(places, "trashcan_empty.svg"))
    os.symlink("user-trash-full.svg", os.path.join(places, "trashcan_full.svg"))
    return count + 2


def fix_index(theme_dir):
    """Make sure index.theme lists the places folder."""
    p = os.path.join(theme_dir, "index.theme")
    text = open(p).read()
    if "scalable/places" not in text:
        text = text.replace("Directories=scalable/apps", "Directories=scalable/apps,scalable/places")
        text += "\n[scalable/places]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=Places\n"
        open(p, "w").write(text)


def main():
    n = 0
    for theme in ("Devium", "Devium-Dark"):
        d = os.path.join(OUT, theme)
        n = write(d)
        fix_index(d)
    print(f"Made {n} folder icons ({sum(len(v) for v in NAMES.values()) + 4} names) in Devium and Devium-Dark")


if __name__ == "__main__":
    main()
