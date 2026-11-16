# Devium beta17

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. The last beta before **Devium 1.0**: safe mode, stable and
beta updates, a polished login screen, GNOME-style gestures, and everything set up for a full release.

## New
- **A more polished login screen:** it starts like a phone's lock screen with a big clock. Press any key, click or
  move the mouse and the sign-in card slides up (typing straight away works too). A greeting, a show/hide password
  button, a Caps Lock warning, a spinner while your password is checked, Sleep next to Restart and Shut down, and
  smoother animations. Pressing Space to wake the screen no longer ends up in your password (spaces inside a
  password still work).
- **Safe mode:** pick **"Devium (safe mode)"** in the boot menu to start with Devium's extras paused (widgets,
  tiling, gestures, Snap Assist). A window lets you turn off every Customise tweak, undo the last update or run
  Devium Doctor, then restart normally.
- **Touchpad gestures like GNOME** (optional, Customise > Touchpad gestures): three fingers up for the overview,
  down for the desktop, left and right to change workspace, with a new workspace appearing past the last one like
  GNOME. KDE, plus left/right on Hyprland. KDE's four-finger gestures keep working.
- **Spotlight searches with your browser:** "Search the web" opens your default browser with the search engine you
  picked in that browser (Firefox, Brave, Chrome, Vivaldi and others). You can still pick a fixed engine in Devium
  Tools > Look.
- **Home screen pages in Devium Configure:** a "Home screen pages, like an iPhone" choice on the Look and feel page
  (KDE), off unless you tick it.
- **Stable and beta updates:** from 1.0 on, Devium Updater gives you stable versions. Testers can tick "Get beta
  versions too" for the newest features.

## Changed
- **Closing windows looks smooth again:** the magic-lamp close animation from beta16 is gone. Minimising keeps
  KDE's real Magic Lamp genie, and closing uses KDE's own smooth fade. If you had it on, it's switched back for
  you at your next login.
- **fastfetch side by side more often:** the logo and your info sit next to each other whenever they fit (about 92
  columns on a typical laptop, instead of needing 110). Only a really narrow window puts the info under the logo.
- **Dolphin keeps its dolphin**, and the new folder and file icons stay.

## Ready for 1.0
- **Devium is free software (GPL-3.0),** with credits for the artwork and icons it uses, and a clear note that it's
  based on Arch Linux but isn't an official Arch product.
- **Every ISO is tested:** each build starts in a virtual machine and must reach the desktop, and Devium's code is
  checked on every change.
- **Signed downloads** are ready to switch on, so you'll be able to check an ISO really comes from Devium
  (see docs/VERIFY.md).
- **Bug, hardware and idea forms** on GitHub, a security policy and a guide for helping out.
- **Secure Boot guide:** how to turn it off on each laptop brand (it has to be off to start Devium).

## Updating from beta16
Open **Devium Updater** and press **Update Devium** (it works again since beta16). Or in a terminal:

```bash
pkexec /usr/lib/devium/devium-helper refresh beta17
```

Then log out and back in. From beta15, run the same command.

**Please test and tell us on Discord:** the new login screen, safe mode (in the boot menu), and the gestures. If you
can, fill in a **Hardware report** on GitHub (Issues > New issue) so we know which computers work well for 1.0.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
