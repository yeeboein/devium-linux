# Devium beta15

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**.

## New
- **Devium Spotlight (Meta+Space):** one search box for apps, settings and files. It also does quick maths
  (`12*7`, `15% * 80`, `sqrt(2)`), unit conversions (`10 km in miles`, `100 f to c`, `5 GB in MiB`),
  and `> command` runs a command in the terminal.
- **Simpler login screen:** it shows your account name instead of a box to type it in, and the desktop picker
  is gone (Devium always starts its own desktop). With more than one account, small arrows switch between them.
- **Loading screen after login:** the mountains, the Devium logo and "Welcome, *name*" cover the desktop while
  it and your startup apps load, then fade away smoothly. Click to skip; turn it off in Devium Tools > Look.
- **Devium folder icons:** folders in the Devium gradient with a white symbol for Documents, Downloads, Music,
  Pictures, Videos, Desktop, Home, Projects (code), Git, Cloud, Games and more, plus a matching bin.
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
- **Snap Assist on every desktop:** snap a window to one side, then pick the window for the other side.
  - **KDE:** drag to the edge or Meta+Left/Right, then pick from KDE's window overview.
  - **Xfce:** drag to the edge or Super+Left/Right, then pick from a Devium list of your open windows.
  - **Hyprland:** windows tile side by side by themselves; **SUPER+S** picks a window (even from another
    workspace) to put next to the one you're using.
- **fastfetch fits your window:** big DEVIUM logo in wide terminals, a smaller logo in medium ones, and just the
  info in narrow ones, so nothing wraps onto the next line.
- **Devium widget pack** (all three desktops): eight desktop widgets in the Devium style. Add them from
  Devium Tools > Look (on KDE also right-click the desktop > Add or Manage Widgets). On Xfce and Hyprland
  they sit on the desktop behind your windows; drag one to move it.
  - **Sea conditions:** wave height and how rough it is, swell, water temperature, wind in knots, and a tide
    curve with the next high and low water (from Open-Meteo, free).
  - **Weather:** now, feels-like, wind, humidity, UV and the next 5 days.
  - **System:** CPU, memory and disk rings, temperature, battery and uptime.
  - **Clock:** a big clock with the date and a "Good morning" greeting.
  - **Focus timer:** 25 minutes of focus, 5 minutes of break, with a notification and a count of today's sessions.
  - **Git projects:** your repos with branch, changed files and commits to push or pull. Click to open one
    in your editor, right-click for a terminal.
  - **Dev servers:** what's running on which port, with Open and Stop.
  - **Devium shortcuts:** Spotlight, Devium Tools, Configure, Updates, Clean up and more in one click.
  Weather and sea find your town from your IP address, or you can type a place in the widget's settings.
- **Emoji style** (Devium Configure): pick how emoji look everywhere: Android / Linux (Noto, the default),
  iPhone-style (JoyPixels, glossy and rounded, the closest legal match to Apple's), flat (Twemoji, like Discord) or hand-drawn
  (OpenMoji). Works in apps, websites (Firefox too) and the terminal.
- **Brightness only in ArchPill:** with ArchPill on, Plasma's own brightness popup is switched off, so the
  brightness keys only show the pill's popup. (On Hyprland the keys now show it in the pill too.)
- **Clean up** (Devium Tools > Clean up): finds app caches, the bin, old `node_modules` / Rust `target` /
  `.venv` folders in projects you haven't touched for a month, old installers and duplicate files in Downloads,
  big forgotten files, unused Docker images and old system packages and logs. Nothing goes until you tick it.
- **Guest account** (Devium Tools > Privacy): a friend presses **Guest** on the login screen, no password. They
  can't see your files or change the system, and everything they do is wiped when they log out.
- **Crash catcher:** when an app crashes, a notification offers to send a report. It opens Report a problem,
  filled in with which app crashed and where, so you can check it before sending. (KDE apps keep their own
  crash reporter.)

## For coders
- **Project starters:** `devium-new-project my-app --template rust`, or Devium Tools > Developer > New project.
  Templates: Python, website, Node.js, Flask, Rust, Go, C, C++ (CMake), Java and Discord bot, each with Git,
  a README and the right `.gitignore`.
- **Ports and servers** (Devium Tools > Developer): see what's running on which port, open `localhost:3000` with a
  double-click, and stop it with one button.
- **More developer tools** in Devium Configure and Devium Tools: modern terminal tools (fzf, eza, zoxide, jq, yq,
  httpie), Neovim, tmux, mise + direnv + just, act (run GitHub Actions locally), DBeaver, Meld and Kubernetes tools.

## Coding tools (new page in Devium Tools)
- **Dev doctor:** `support dev` checks Git, your SSH key and GitHub, languages, Docker, PATH and your projects,
  and tells you the exact command to fix anything.
- **Databases in one click:** PostgreSQL, MySQL, Redis or MongoDB in a container, with the connection string
  ready to copy. Nothing installed on your system.
- **Secret guard:** on by default. Stops a commit that contains a password, API key, private key or `.env` file
  (uses gitleaks if you install it). Your projects' own Git hooks still run.
- **.env files:** lists your projects' secret files and warns in red if one is committed to Git. One click
  keeps it out of Git, another makes a safe `.env.example`.
- **HTTPS on localhost:** one button makes a certificate your browsers trust, so `https://localhost` just works.
- **Share a local site:** a temporary public link (and a QR code) for your `localhost:3000`.
- **Language versions per project:** pick Python, Node, Go, Rust, Java and more per folder (mise).
- **Snippets:** save code you reuse; `snip NAME` in the terminal, or `snip docker` in Spotlight.
- **Build notifications:** a notification when a terminal command that took 30+ seconds finishes or fails.
- **Offline docs:** Zeal, and `docs python:split` in Spotlight.
- **Terminal extras:** mise, zoxide (`z folder`) and fzf (Ctrl+R) switch on by themselves once installed.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
