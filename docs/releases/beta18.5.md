# Devium beta18.5

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. A small update to beta18: `lyrics` and `album-cover` redone, and both are now options on Devium Configure's Terminal fun page.

## Updating from beta18
**The Updater in beta18 can't see this update** (it reads "beta18.5" as "beta18"; fixed from now on), so update once from
the terminal. Your files and apps stay:

```bash
pkexec /usr/lib/devium/devium-helper refresh beta18.5
```

Then log out and back in. From beta17 or earlier, the Update Devium button in Devium Updater works as usual (or run the
same command).

## New
- **`lyrics` shows one huge word at a time,** in time with the music ("Hey" ... "This" ... "Is" ... "A" ... "Song"). The
  line being sung is under it with the current word lit up, and a big note shows during instrumental breaks.
  `lyrics --lines` gives the classic view, `lyrics --once` prints the whole lyrics. The words' timing is an estimate,
  because lyrics are timed per line, so a word can be slightly off the beat.
- **`album-cover` shows the cover as a picture and updates by itself** when the song changes. In kitty you get the real
  picture; in other terminals (Konsole, Xfce Terminal) the cover is drawn in full-colour blocks. The ASCII art is gone.
  `album-cover --once` shows it one time.
- **`lyrics` and `album-cover` are options on Devium Configure's Terminal fun page,** off unless you tick them. If you
  already had them, you keep them (and get the new versions). The Now playing widget's lyric line works without them.

## Fixed
- **Devium Updater** now understands versions with a dot, like beta18.5, so it offers them correctly from now on.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
