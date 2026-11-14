# Devium beta12

## Fixed
- **Devium Tools wouldn't open on an installed Devium** (and the restart pop-up never showed). Some Devium
  programs weren't marked as runnable outside the live ISO; the build now makes sure they all are.

## Changes
- **Devium Setup is now "Devium Configure"**, with the Devium icon.
- **Dock:** your apps, then the start button. No more Trash icon. The dock grows and shrinks with the
  number of apps in it.
- **About Devium** only appears on the live ISO, not on your installed system.
- **yay** (installs community packages from the AUR) is ticked by default in Devium Configure.
- Devium Tools home: Privacy and Report a problem tiles.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
