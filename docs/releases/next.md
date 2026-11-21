# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## Planned
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15 to beta18.5 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **Spotlight is exempt from Hyprland's tiling:** Super+Space opens it as a floating box near the top of the screen
  that never joins the tiled windows (Spotlight now makes sure of that itself, whatever Hyprland version you have),
  and pressing Super+Space again closes it instead of opening a second copy.
- **Fixes** for everything beta18.5 testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Screenshot editor (crop, arrows, blur private details)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
- fastfetch: long lines are cut to the window width so they never wrap back under the logo (narrow windows looked broken).
- fastfetch in a narrow or tall window: CPU, GPU, Memory, Disk and Packages show short versions (no clock speed, percentage or file system) so nothing wraps under the logo.
- Spotlight polish: every result has a small label (App, Setting, File, Web, Answer...), the hint under the box says what Enter will do for the selected result, the window fades in, and results are drawn cleaner.
- Spotlight remembers what you open: apps you use a lot rank higher, and an empty box shows your recent apps and commands.
- Spotlight keys: Alt+1 to Alt+8 opens that result, Ctrl+N / Ctrl+P (or Ctrl+J / Ctrl+K) and PageUp / PageDown move through results, and Up on the first result goes to the last.
- Devium Configure can't be closed the first time until Devium is fully set up: closing it shows "Sorry, you can't close Configure until Devium is fully set up." (Not on the live ISO, and not for Customise.)
