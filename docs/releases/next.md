# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## Planned
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15 to beta18 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **`lyrics` shows one huge word at a time,** in time with the music ("Hey" ... "This" ... "Is" ... "A" ... "Song"),
  with the line being sung under it and the current word lit up. A big note shows during instrumental breaks.
  `lyrics --lines` gives the classic view. The timing of each word is an estimate.
- **`album-cover` shows the cover as a picture and updates by itself** when the song changes (the ASCII art is gone).
  Real picture in kitty, full-colour blocks in other terminals. `album-cover --once` shows it once.
- **`lyrics` and `album-cover` are options on Devium Configure's Terminal fun page,** off unless you tick them. If you
  already had them, you keep them. The Now playing widget's lyric line works without them.
- **Fixes** for everything beta18 testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Screenshot editor (crop, arrows, blur private details)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
