# How Devium updates (the rolling model)

**Short version:** Devium is Arch-based and *rolling*. You install it once and keep it up to date. There is no
"Devium 2.0, reinstall to upgrade". Devium's own parts are updated in numbered steps on top of that.

## Two layers
| Layer | What it is | How it updates |
|---|---|---|
| **The system** | The kernel, KDE Plasma / Xfce / Hyprland, drivers, your apps | Rolling. Normal Arch packages, always the newest versions, through `pacman` |
| **Devium's own parts** | Devium Configure, Tools, Spotlight, Updater, themes, widgets, wallpapers, the helper scripts | Numbered releases (`beta18.5`, `beta19`, ... `v1.0`) |

The ISO you download is a **snapshot** of both layers on release day. A newer ISO is only a fresher starting
point: if you already have Devium installed you never need one.

## What "rolling" means for you
- **You are always current.** One update brings the newest kernel, desktop and apps. No big upgrade every six months.
- **You install once.** Your files, apps and settings stay across every update.
- **Updates are frequent.** There are small updates often instead of one big one now and then.
- **Now and then an update breaks something.** That is the price of always having the newest software, and it
  happens on every rolling distro. Devium gives you ways back (below).

## How to update
1. **Devium Updater** (or Devium Tools > Updates). It shows what is waiting, updates the system, and updates
   Devium's own parts when a new Devium release is out. "Update Devium" is the button for the numbered releases.
2. **Terminal:** `sudo pacman -Syu` updates the system. To update Devium's own parts to a release:
   ```bash
   pkexec /usr/lib/devium/devium-helper refresh <version>
   ```
   Log out and back in afterwards.
3. Devium Tools can also show update notifications and update Flatpak apps.

Tip: update when you have a few minutes and a charged battery, and don't turn the computer off during an update.
Restart now and then, especially after a new kernel.

## If an update goes wrong
- **Undo the last update.** Devium Tools > Updates has "Undo". It puts back the package versions from before the
  last update (they are kept in pacman's cache, so this works until the cache is cleaned).
  Terminal: `pkexec /usr/lib/devium/devium-helper undo-update`.
- **Safe mode.** The boot menu has a Devium safe mode entry with reset, undo update and Doctor.
- **Doctor.** `support fix` checks for common problems and fixes what it can.
- **Ask.** Discord: https://discord.gg/YTMattgyG3. Say what you updated and what broke.
- **Coming for 1.0:** automatic Btrfs snapshots before every update, with a Restore button.

## Channels: stable and beta
Devium Updater has two channels (Devium Tools > Updates, or `~/.config/devium/update-channel`):
- **stable:** only finished releases (`v1.0` and later).
- **beta:** every beta too, so you get new features first and help test.

Version order: `beta1` ... `beta18` < `beta18.5` < `beta19` < `v1.0-beta1` < `v1.0-rc1` < `v1.0`.
The final `v1.0` ranks above every beta, so beta users move to it automatically.

## Good habits on a rolling system
1. Read the release notes (`docs/releases/`) before a big update.
2. Keep a backup of anything important (Devium Tools > Backup and move).
3. Don't mix in random repositories or half-finished manual changes. Use Devium Configure and Discover for apps.
4. Update regularly. A computer that goes six months without updates takes longer to catch up and is more likely to hit a hiccup.
5. Do a restart after kernel or graphics driver updates.

## Is rolling the right choice for me?
- **Good for:** developers and anyone who wants the newest tools, learners who like to understand their system,
  people who want to install once and keep going.
- **Maybe not for:** a computer that must never change (an exam machine, a machine you cannot fix), or someone
  who wants updates only once or twice a year. A fixed-release distro suits that better.

## What we plan
- Online signed package repository for Devium's own parts, so ordinary system updates carry Devium too.
- Btrfs with automatic snapshots before updates, and a one-click Restore.
- An upgrade test for every release (older beta to the newest in a virtual machine, files kept).
- Optional "delay my updates by a week" setting for people who want others to find the bugs first.

Devium is Arch-based and not affiliated with or endorsed by Arch Linux.
