# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## New since beta19 (in beta19.5)
- **fastfetch no longer breaks in a narrow or oddly sized window.** In beta19, `fastfetch` could print "Unsupported
  module option: --cpu-format" and then fail every time at that window size, because the newer fastfetch no longer
  accepts that kind of option. The short CPU, GPU, Memory, Disk and Packages lines now live in their own config
  files, and if fastfetch ever fails for any reason, Devium runs the normal layout instead of showing an error.

## Planned
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15 to beta19 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **Fixes** for everything testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
