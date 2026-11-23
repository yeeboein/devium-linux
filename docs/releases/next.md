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
- **Updates are two pages inside Devium Tools: "Update Arch" and "Devium updates".** **Update Arch** is the whole
  system (the Update Manager, Arch news, undo, restore point and automatic updates) right in the page, and **Devium
  updates** is Devium's own new versions (what changed, stable or beta, the update button and the ISO), also right in
  the page. There is no separate Devium Updater or Update Manager window to open any more; Spotlight, System Settings >
  Devium and the shortcuts (Meta+U) all go to these pages.
- **Space pressed to wake the lock screen no longer ends up in your password** (after sleep, when you press Space and
  then type your password). On the lock screen, a Space on an empty password box now only wakes the screen. (The login
  screen already did this.) Passwords that start with a space can't be typed on the lock screen any more; spaces in the
  middle or at the end still work.
- **Websites installed as apps: icon fix and a choice.** In beta19.5 the favicon-on-Devium-tile icon could fail to
  show, because it was saved in a place not every desktop reads. Devium now puts the picture straight into the icon the
  browser made for the app (the browser's own picture is kept), so the menu, dock and Spotlight all show it. New in
  **Devium Tools > Look > Websites installed as apps:** choose **the site's icon on a Devium tile**, **just the site's
  icon** (the favicon on its own), or **leave them as the browser made them**, and press Refresh now. It also says how
  many website apps it found.

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
