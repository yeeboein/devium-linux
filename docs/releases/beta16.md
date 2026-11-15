# Devium beta16

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. Fixes from beta15 testing, tiling for KDE, 126 Customise options and a Linux tools page.

## Fixed
- **Devium Updater finds new versions again.** It said "No Devium releases published yet" because GitHub leaves
  beta releases out of its "latest release". It now sees every release, betas included, so the Update button
  works for future versions.
- **The fastfetch logo no longer breaks** when the window is small or resized:
  - one full-size DEVIUM logo only; in a wide window the info sits beside it, in a narrow window it goes
    underneath, so they never run into each other
  - the terminal keeps old output as it was when you resize the window, instead of re-wrapping it
    (Konsole and the Xfce terminal)

## Changed
- **About Devium only on the live USB:** updating no longer adds it to installed systems, and updating to
  beta16 removes it if an earlier update put it there.
- **No loading screen after login:** you go straight from the login screen to your desktop.
- **fastfetch shows your Devium version:** a new line, `Ver  Devium Beta16`.

## New
- **Automatic tiling for KDE, like Hyprland** (Customise > Tiling): new windows split the screen by themselves,
  side by side and then top and bottom, with gaps. Dialogs and full-screen apps are left alone.
  - **Meta+Shift+Space** floats or tiles a window, **Meta+Shift+T** turns tiling off for a moment
  - **Meta+Alt+Left/Right** swaps windows, **Meta+Alt+Return** makes a window the big one, or drag a window
    onto another to swap them
  - options for a "one big window and a stack" layout, and no gaps or big gaps
- **Customise now has 126 options** (111 on KDE, 35 on Xfce, 39 on Hyprland). New ones include:
  - **Windows:** no title bars at all, smaller buttons, wide borders, Alt+Tab with big previews, cover switch
    or flip switch, Alt+Tab across all workspaces
  - **Dock and desktop:** dock on the left or at the top, a macOS-style top bar with the app's menus, dock shows
    only this workspace, don't group windows, start with a clean desktop, log out without asking
  - **Keyboard and sound:** Num Lock on at login, faster key repeat, Caps Lock as Escape, swap Caps Lock and Ctrl,
    a compose key, volume up to 150%, silent volume keys
  - **Power and lock screen:** lock after 5 minutes or never, don't lock after sleep, screen off after 10 minutes,
    never sleep when plugged in, closing the lid does nothing when plugged in
  - **Files:** split view, full path, show hidden files
  - **And more:** faster or left-handed mouse, week numbers, no pop-ups over full-screen apps, colour-blind
    friendly colours, invert colours, and Xfce options (no effects, snapping windows, roll-up title bars)
- **Home screen pages, like an iPhone** (optional, KDE: Customise or Devium Tools > Look): pages of apps and
  Devium widgets on your desktop that you swipe between with the touchpad or mouse, with page dots at the bottom.
  Press and hold (or Edit) and the icons wiggle: ✕ removes, + adds apps, widgets and pages.
- **Search the web from Spotlight** (Meta+Space): every search has "Search the web for…" (DuckDuckGo, or pick
  Brave, Google, Startpage, Bing or Ecosia in Devium Tools > Look). Site shortcuts: `yt`, `g`, `wiki`, `gh`, `aur`,
  `arch`, `pkg`, `so`, `maps` and `r` followed by your words, e.g. `yt lofi beats`. Typing an address like
  `github.com` opens it.
- **Photo widget** (Devium widgets, all three desktops): a picture, or a slideshow from a folder (your Pictures
  folder unless you pick another), with rounded corners and a soft fade between photos. Settings for the folder or a
  single picture, seconds per picture, random order, fill or fit, and the picture's name. Double-click to open
  the picture. Add as many as you like on KDE.
- **Linux tools** (new page in Devium Configure): 34 handy tools, all optional: GParted, Filelight, BleachBit,
  TestDisk/PhotoRec, ddrescue, Impression (USB writer), Pika Backup, Syncthing, rclone, KeePassXC, Mission Center,
  CPU-X, inxi, PowerTOP, s-tui, OpenRGB, Piper, Solaar, Flatseal, Warehouse, Distrobox, GNOME Boxes, Firejail,
  scrcpy, yt-dlp, ImageMagick, Pandoc, 7-Zip and RAR, Nmap, Wireshark, ClamAV and more.
- **Konsole (see-through):** a new choice on Devium Configure's Terminal page: Konsole with a frosted,
  see-through background, in any Devium theme.
- **Glass mode, done properly** (Customise > "Glass mode: see-through everything"): every window is slightly
  see-through with frosted blur, the dock and terminal too, while videos, games, photo apps and full-screen
  windows stay solid. Background windows are a little more see-through than the one you're using.
- **See-through all the time** (Customise): every window see-through, always, with no exceptions (videos,
  games and full-screen too), with strong frosted blur. KDE and Hyprland.
- **Your own emoji font:** the Emoji style page in Devium Configure also lists any colour emoji font installed on
  your computer, and applies it everywhere like the built-in ones.

## Updating from beta15
Devium Updater in beta15 still has the bug above, so update once from the terminal (your files and apps stay):

```bash
pkexec /usr/lib/devium/devium-helper refresh beta16
```

Then log out and back in. From beta16 on, the Update Devium button works again.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
