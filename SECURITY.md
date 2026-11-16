# Security

## Reporting a problem
Please **don't** post security problems in public issues or on the Discord. Report them privately through
GitHub: [Report a vulnerability](https://github.com/yeeboein/devium-linux/security/advisories/new).
You'll get an answer within a week, and we'll credit you in the release notes if you'd like.

## What's covered
Devium's own code: its apps, scripts, the installer setup, the updater and the helper that runs as root
(`/usr/lib/devium/devium-helper`). Problems in Arch packages, KDE, Firefox and so on belong upstream, but tell us
too if Devium makes them worse.

## Updates
Devium follows Arch Linux, so security fixes for normal packages arrive with system updates (Devium Updater or
`sudo pacman -Syu`). Fixes to Devium's own files come in Devium updates. Supported versions: the latest stable
release and the latest beta.

## Checking downloads
Every ISO has a `.sha256` file. When a release has `SHA256SUMS` and `SHA256SUMS.sig`, check them with Devium's
signing key (see the release notes and `docs/VERIFY.md`).
