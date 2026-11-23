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
- **Fewer apps in the menu and in Spotlight.** Devium Updater, Wallpapers, Screenshot Editor, Snip and About Devium no
  longer have their own menu entries: they are all in **Devium Tools** (new tiles for Wallpapers, Screenshot
  Editor, What's new and About Devium, next to Configure and Updater). Searching "devium" in Spotlight now shows
  just Devium Tools. You can still find the others by name, e.g. type "screenshot" or "updater" in Spotlight.
- **Devium Configure moves into Devium Tools after your first setup.** On a brand-new install it is its own app so you
  can find it; once the first setup has finished, its separate menu entry goes away and you open it from Devium
  Tools (or Spotlight, or System Settings > Devium).

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
