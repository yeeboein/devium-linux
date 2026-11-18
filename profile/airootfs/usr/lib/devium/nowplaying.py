"""What's playing right now, from any music player (Spotify, Firefox, Brave, VLC, Elisa...), using the standard
MPRIS interface over D-Bus via busctl (part of systemd, so nothing extra to install). Used by `lyrics` and
`album-cover`."""
import json
import subprocess

PATH = "/org/mpris/MediaPlayer2"
IFACE = "org.mpris.MediaPlayer2.Player"


def _busctl(*args):
    try:
        out = subprocess.run(["busctl", "--user", "--json=short", *args], capture_output=True, text=True, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    try:
        return json.loads(out.stdout)
    except ValueError:
        return None


def players():
    r = _busctl("call", "org.freedesktop.DBus", "/org/freedesktop/DBus", "org.freedesktop.DBus", "ListNames")
    names = r["data"][0] if r and r.get("data") else []
    return [n for n in names if n.startswith("org.mpris.MediaPlayer2.")]


def _prop(player, name):
    r = _busctl("get-property", player, PATH, IFACE, name)
    return r.get("data") if r else None


def _val(v):
    """busctl wraps variants as {"type": ..., "data": ...}."""
    while isinstance(v, dict) and "data" in v and "type" in v:
        v = v["data"]
    return v


def current():
    """The player that's playing (or the first paused one): dict with player, status, title, artist, album,
    length and position in seconds, art (URL) and id. None when nothing is playing."""
    best = None
    for p in players():
        status = _val(_prop(p, "PlaybackStatus")) or ""
        if status not in ("Playing", "Paused"):
            continue
        meta = _val(_prop(p, "Metadata")) or {}
        meta = {k: _val(v) for k, v in meta.items()} if isinstance(meta, dict) else {}
        title = meta.get("xesam:title") or ""
        if not title:
            continue
        artist = meta.get("xesam:artist") or ""
        if isinstance(artist, list):
            artist = ", ".join(str(a) for a in artist)
        info = {
            "player": p.split(".")[3] if p.count(".") >= 3 else p,
            "bus": p,
            "status": status,
            "title": str(title),
            "artist": str(artist),
            "album": str(meta.get("xesam:album") or ""),
            "length": (meta.get("mpris:length") or 0) / 1_000_000,
            "art": str(meta.get("mpris:artUrl") or ""),
            "id": str(meta.get("mpris:trackid") or f"{artist}|{title}"),
        }
        info["position"] = (_val(_prop(p, "Position")) or 0) / 1_000_000
        if status == "Playing":
            return info
        best = best or info
    return best


def control(action):
    """Play/pause, next or previous on the player that's playing (or the first one that has a song)."""
    method = {"playpause": "PlayPause", "next": "Next", "previous": "Previous"}.get(action)
    if not method:
        return False
    song = current()
    bus = song["bus"] if song else (players() or [None])[0]
    if not bus:
        return False
    try:
        return subprocess.run(["busctl", "--user", "call", bus, PATH, IFACE, method], capture_output=True,
                              timeout=3).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
