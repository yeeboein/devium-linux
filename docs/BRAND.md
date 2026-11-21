# Devium brand guide

Everything you need to make a website, a video, a Discord banner or a post that looks like Devium.

## Name and words
- Write it **Devium** (capital D, nothing else capital). Versions: Beta18.5, Beta19, v1.0.
- Say "Devium Linux" the first time, then "Devium". Always say it is **Arch-based** (not "Arch"). Not affiliated with Arch Linux.
- Tagline: **An Arch-based distro for coding. Light enough for old laptops, easy enough for your first Linux.**
- Short lines: "Arch Linux, made easy." / "Choose only what you need." / "Runs on 4 GB."
- Voice: plain, friendly, honest. No jargon, no hype. Say "beta" while it is beta.
- Editions: **KDE Plasma** (main), **Xfce** (light), **Hyprland** (tiling).
- Features to name the same way everywhere: Devium Configure, Devium Tools, Devium Spotlight (Meta+Space), Devium Updater, Devium widgets.

## Colours
| Name | Hex | Where it is used |
|---|---|---|
| **Devium Blue** (main accent) | `#8fb4d8` | buttons, links, focus, selected rows |
| **Devium Lavender** (accent 2) | `#b4b8e0` | the second half of every gradient, titles |
| Lavender (videos) | `#beb9e4` | gradient end in videos |
| Gradient | `#8fb4d8` → `#b4b8e0` (left to right) | primary buttons, selected items, progress bars, "Testers wanted" text |

**Dark theme (default)**
| Name | Hex |
|---|---|
| Background | `#181c22` |
| Raised surface | `#1d2229` |
| Cards, buttons | `#21272f` |
| Spotlight and app text on gradient | `#1b2026` |
| Text | `#d6dde5` |
| Soft text | `#8b98a8` |

**Light theme**
| Name | Hex |
|---|---|
| Background | `#ecf0f4` |
| Raised surface | `#e3e9ef` |
| Accent (light) | `#78a0c8` |

**Status colours:** good `#a3d4aa`, warning `#e8cd96`, error `#e89ca0`.

**Video and website extras:** black `#000000` with a soft blue glow at the bottom, white text `#f5f5f7`, grey text `#86868b`, card `#1e2128` with a `#464c58` outline.

**Terminal logo (fastfetch):** `#b8cee4`, `#96b2d0`, `#7a92b0`; separators `#5c6878`.

The accent can be changed by the user in Devium Tools > Look, so apps read it from `~/.config/devium/accent`. Marketing material always uses the default blue and lavender above.

## Fonts
- **Inter** for headings, the website and videos (free, open licence). Use Bold for headlines, Medium for small text.
- Apps use the system font (Plasma's default). Terminal and code use a monospace font (DejaVu Sans Mono in the videos).
- Headline style: big, tight, a full stop at the end ("Meet Devium.").

## Logo
- The logo is the angled **D** arrow. Files: `profile/airootfs/usr/share/devium/logo.png` (colour) and `logo-white.png` (white, on dark backgrounds). More sizes in `docs/branding/`.
- Give it clear space about half its height on every side. Never stretch, recolour or add effects.
- On photos, use the white logo on a darkened photo.
- Photo: the mountain wallpaper is from Unsplash (Unsplash License). Credit is in `CREDITS.md`.

## Shapes and style
- Rounded corners: 18 px for windows and Spotlight, 10 to 12 px for rows and buttons, pill shapes for tags and chips.
- Soft shadows, thin 1 px blue outline on floating windows, lots of space.
- Dark by default with the blue-lavender gradient used sparingly for the one thing that matters.

## Discord
- Invite: **https://discord.gg/YTMattgyG3**
- Discord blurple (only for the Discord button or badge): `#5865F2`.
- Server icon: `docs/branding/devium-discord-icon-512.png` (512 x 512).
- Server banner: `docs/branding/devium-discord-server-banner-960x540.png` (960 x 540).
- Profile banner: `docs/branding/devium-discord-profile-banner-680x240.png` (680 x 240); there is a safe-area version too.
- Bug reports and testers: the Discord is where people send them. The Report button in Devium Tools posts to the team through a private webhook (kept as a GitHub secret).

## Links
- GitHub: https://github.com/yeeboein/devium-linux
- Releases: https://github.com/yeeboein/devium-linux/releases
- Licence: GPL-3.0
- TikTok and website: to be added.

## Sizes cheat sheet
| Use | Size |
|---|---|
| TikTok / Shorts video | 1080 x 1920 (9:16) |
| YouTube video | 1920 x 1080 |
| GitHub social preview | 1280 x 640 (`docs/website/images/social-preview.png`) |
| Profile photo (TikTok, Discord) | 512 x 512, logo centred |
| Website hero | 1920 x 1080 |
