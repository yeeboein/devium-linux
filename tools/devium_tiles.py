"""Shapes drawn from scratch for the Devium icon theme, in the same style as the app icons: a rounded square
in the Devium gradient with a white shape on it. Folders and files have their symbol cut into the shape.
Used by tools/make-folder-icons.py (folders, files, trash) and tools/make-icons.py (file managers)."""
TOP, BOTTOM = "#8fb4d8", "#b4b8e0"
CUT = "#9fb4dc"        # the symbol is "cut out" of the white shape in the tile's own colour

# 24x24 symbols (same set as the folders), stroked
SYM = {
    "plain": "",
    "documents": "M8 7.5h8|M8 11h8|M8 14.5h5",
    "download": "M12 5v9|M8.5 10.5 12 14l3.5-3.5|M7.5 17.5h9",
    "music": "M10 16V7l7-1.5v9|fill:M8.5 14.5a1.6 1.6 0 1 0 .01 0z|fill:M15.5 13a1.6 1.6 0 1 0 .01 0z",
    "pictures": "M6 7h12v10H6z|M6 15l4-4 3 3 1.5-1.5 3.5 3.5|fill:M14.5 9.2a1.2 1.2 0 1 0 .01 0z",
    "videos": "M6 7h12v10H6z|fill:M10.5 9.5v5l4-2.5z",
    "desktop": "M6 6.5h12v8.5H6z|M10 18.5h4|M12 15v3.5",
    "home": "M6 12 12 6.5l6 5.5|M7.8 10.5V17.5h8.4V10.5|M10.6 17.5v-3.5h2.8v3.5",
    "code": "M9.5 8.5 6 12l3.5 3.5|M14.5 8.5 18 12l-3.5 3.5|M13 7l-2 10",
    "templates": "M6.5 6.5h4.5v4.5H6.5z|M13 6.5h4.5v4.5H13z|M6.5 13h4.5v4.5H6.5z|M13 13h4.5v4.5H13z",
    "globe": "M12 5.5a6.5 6.5 0 1 0 .01 0z|M5.5 12h13|M12 5.5c2.4 2.4 2.4 10.6 0 13|M12 5.5c-2.4 2.4-2.4 10.6 0 13",
    "git": "M8.5 6a1.6 1.6 0 1 0 .01 0z|M8.5 16a1.6 1.6 0 1 0 .01 0z|M15.5 7.5a1.6 1.6 0 1 0 .01 0z|M8.5 9.2v5.2|M15.5 9.1c0 3.4-4.4 2.4-6.4 5",
    "cloud": "M8.5 16.5h7.5a3 3 0 0 0 .4-6 4.5 4.5 0 0 0-8.6 1.2 2.6 2.6 0 0 0 .7 4.8z",
    "star": "M12 6l1.8 3.8 4.2.5-3.1 2.8.9 4.1L12 15.2l-3.8 2 .9-4.1L6 10.3l4.2-.5z",
    "games": "M8.5 9.5h7a2.8 2.8 0 0 1 2.7 3.4l-.6 2.5a1.5 1.5 0 0 1-2.6.6L13.8 15h-3.6L9 16a1.5 1.5 0 0 1-2.6-.6l-.6-2.5a2.8 2.8 0 0 1 2.7-3.4z|M9.4 11.3v2.4|M8.2 12.5h2.4",
    "recent": "M12 5.5a6.5 6.5 0 1 0 .01 0z|M12 8.5v3.5l2.5 1.6",
    "lock": "M8 11h8v6.5H8z|M9.8 11V9a2.2 2.2 0 0 1 4.4 0v2",
    # file types
    "text": "M8.5 9h7|M8.5 12h7|M8.5 15h4.5",
    "pdf": "",          # drawn as text
    "sheet": "M7.5 8.5h9v8h-9z|M7.5 11.2h9|M7.5 13.9h9|M10.5 8.5v8",
    "slides": "M7 8.5h10v6.5H7z|M12 15v2.5|M10 17.5h4",
    "zip": "M12 6v2|M12 9v2|M12 12v2|M10.5 14.5h3v3h-3z",
    "disc": "M12 6a6 6 0 1 0 .01 0z|fill:M12 10.6a1.4 1.4 0 1 0 .01 0z",
    "terminal": "M7.5 9.5 10.5 12l-3 2.5|M12 15.5h4.5",
    "package": "M12 6.5l5.5 2.8v5.6L12 17.7l-5.5-2.8V9.3z|M6.5 9.3 12 12l5.5-2.7|M12 12v5.7",
    "font": "",         # drawn as text
}

