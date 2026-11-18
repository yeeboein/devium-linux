"""Lyrics lookup (LRCLIB, lrclib.net: free, no account) with a local cache. Shared by the `lyrics` command and the
Now playing widget. Only the song's title, artist, album and length are sent to the site."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "devium", "lyrics")
UA = "Devium lyrics (https://github.com/yeeboein/devium-linux)"


def key(song):
    return hashlib.sha1(f"{song['artist']}|{song['title']}|{song['album']}".lower().encode()).hexdigest()


def _path(song):
    return os.path.join(CACHE, key(song) + ".json")


def parse_lrc(text):
    """"[01:23.45] words" lines -> sorted [(seconds, words), ...] or None."""
    lines = []
    for raw in (text or "").splitlines():
        stamps = re.findall(r"\[(\d+):(\d+(?:\.\d+)?)\]", raw)
        words = re.sub(r"\[[^\]]*\]", "", raw).strip()
        for m, s in stamps:
            lines.append((int(m) * 60 + float(s), words))
    lines.sort()
    return lines or None


def _process(raw):
    """What LRCLIB sent -> {"synced": [(t, words)...] | None, "plain": str | None, "instrumental": bool}."""
    raw = raw or {}
    return {"synced": parse_lrc(raw.get("syncedLyrics") or ""), "plain": raw.get("plainLyrics"),
            "instrumental": bool(raw.get("instrumental"))}


def cached(song):
    """The saved answer for this song, or None if we haven't looked it up yet."""
    try:
        data = json.load(open(_path(song)))
    except (OSError, ValueError):
        return None
    if data.get("synced"):
        data["synced"] = [tuple(x) for x in data["synced"]]
    return data


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def _ask(song):
    """LRCLIB's raw answer, {} when it doesn't know the song, or None when it can't be reached."""
    q = {"artist_name": song["artist"], "track_name": song["title"]}
    if song["album"]:
        q["album_name"] = song["album"]
    if song["length"]:
        q["duration"] = int(round(song["length"]))
    try:
        return _get("https://lrclib.net/api/get?" + urllib.parse.urlencode(q))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return None
    except Exception:
        return None
    try:   # not an exact match: search instead, closest length first
        results = _get("https://lrclib.net/api/search?" + urllib.parse.urlencode(
            {"track_name": song["title"], "artist_name": song["artist"]}))
    except Exception:
        return None
    if not results:
        return {}
    length = song["length"] or 0
    results.sort(key=lambda r: (not r.get("syncedLyrics"), abs((r.get("duration") or 0) - length)))
    return results[0]


def fetch(song):
    """The lyrics for this song (looked up once, then kept), or None when the site can't be reached."""
    data = cached(song)
    if data is not None:
        return data
    raw = _ask(song)
    if raw is None:
        return None
    data = _process(raw)
    os.makedirs(CACHE, exist_ok=True)
    with open(_path(song), "w") as f:
        json.dump(data, f)
    return data


def prefetch_in_background(song, retry_after=90):
    """Start a lookup that doesn't block (used by the widget); not again within retry_after seconds."""
    marker = os.path.join(CACHE, "pending-" + key(song))
    try:
        if time.time() - os.path.getmtime(marker) < retry_after:
            return
    except OSError:
        pass
    exe = shutil.which("lyrics") or "/usr/local/bin/lyrics"
    if not os.path.exists(exe):
        return
    os.makedirs(CACHE, exist_ok=True)
    open(marker, "w").close()
    subprocess.Popen([sys.executable, exe, "--prefetch"], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


def window(synced, position, before=1, after=5):
    """A few lines around "now" for a widget: [{"t": seconds, "w": words}, ...] (the current line is the last one
    with t <= position)."""
    cur = -1
    for i, (t, _w) in enumerate(synced):
        if t <= position + 0.25:
            cur = i
    start = max(0, cur - before)
    return [{"t": round(t, 2), "w": w} for t, w in synced[start:start + before + after + 1]]
