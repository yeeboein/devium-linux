# Devium roadmap

Status of the "next update" (v2). Tick items as they land.

## Look and feel
- [x] Mountain wallpaper as default (desktop, login, lock screen)
- [x] Dock: centred, big icons, floating, hides when a window covers it ("dodge windows")
- [x] White Devium logo as the dock's app-menu button
- [x] Animated Devium boot screen (Plymouth)
- [x] No emojis in Devium apps (theme icons instead)
- [x] Big floating dock is part of the Devium themes (Base KDE gets the normal panel)

## Installer
- [ ] Point-and-click installer (Calamares), Devium-branded, beginner instructions on every page

## "Welcome to Devium" setup wizard (first boot after install) - done (devium-setup-wizard)
Pages: Welcome, Browser, Everyday apps (file manager + terminal), Code editor, Languages /
compilers, Python libraries, Developer tools, Apps (Flathub), Look and feel (mode, theme,
shell, ArchPill, dock), Summary (sizes + free space), Installing, Done.
- Browsers: Brave, Brave Origin (TODO: no verified Arch/Flathub package yet), Firefox, Chrome, Chromium, LibreWolf, Vivaldi, none
- File managers: Dolphin, Thunar, PCManFM-Qt, Nemo, Nautilus, yazi
- Terminals: Konsole, Kitty, Alacritty, WezTerm, Ghostty, Foot
- Editors: VSCodium, VS Code, PyCharm, IntelliJ, Zed, Neovim, Vim, Kate
- Languages: Python, C/C++ (gcc, clang, cmake, make, ninja, meson, gdb, lldb, valgrind), Rust,
  Go, Java (+Maven/Gradle), Kotlin, C#/.NET, Zig, Fortran, Haskell, Lua (+LuaRocks), Node.js
- Python sets: Basics, Data science, Web, Testing, AI/ML
- Dev tools: git + gh, glab, Docker, Ollama, AI chat app, AI coding extension, SQLite browser, lazygit
- Apps: Discord, Spotify, Steam, LibreOffice, GIMP, OBS, Thunderbird, VLC
- ArchPill optional (ticked by default)

## Light on storage and RAM
- [x] Extras only installed when picked in the wizard (target: ~5-6 GB disk, ~450-600 MB RAM idle, ISO < 2 GB)
- [x] Package cache auto-clean, journal capped at 50 MB, on-demand services
- [x] Storage info: sizes in wizard, disk breakdown + "Free up space" in Update Manager, low-space warning

## Other
- [x] zsh by default (autosuggestions + syntax highlighting); fish/bash in the wizard
- [x] Devium Updater app: checks GitHub Releases for new Devium versions, updates Devium's own files, downloads new ISOs
- [x] ISOs published as GitHub Releases per edition ("KDE Plasma")
- [x] Remove network-boot (PXE) options from the ISO
- [x] Rename "Arch Linux" boot entries to Devium on installed systems

## beta3 (done)
- [x] devium-desktop package on the ISO: installs no longer depend on GitHub; first-boot safety net
- [x] Live ISO shows only Install Devium + About Devium; extras removed from the ISO
- [x] Installer progress bar, disk size check, no time-sync hang
- [x] About Devium + Developers section
- [x] KDE Lite / Full KDE choice (KDElite)
- [x] Gaming page, Devium Dark, support command

