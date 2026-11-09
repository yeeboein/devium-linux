# Devium beta3

The third test release of Devium, a light, fast Arch Linux desktop made for coding.

## Fixed
- **Devium's setup didn't run after installing** (you got a text login with "Arch Linux"
  instead of the Devium desktop). Devium's files now come in a `devium-desktop` package
  that's on the ISO itself, so the installer copies them straight from the ISO: no internet
  or GitHub download needed. A first-boot safety net finishes the setup if anything was missed.
- The installer no longer hangs on "Waiting for time sync".
- The installer checks the disk first and stops with a clear message if it's under 20 GB.
- The computer is named `devium` (not `archlinux`).

## New
- **Smaller, simpler live ISO:** the preview only shows **Install Devium** and **About Devium**.
  No browser or extra apps are on the ISO: you pick them after installing.
- **Progress bar while installing**, pinned to the bottom of the installer window.
- **About Devium** app with a **Developers** section (also in Devium Welcome).
- **Devium Setup wizard** (opens on first login after installing):
  - **KDE Lite** (recommended, uses less RAM, powered by [KDElite](https://github.com/yeeboein/kdelite)) or **Full KDE**
  - **Gaming:** Steam (with Proton), ProtonUp-Qt, Wine, Bottles, Lutris, Heroic, GameMode, MangoHud, Gamescope, controller support
  - **Themes:** Devium, Devium Dark or Base KDE
  - Browsers, file managers, terminals, code editors, languages and compilers, Python libraries,
    developer tools, Flathub apps, ArchPill
- **`support` command:** type `support` in a terminal for helpful commands (`support git`, `support files`...).
- Blue-grey Devium look with pale accents, recoloured logo, DEVIUM-letters fastfetch logo.
- Big floating dock (part of the Devium themes). With ArchPill, the dock shows only the start button and apps.
- Beginner/Pro mode removed: everyone gets the handy git/Python shortcuts and the Starship prompt.

## Known limitations
- The installer is still Arch's text-based installer (a point-and-click installer is planned).
- Brave Origin isn't offered yet (no verified package source).
