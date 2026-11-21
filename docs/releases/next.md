# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## New since beta18.5 (in the next beta)
- **Devium Tools looks much nicer:** a header with the logo, four live cards (Storage, Memory, Battery, Devium version and
  uptime), the tools in three groups of big clickable cards, a search box above the side list, bigger icons, and a
  cleaner look everywhere: rounded boxes and fields, thin scroll bars, hover highlights and tidier tables. The other
  Devium apps pick up the same polish.
- **Devium is now in System Settings.** A new **Devium** section at the top of the list has Devium Tools, Updates,
  System storage, Clean up, App Manager, Make it faster, Look and desktop reset, Backup and move, Drivers, Health
  check, Battery charge limit, Privacy, Phone link, Background and extras, Coding tools, Printers, Get help, Devium
  Configure and Devium Updater. Each opens that page of Devium Tools and shows up when you search System Settings.
- **Devium Tools > System storage:** where your disk space went, in one picture. A coloured bar for each disk split into
  System, Apps, Games, Documents, Downloads, Pictures, Videos, Music, Code and projects, Caches and logs, and Other,
  with the size of each, buttons to open the folder or jump to Clean up, and every drive with its free space. It only
  looks, nothing is deleted. Search "storage" in Spotlight to open it.
- **Spotlight polish:** every result has a small label (App, Setting, File, Web, Answer...), the hint under the box says
  what Enter will do, the window fades in, and results are drawn cleaner. It remembers what you open: apps you use a
  lot rank higher, and an empty box shows your recent apps and commands.
- **Spotlight always fits its contents:** the window grows and shrinks smoothly as you type, and when you delete your search it goes back to just the search bar (before, it could stay too tall after a search). Recent apps show when you press Down on an empty box.
- **Spotlight keys:** Alt+1 to Alt+8 opens that result, Ctrl+N / Ctrl+P (or Ctrl+J / Ctrl+K) and PageUp / PageDown
  move through results, and Up on the first result goes to the last.
- **Spotlight replaces KDE's built-in search (KRunner):** Alt+Space and Alt+F2 now open Spotlight as well as
  Meta+Space, and KRunner's own shortcuts are switched off. Log out and back in after updating.
- **Spotlight is exempt from tiling:** on Hyprland, Super+Space opens it as a floating box near the top of the screen
  that never joins the tiled windows (it makes sure of that itself, whatever Hyprland version you have), and pressing
  Super+Space again closes it instead of opening a second copy. On KDE it never joins the automatic tiling either.
- **Meta+Shift+G turns glass mode off** (the see-through windows), and pressing it again brings it back. It's the
  `devium-glass` command (`off` / `on` / no word to switch), works on KDE and Hyprland, and keeps Customise in step.
  Existing installs get the key the next time they log in.
- **Devium Configure can't be closed the first time until Devium is fully set up:** closing it shows "Sorry, you can't
  close Configure until Devium is fully set up." (Not on the live ISO, and not for Customise.)
- **fastfetch fixed in narrow and tall windows:** lines are cut to the window width, and in narrow windows CPU, GPU,
  Memory, Disk and Packages show short versions (no clock speed, percentage or file system), so nothing wraps under
  the logo.

## Planned for 1.0
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15 to beta18.5 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **Fixes** for everything testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
