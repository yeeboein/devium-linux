# beta17

<!-- For Yeeboein: Devium Updater shows this list as "Coming in beta17". Edit this file on GitHub to change it:
     Devium users see the new list straight away, no new ISO needed. When beta17 is released, its real release
     notes are shown instead. Comments like this one aren't shown. -->

The last beta before **Devium 1.0**: getting everything ready for a full release.

## Ready for 1.0
- **Safe mode:** pick "Devium (safe mode)" in the boot menu to start with Devium's extras paused (widgets, tiling,
  gestures, Snap Assist). A window lets you turn off every Customise tweak, undo the last update or run Devium
  Doctor, then restart normally.
- **Stable and beta updates:** Devium Updater gives you stable versions from 1.0 on. Testers can tick "Get beta
  versions too" for the newest features.
- **Signed downloads:** releases get a signed list of checksums, so you can check an ISO really comes from Devium
  (see docs/VERIFY.md).
- **Devium is free software (GPL-3.0),** with credits for the artwork and icons it uses, and a clear note that it's
  based on Arch Linux but not an official Arch product.
- **Bug, hardware and idea forms** on GitHub, a security policy, and a guide for helping out.
- **Secure Boot guide:** how to turn it off on each laptop brand (it has to be off to start Devium).

## Also planned
- **A more polished login screen:** it starts like a phone's lock screen with a big clock; press any key, click
  or move the mouse and the sign-in card slides up (typing straight away works too). New: a greeting, a
  show/hide password button, a Caps Lock warning, a spinner while it checks your password, Sleep next to Restart
  and Shut down, and smoother animations. Pressing Space to wake the screen no longer ends up in your password
  (spaces inside a password still work).
- **`support selftest`:** checks that every Devium app, widget and helper works, and gives you a list to share.
- **Automatic tests for every ISO:** each build boots in a virtual machine and is checked before release, and the
  code is checked on every change.
- **Lighter on old laptops:** Snap Assist on Xfce only wakes up when a window moves, and the crash catcher
  switches off in Low-RAM mode.
- **fastfetch side by side more often:** the logo and your info sit next to each other whenever they fit, like
  full screen (about 92 columns on a typical laptop, instead of needing 110). Only a really narrow window puts the
  info under the logo.
- **Spotlight searches with your browser:** "Search the web" now opens your default browser with the search
  engine you picked in that browser (Firefox, Brave, Chrome, Vivaldi and others). You can still pick a fixed engine
  in Devium Tools > Look.
- **Home screen pages in Devium Configure:** a clear "Home screen pages, like an iPhone" choice on the Look and
  feel page (KDE), off unless you tick it. It's the same switch as in Customise and Devium Tools > Look.
- **Closing windows looks smooth again:** the magic-lamp close animation from beta16 is gone. Minimising keeps
  KDE's real Magic Lamp genie, and closing uses KDE's own smooth fade.
- **Touchpad gestures like GNOME** (optional, Customise > Touchpad gestures): swipe up with three fingers for
  the overview, down for the desktop, and left or right to change workspace, with a new workspace appearing past
  the last one like GNOME. KDE, plus left/right on Hyprland. KDE's four-finger gestures keep working.
- **Fixes** for everything beta16 testers report on Discord.

## Ideas being considered
- Screenshot editor (crop, arrows, blur private details)
- Clone a GitHub repo from Spotlight and open it ready to code
- Community themes in Devium Tools > Look
