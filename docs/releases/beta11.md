# Devium beta11

Fixes from testing beta10, a simpler Devium, and the new Linux Magnify.

## Fixed
- **Windows can be closed again.** beta10's custom title bar didn't load; Devium is back to KDE's normal
  close / minimise / maximise buttons (beta10 installs are fixed at the next login).
- **Dock icons and the centred start button no longer reset after a restart.** Restart now goes through KDE
  so it saves first, Devium Setup saves the dock straight away, and a login check puts things back if needed.
- **Installer:** fresh download servers and package keys, and one-step upgrade during install
  (fixes "Package Manager error" when the ISO is a few days old).

## Dock
- Only the terminal is pinned to start with.
- Start button in the middle of the dock: apps | start | tray (or a Trash icon with ArchPill).
- The dock is only as wide as its icons.

## Devium Setup
- ArchPill is off by default; ticking Linux Magnify turns it on (you can untick it).
- **Linux Magnify** (new version): its own start menu and settings app (Quickshell), set up exactly as its
  README says. Untick it later and it's removed completely, and the Devium dock comes back.
- C / C++ is off by default (Python is the only language ticked).
- Only shows what works on your desktop (ArchPill needs Wayland).
- No ArchPill tutorial; the "We recommend a restart" pop-up appears a minute after Setup finishes.

## Simpler
- **Devium Welcome is gone.** Devium Setup and Devium Tools cover everything; driver tips are in `support`
  (`support nvidia`, `support broadcom`).
- Updates live in **Devium Tools > Updates** (Meta+U).

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
