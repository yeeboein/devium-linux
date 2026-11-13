<p align="center">
  <img src="docs/banner.png" alt="Devium" width="100%">
</p>

<p align="center">
  <img src="profile/airootfs/usr/share/devium/logo.png" width="96" alt="Devium logo"><br>
  <b>An Arch-based distro for coding. Light enough for old laptops, easy enough for your first Linux install.</b>
</p>

<p align="center">
  <a href="https://discord.gg/YTMattgyG3"><img src="https://img.shields.io/badge/Discord-join-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/yeeboein/devium-linux/releases"><img src="https://img.shields.io/github/v/release/yeeboein/devium-linux?include_prereleases&label=download&color=8fb4d8" alt="Download"></a>
</p>

<p align="center">
  <img src="docs/screenshots/desktop-mockup.png" width="90%" alt="Devium desktop">
</p>

## What is this?

I wanted an Arch setup I could put on any laptop and start coding on straight away, without spending
an evening configuring it. So I made Devium.

It's Arch Linux with KDE Plasma (or Xfce for really old machines), a blue-grey theme, a floating dock,
and a setup app that asks what you actually want instead of installing everything. You pick your
browser, editor, languages, games and apps, it shows you how much space each one takes, and that's
all that goes on your computer.

It's still in beta, so expect the odd bug. If you find one, tell me on
[Discord](https://discord.gg/YTMattgyG3) or open an issue.

## What you get

- **A real installer.** Click Install Devium, pick your disk, done. Works next to Windows too.
  Needs about 10 GB.
- **Devium Setup.** Runs after install. Browser, file manager, terminal, code editor, languages
  (Python, C/C++, Rust, Go, Java, Node...), Python libraries, dev tools, games, apps. Run it again any
  time to add or remove stuff.
- **Devium Tools** (Meta+T). App manager with size and RAM use, updates with undo, a "make it faster"
  button, low-RAM mode, battery charge limit, privacy switches, printers, Docker, Git/GitHub setup,
  help for people coming from Windows, and a way to report bugs.
- **[ArchPill](https://github.com/yeeboein/archpill)** if you want it: a little pill at the top of the
  screen with the time, music, volume and battery, and a control centre when you click it.
- **Linux Magnify** if you want a macOS-style dock where the icons grow under your mouse.
- **Optional local AI.** Ollama with a model that fits your RAM. Off unless you pick it.
- **`support`** in the terminal lists about 100 useful commands. `support fix` checks for common
  problems and fixes what it can.
- Small touches: Devium icon pack, light and dark themes, disk encryption option, Irish/Spanish/
  French/German in the Devium apps, and a fastfetch logo made out of the word DEVIUM.

## Screenshots

From a real install:

<p align="center">
  <img src="docs/screenshots/real/setup-01-welcome.png" width="45%">
  <img src="docs/screenshots/real/setup-02-browser.png" width="45%"><br>
  <img src="docs/screenshots/real/setup-06-languages.png" width="45%">
  <img src="docs/screenshots/real/setup-09-gaming.png" width="45%"><br>
  <img src="docs/screenshots/real/setup-10-apps.png" width="45%">
  <img src="docs/screenshots/real/setup-11-summary.png" width="45%">
</p>

<p align="center">
  <img src="docs/screenshots/real/terminal-fastfetch.png" width="70%">
</p>

More in [docs/screenshots/real](docs/screenshots/real).

## Download

Grab the latest ISO from [Releases](https://github.com/yeeboein/devium-linux/releases). There are two:

- **KDE Plasma**: the main one, for most computers
- **Xfce**: lighter, for old laptops

First time? The [guide](docs/GUIDE.md) walks you through putting it on a USB stick or in a VM.

### Trying it in VirtualBox

- Turn on **EFI** (Settings > System). If you forget, it keeps booting the installer after you install.
- 4 GB RAM, 2 CPUs, 20 GB disk
- Graphics: VMSVGA with 3D acceleration on

The live session logs in as `devium` (password `devium`). If you get a black screen, pick
"safe graphics" in the boot menu. After installing, remove the ISO from the virtual drive before
rebooting.

## Building it yourself

The ISOs are built by GitHub Actions (`.github/workflows/build-iso.yml`). On an Arch machine you can
build one locally:

```bash
git clone https://github.com/yeeboein/devium-linux.git
```

```bash
cd devium-linux
```

```bash
sudo ./build.sh
```

Use `sudo EDITION=xfce ./build.sh` for the Xfce version. The ISO ends up in `out/`, and
`sudo ./build.sh --clean` starts from scratch.

### Where things are

```
build.sh                      builds the ISO (wraps mkarchiso)
profile/packages.x86_64       package list (#install = installed systems only, #kde = KDE edition only)
profile/airootfs/             everything that goes into the system
  usr/local/bin/devium-*      the Devium apps
  usr/lib/devium/             setup script, root helper, shared UI code, Devium Setup's app list
  usr/share/devium/           logos, fastfetch logo, previews
  etc/calamares/              the installer
editions/xfce/                Xfce edition overrides
tools/make-icons.py           generates the Devium icon pack
docs/                         guide, release notes, screenshots
```

Want to change the app list in Devium Setup? It's all in `profile/airootfs/usr/lib/devium/setup_catalog.py`.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Next up: more desktops for 1.0 (Hyprland, Cinnamon, COSMIC and others,
no GNOME) and maybe ARM.

## Thanks

Devium is built on [Arch Linux](https://archlinux.org), [KDE Plasma](https://kde.org/plasma-desktop),
[Calamares](https://calamares.io) and a lot of other open source work. Icons use shapes from
[Simple Icons](https://simpleicons.org) and KDE's Breeze.

My other projects that ship with it: [ArchPill](https://github.com/yeeboein/archpill),
[KDElite](https://github.com/yeeboein/kdelite) and [Linux Magnify](https://github.com/yeeboein/linux-magnify).

Made by [Yeeboein](https://github.com/yeeboein).
