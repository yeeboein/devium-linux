# 1.0

<!-- For Yeeboein: Devium Updater shows this list as "Coming in 1.0". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When 1.0 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

**Devium 1.0**, the first full release.

## New since beta19.5 (in the next beta)
- **Devium restarts by itself after an update.** When Devium Updater finishes, it says "Devium is updated" and
  restarts the computer after a 30-second countdown, with **Restart now** and **Not now** buttons, so new apps, keys and
  icons start fresh without you having to remember to log out. Do nothing and it restarts; press **Not now** to stay.
  Tick or untick **Restart automatically after updates** in that window to turn it on or off (when it's off it only
  asks). "What's new" then shows at your next login. The Update Manager does the same after a Linux kernel update.

## Planned
- **Devium updates through normal system updates:** Devium's own files come from a signed online package repo, so
  updating your system updates Devium too, and old files are cleaned up properly.
- **Signed downloads switched on** for every ISO.
- **Tested upgrades:** beta15 to beta19.5 move to 1.0 with one click, keeping your files and apps.
- **A tested installer:** every build installs Devium in a virtual machine and starts it.
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **Fixes** for everything testers report on Discord.

## Ideas being considered
- Automatic snapshots before every update (Btrfs)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