## beta4
- [x] Point-and-click installer (Calamares) with "Install alongside" dual boot (GRUB + os-prober)
- [x] Devium Xfce edition (editions/xfce, EDITION=xfce ./build.sh)
- [x] Brave Origin (official build from Brave's GitHub releases)

## beta5
- [x] Installer fix (squashfs-tools, rsync), QR codes for links, install splash, storage trims, 12 GB minimum

## beta7
- [x] Installer packages step fixed (devium-desktop installed with --overwrite after it, live keyring copied), no auto-lock on the live preview

## beta8 (planned)
- [x] No "Disks & Devices" pop-up on the live preview while installing
- [x] Devium Setup: Cancel install button; "Not enough space" sends you back to the start
- [x] Devium Setup: descriptions wrap (nothing cut off), no duplicate "(included)"
- [ ] Installer fixes from the beta7 test
- [ ] Blank Devium (still choose Devium / Devium Dark / Base KDE)
- [x] Devium Setup any time: installed things start ticked, untick to remove them
- [x] Rename "Apps" to "Packages"
- [x] More Python library sets (maths, images, games, GUIs, CLIs, databases, scraping, documents)
- [x] Local AI (optional): Ollama + Alpaca, model picked to fit your RAM
- [x] Magnify dock option (linux-magnify)
- [x] Devium Tools: Devium Hub, App Manager (size, average RAM, remove), Safe Updates (Arch news,
      undo last update, automatic updates), Make it faster, Low-RAM mode, battery health and charge
      limit, privacy, printers and scanners, Docker/Podman, Git/GitHub connect, Coming from Windows
      (copy your files), accessibility, language, Get help
- [x] Report a problem: goes to the Devium Discord (webhook from a GitHub secret)
- [x] Low-RAM mode turns on by itself on 4 GB computers; zram tuned to your RAM
- [x] Disk encryption option in the installer
- [x] Translations: Irish (Gaeilge), Spanish, French, German
- [x] devium-ram, support search, "support fix"
- [ ] Easy backup, export/import setup, stricter disk check

## beta9 (in progress)
- [x] Devium Setup: progress bar moves smoothly during each step
- [x] Devium icon pack: every app icon is a rounded square in the Devium gradient with the logo in white (part of the Devium themes)
- [x] KDE ISO in one file again (about 1.9 GB)
- [ ] Easy backup to USB (and restore), export/import your Devium Setup choices
- [ ] Stricter disk check in the installer
- [ ] Blank Devium (nothing extra installed, still pick Devium / Devium Dark / Base KDE)
- [ ] ArchPill: take over notifications and the volume popup automatically when it's turned on
- [ ] Fixes from beta8 testing

## beta10 (in progress)
- [x] Dock fits its apps (no wide bar), terminal pinned
- [x] Devium Setup: Full KDE recommended with 8 GB+ RAM, KDE Lite below that
- [x] Devium Setup: "Terminal fun" page (cmatrix, cbonsai, asciiquarium, cowsay, tldr, bat, eza...)
- [x] Devium Setup again on an installed Devium: "Let's configure your Devium", everything installed is ticked, "Updating"
- [x] ArchPill starts after setup and takes over notifications and the volume popup
- [x] "We recommend a restart" pop-up after setup (Restart now / Ignore)
- [x] New Linux Magnify (replaces the dock, copies pinned apps, own settings app)
- [x] 10 GB minimum disk, smaller installs
- [x] No install loop: the live ISO notices an installed Devium and explains; "Start installed Devium" in the BIOS menu

## beta11 (in progress)
- [x] Fix: window title bars missing in beta10 (couldn't close windows) - back to KDE's standard buttons
- [x] No ArchPill tour; the restart pop-up appears one minute after Setup finishes
- [x] Devium Setup only shows what works on your desktop (ArchPill needs Wayland; Linux Magnify needs its packages)
- [x] Linux Magnify installed the way its README says (packages, install.sh with autostart, then start it)
- [x] ArchPill off by default; ticking Linux Magnify ticks ArchPill too (you can still untick it)
- [x] Dock starts with only the terminal pinned; start button in the middle of the dock (apps | start | tray)
- [x] Devium Welcome no longer opens at login; updates live in Devium Tools (Meta+U)
- [x] Installer upgrades in one step and refreshes mirrors and keys first (fixes "Package Manager error")
- [x] README rewritten
- [x] Devium Welcome removed (Devium Setup + Devium Tools cover it; driver tips moved to `support`)
- [x] Fix: dock icons disappearing after a restart (restart goes through KDE so it saves first, Setup saves
      the dock straight away, and a login check puts pinned apps back if they ever go missing)
- [x] Devium Dark icons are a real copy, not a folder link

## Next
- [ ] RAM trims: zram tuning, earlyoom, services off by default, devium-ram command
- [ ] Real screenshots from a VM for the website

## V1 (1.0): more desktops (no GNOME)
ISOs: KDE Plasma (main), Xfce (old laptops), Hyprland (tiling showcase).
Installer gets a "Desktop" page to install any of these from any ISO, each with Devium theming,
Devium apps, support, fastfetch, a Devium-style dock/bar, and ArchPill where supported.
Tiling desktops ship a beginner-friendly starter config and a shortcuts cheat sheet.
- [x] KDE Plasma
- [x] Xfce
- [ ] Hyprland (bar, launcher, notifications, lock screen, starter keybinds)
- [ ] Cinnamon
- [ ] COSMIC
- [ ] LXQt
- [ ] MATE
- [ ] Sway
- [ ] niri
- [ ] i3
- [ ] Budgie? (partly GNOME-based - decide)
- No GNOME (and GNOME can't show ArchPill)
