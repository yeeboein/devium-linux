# Devium beta7

Fixes from testing the point-and-click installer (there's no beta6: we went straight to beta7).

## Fixed
- **Installer stopped with "Package Manager error"** while downloading Devium's packages:
  - Devium's own files were already on the new system (copied from the live preview), so
    installing the `devium-desktop` package on top of them was refused. It's now installed
    afterwards in a way that's allowed to replace those copies.
  - The new system now gets the live preview's working package signing keys before downloading,
    so downloads aren't rejected.
- **The live preview locked itself** after a few idle minutes, asking for a password nobody was
  told. Auto-lock is now off on the live preview, and About Devium shows the live login
  (user `devium`, password `devium`).

## Also in this release (since beta4)
- Installer fix for "Bad unpackfs configuration"
- QR codes for links (scan with your phone when no browser is installed)
- Loading splash when you click **Install Devium**
- Lighter installs (download cache removed after installing, no offline docs, smaller fonts),
  12 GB minimum disk, and the KDE ISO fits in one file
