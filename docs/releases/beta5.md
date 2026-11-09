# Devium beta5

Everything from beta4 (point-and-click installer, dual boot, Xfce edition, Brave Origin), plus fixes
from the first real installer test.

## Fixed
- **Installer stopped with "Bad unpackfs configuration"**: the ISO was missing the tools that copy
  Devium onto the disk (squashfs-tools, rsync). Fixed in both editions.
- **Links and "Devium on GitHub" buttons did nothing** (there's no web browser until you pick one in
  Devium Setup). They now show a **QR code** to open the page on your phone, plus an
  "Open in browser" button whenever a browser is installed.
- The installer no longer shows web-link buttons that couldn't open on the live system.

## New
- **Loading animation** when you click **Install Devium**: a Devium splash (glowing logo and pulsing
  dots) while the installer starts.
- **Lighter on storage:**
  - The installer's download cache (1.5-2 GB) is removed after installing.
  - Offline documentation isn't installed (man pages stay).
  - Smaller symbol font instead of the full Nerd Font.
  - Compilers (base-devel) are added only when you pick C/C++ or AUR apps in Devium Setup.
  - Minimum disk space lowered from 20 GB to **12 GB**.

## Download
| | KDE Plasma | Xfce |
|---|---|---|
| Best for | Most computers (4 GB+ RAM) | Very old laptops (2-4 GB RAM) |
| Minimum disk | 12 GB | 12 GB |