FOLDER_NAMES = {
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

FILE_NAMES = {   # freedesktop mimetype icon names
    "text": ["text-x-generic", "text-plain", "application-x-zerosize", "unknown", "application-octet-stream",
             "text-markdown", "text-x-readme"],
    "documents": ["x-office-document", "application-vnd.oasis.opendocument.text", "application-msword",
                  "application-vnd.openxmlformats-officedocument.wordprocessingml.document", "application-rtf"],
    "pdf": ["application-pdf", "application-x-pdf"],
    "sheet": ["x-office-spreadsheet", "application-vnd.oasis.opendocument.spreadsheet", "text-csv",
              "application-vnd.ms-excel", "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "slides": ["x-office-presentation", "application-vnd.oasis.opendocument.presentation",
               "application-vnd.ms-powerpoint", "application-vnd.openxmlformats-officedocument.presentationml.presentation"],
    "pictures": ["image-x-generic", "image-png", "image-jpeg", "image-gif", "image-webp", "image-svg+xml", "image-bmp"],
    "videos": ["video-x-generic", "video-mp4", "video-x-matroska", "video-webm", "video-quicktime"],
    "music": ["audio-x-generic", "audio-mpeg", "audio-flac", "audio-ogg", "audio-x-wav", "audio-mp4"],
    "zip": ["package-x-generic", "application-zip", "application-x-tar", "application-x-compressed-tar",
            "application-x-7z-compressed", "application-x-rar", "application-gzip", "application-x-xz-compressed-tar",
            "application-x-zstd-compressed-tar"],
    "disc": ["application-x-cd-image", "application-x-iso9660-image", "application-x-raw-disk-image"],
    "code": ["text-x-script", "text-x-python", "text-x-csrc", "text-x-c++src", "text-x-chdr", "text-x-java",
             "text-x-rust", "text-x-go", "application-javascript", "text-javascript", "application-json",
             "text-html", "text-css", "application-x-yaml", "text-x-makefile", "application-xml", "text-x-lua"],
    "terminal": ["application-x-shellscript", "text-x-sh", "application-x-executable", "application-x-sharedlib"],
    "package": ["application-x-rpm", "application-vnd.debian.binary-package", "application-x-archlinux-package",
                "application-vnd.flatpak.ref", "application-x-appimage"],
    "font": ["font-x-generic", "application-x-font-ttf", "font-ttf", "font-otf", "application-x-font-otf"],
}


def _symbol(kind, color, scale, tx, ty, width=2.4):
    spec = SYM.get(kind, "")
    if not spec:
        return ""
    parts = []
    for p in spec.split("|"):
        if p.startswith("fill:"):
            parts.append(f'<path d="{p[5:]}" fill="{color}" stroke="none"/>')
        else:
            parts.append(f'<path d="{p}"/>')
    return (f'<g transform="translate({tx} {ty}) scale({scale})" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</g>')


def _tile(inner):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{TOP}"/><stop offset="1" stop-color="{BOTTOM}"/></linearGradient></defs>'
            '<rect x="4" y="4" width="56" height="56" rx="14" ry="14" fill="url(#g)"/>'
            '<rect x="4.5" y="4.5" width="55" height="55" rx="13.5" ry="13.5" fill="none" stroke="#ffffff" stroke-opacity="0.25"/>'
            f'{inner}</svg>\n')


def folder_svg(kind):
    """A white folder on the Devium tile, with the symbol cut into it."""
    shadow = ('<path d="M15 21.5a3 3 0 0 1 3-3h8l3 3h17a3 3 0 0 1 3 3V45a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3z" '
              'fill="#2b323b" opacity="0.18" transform="translate(0 1.3)"/>')
    folder = ('<path d="M15 21.5a3 3 0 0 1 3-3h8l3 3h17a3 3 0 0 1 3 3V45a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3z" fill="#ffffff"/>'
              '<path d="M15 26h34" stroke="#2b323b" stroke-opacity="0.10" stroke-width="1.2"/>')
    return _tile(shadow + folder + _symbol(kind, CUT, 0.98, 20.2, 22.4, 2.3))


def file_svg(kind):
    """A white page with a folded corner on the Devium tile, with the symbol cut into it."""
    page = "M21 13h15l8 8v28a2.5 2.5 0 0 1-2.5 2.5h-20.5a2.5 2.5 0 0 1-2.5-2.5V15.5a2.5 2.5 0 0 1 2.5-2.5z"
    shadow = f'<path d="{page}" fill="#2b323b" opacity="0.18" transform="translate(0 1.3)"/>'
    body = f'<path d="{page}" fill="#ffffff"/><path d="M36 13v6.5a1.5 1.5 0 0 0 1.5 1.5H44" fill="{CUT}" opacity="0.55"/>'
    if kind in ("pdf", "font"):
        label = "PDF" if kind == "pdf" else "Aa"
        sym = (f'<text x="32" y="{40 if kind == "pdf" else 41}" text-anchor="middle" font-family="Inter, Noto Sans, sans-serif" '
               f'font-weight="800" font-size="{10 if kind == "pdf" else 13}" fill="{CUT}">{label}</text>')
    else:
        sym = _symbol(kind, CUT, 0.9, 21.2, 22.2, 2.4)
    return _tile(shadow + body + sym)


def trash_svg(full):
    can = ('<path d="M22 24h20l-1.8 21a2.5 2.5 0 0 1-2.5 2.3H26.3a2.5 2.5 0 0 1-2.5-2.3z" fill="#ffffff"/>'
           '<rect x="19.5" y="19.5" width="25" height="4.5" rx="2.2" fill="#ffffff"/>'
           '<rect x="28" y="16.5" width="8" height="3.5" rx="1.5" fill="#ffffff"/>'
           f'<g stroke="{CUT}" stroke-width="2.2" stroke-linecap="round"><path d="M28 28.5v14"/><path d="M32 28.5v14"/><path d="M36 28.5v14"/></g>')
    paper = '<path d="M25 19l3-5 4 3.2 3.5-4 2.5 5.8z" fill="#ffffff" opacity="0.9"/>' if full else ""
    return _tile(paper + can)


# --- app icons drawn here (no outside glyph) --------------------------------------------------------------
def file_manager_svg():
    """Other file managers: a folder with a magnifying glass (an app, not a folder)."""
    f = "M14 21.5a3 3 0 0 1 3-3h8l3 3h15a3 3 0 0 1 3 3V41a3 3 0 0 1-3 3H17a3 3 0 0 1-3-3z"
    return _tile(f'<path d="{f}" fill="#2b323b" opacity="0.18" transform="translate(0 1.2)"/>'
                 f'<path d="{f}" fill="#ffffff"/>'
                 '<circle cx="40" cy="40" r="8.5" fill="url(#g)" stroke="#ffffff" stroke-width="3.2"/>'
                 '<path d="M46.2 46.2 51 51" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>')


CUSTOM_APPS = {"filemanager": file_manager_svg}
