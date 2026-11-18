# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## Planned
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15, beta16 and beta17 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **fastfetch always side by side:** the Devium logo always sits next to your info, whatever the window size
  (no more logo on top in narrow windows).
- **Apps open where you left them** (KDE): each app's window size and position are remembered when you close it,
  and maximised apps open maximised. Turn it off in Customise ("Don't remember where windows were").
- **The top edge of new windows can always be grabbed:** new windows open in the middle of the screen instead of
  touching the top, where the resize edge was half off-screen.
- **Home screen pages removed:** if you had them on, they're taken off your desktop when you update.
- **Automatic tiling no longer overlaps windows:** apps that resize themselves just after opening (browsers,
  terminals, Electron apps) are put back in their tile, and tiling now wins over "remember where windows were".
- **`lyrics` in the terminal:** shows the words to whatever song is playing (Spotify, your browser, VLC and more),
  with the current line lit up as the song plays, and it moves on to the next song by itself. `lyrics --once` prints
  them. Lyrics come from LRCLIB (free, only the song's name and artist are sent).
- **`album-cover` in the terminal:** draws the playing song's cover in colour, or as ASCII art with `--ascii`.
- **Pictures stay solid in see-through mode:** with "See-through all the time", photo viewers and image editors
  (Gwenview, Okular, GIMP, Krita and others) are no longer see-through, so pictures look right. Tick "Keep pictures
  see-through too" in Customise if you like them see-through.
- **New wallpaper:** a snowy mountain peak with the Devium logo, on the desktop, login screen and installer.
- **Fixes** for everything beta17 testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Screenshot editor (crop, arrows, blur private details)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
