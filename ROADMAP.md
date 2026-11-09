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

## Next
- [ ] Point-and-click installer (Calamares)
- [ ] Brave Origin (when a package source exists)
- [ ] Maybe: Devium Xfce edition for very old laptops
