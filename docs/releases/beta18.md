# Devium beta18

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. New wallpapers and lock screen pictures, a Now playing widget, a screenshot editor, and terminal tools for music and notes.

## New
- **New wallpaper:** a snowy mountain peak with the Devium logo on the desktop. The lock screen and login screen use the
  same photo without the logo, so the clock and sign-in card are easier to read.
- **Choose your own desktop and lock screen pictures,** separately, each with "Use Devium's" to go back. The lock screen
  picture can also be used on the login screen. Find it in System Settings > Appearance > **Lock Screen Wallpaper**
  (right under Wallpaper), the new **Wallpapers** app, or Devium Tools > Look. KDE, Xfce and Hyprland.
- **Now playing widget** (KDE, Xfce, Hyprland): the cover, title, artist, a progress bar, the lyric line being sung, and
  play/pause/next/previous buttons. Works with Spotify, your browser, VLC and other players. Add it from right-click
  desktop > Add Widgets (KDE) or Devium Tools > Look > Devium widgets.
- **Screenshot Editor** (`devium-shot`, or Meta+Ctrl+S): take a screenshot of an area, the whole screen or a window, then
  crop it, draw arrows and boxes, highlight, add text, and **hide private details** (passwords, emails, your IP
  address) behind big blocks. Copy it, or save it to Pictures/Screenshots. Also edits any picture or the one on your
  clipboard.
- **`lyrics` in the terminal:** the words to whatever song is playing, with the current line lit up as it plays, moving on
  to the next song by itself. `lyrics --once` prints them. Lyrics come from LRCLIB (free; only the song's name and
  artist are sent).
- **`album-cover` in the terminal:** draws the playing song's cover in colour, or as ASCII art with `--ascii`.
- **`note` in the terminal:** quick notes. `note "buy milk"` adds one, `note` shows them, `note done 2` ticks one off,
  `note rm 3` deletes one, `note search word` finds them, and #tags work. They're a plain checklist file you can open in
  any editor (`note open`).
- **Apps open where you left them** (KDE): each app's window size and position are remembered when you close it, and
  maximised apps open maximised. Turn it off in Customise ("Don't remember where windows were").

## Fixed and changed
- **Automatic tiling no longer overlaps windows:** apps that resize themselves just after opening (browsers, terminals,
  Electron apps) are put back in their tile, and tiling wins over "remember where windows were".
- **New windows open in the middle of the screen,** so the top edge can always be grabbed to resize.
- **Pictures stay solid in "See-through all the time":** photo viewers and image editors (Gwenview, Okular, GIMP, Krita
  and others) are no longer see-through. Tick "Keep pictures see-through too" in Customise if you like them see-through.
- **fastfetch** always shows the Devium logo next to your info, whatever the window size.
- **Devium widgets on Xfce** never got their data (weather, sea, system...) because of how they were started. Fixed.
- **Home screen pages are removed.** If you had them on, they're taken off your desktop when you update.

## Updating from beta17
Open **Devium Updater** and press **Update Devium**. Or in a terminal:

```bash
pkexec /usr/lib/devium/devium-helper refresh beta18
```

Then log out and back in. From beta15 or beta16, run the same command.

**Please test and tell us on Discord:** the new wallpaper pickers, the Now playing widget and the screenshot editor.
If you can, fill in a **Hardware report** on GitHub (Issues > New issue).

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
