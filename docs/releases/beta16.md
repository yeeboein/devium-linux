# Devium beta16

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. A smaller release with fixes from beta15 testing.

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
- **No loading screen after login:** you go straight from the login screen to your desktop.
- **fastfetch shows your Devium version:** a new line, `Ver  Devium Beta16`.

## New
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
