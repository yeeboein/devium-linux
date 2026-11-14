# Devium beta15

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**.

## New
- **Devium Spotlight (Meta+Space):** one search box for apps, settings and files. It also does quick maths
  (`12*7`, `15% * 80`, `sqrt(2)`), unit conversions (`10 km in miles`, `100 f to c`, `5 GB in MiB`),
  and `> command` runs a command in the terminal.
- **Accent colours** (Devium Tools > Look): Devium blue, Lavender, Mint, Sky, Peach, Rose, Lemon, Graphite or any
  colour you like. It changes the theme highlight, window borders, the Devium apps and the login screen.
- **Reset desktop** (Devium Tools > Look): dock gone, panels in the wrong place or the theme broken? One button puts
  the desktop back to Devium's defaults. Your files and apps stay, and a copy of the old settings is kept.
- **Phone link** (Devium Tools > Phone link): set up KDE Connect with a QR code. Send files both ways, see your
  phone's notifications, share the clipboard, and use the phone as a touchpad or remote.
- **Backup to USB** (Devium Tools > Backup and move): copies your home folder and app list to a USB drive. Later
  backups only copy what changed. **Restore** puts everything back and reinstalls your apps.
- **Move to a new PC:** save your apps, Flatpaks, VS Code extensions, Devium Configure choices, dock, accent colour
  and terminal settings to one small `.devium` file, then import it on the new computer.
- **Drivers** (Devium Tools > Drivers): finds NVIDIA graphics, Broadcom Wi-Fi, laptop sound firmware and fingerprint
  readers, and installs the right driver in one click.
- **Health check** (Devium Tools > Health check): disk health and wear, temperatures and battery wear on one page.
  Devium checks your disks every day and warns you at login if one is starting to fail.
- **What's new:** after Devium Updater moves you to a new version, a window like this one shows what changed.
- **`support learn`:** a hands-on terminal tutorial. Ten short lessons (pwd, ls, cd, mkdir, files, cat, cp/mv, rm,
  grep and pipes) in a safe practice folder.
- **Snap Assist (KDE):** snap a window to one side, then pick or open the window for the other side.
- **fastfetch fits your window:** big DEVIUM logo in wide terminals, a smaller logo in medium ones, and just the
  info in narrow ones, so nothing wraps onto the next line.

## For coders
- **Project starters:** `devium-new-project my-app --template rust`, or Devium Tools > Developer > New project.
  Templates: Python, website, Node.js, Flask, Rust, Go, C, C++ (CMake), Java and Discord bot, each with Git,
  a README and the right `.gitignore`.
- **Ports and servers** (Devium Tools > Developer): see what's running on which port, open `localhost:3000` with a
  double-click, and stop it with one button.
- **More developer tools** in Devium Configure and Devium Tools: modern terminal tools (fzf, eza, zoxide, jq, yq,
  httpie), Neovim, tmux, mise + direnv + just, act (run GitHub Actions locally), DBeaver, Meld and Kubernetes tools.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
