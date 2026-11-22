# Devium beta19

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. A big update for Devium Tools, Spotlight and System Settings.

## Updating
From beta18.5, the **Update Devium** button in Devium Updater works as usual (or run
`pkexec /usr/lib/devium/devium-helper refresh beta19` in a terminal). Then **log out and back in**, so the new
keys (Alt+Space, Meta+Shift+G) start working. From beta18 or earlier, use the terminal command once.

## New
- **Profound in Devium Configure.** Tick **Profound (offline AI coding buddy)** on the **Developer tools** page.
  Profound is Yeeboein's offline AI coding app: chat with an AI that writes, edits and styles your code, 100% on your
  computer, no account. Devium downloads the latest version from github.com/yeeboein/profound (about 60 MB) and adds
  it to the menu. The AI models are big, so you add one yourself: the first time you start Profound it opens the
  models folder (`/opt/profound/models`) and tells you what to put there. Untick it later to remove the app (your
  models are kept).
- **Devium Tools looks much nicer:** a header with the logo, four live cards (Storage, Memory, Battery, Devium version
  and uptime), the tools in three groups of big clickable cards, a search box above the side list, bigger icons, and a
  cleaner look everywhere: rounded boxes and fields, thin scroll bars, hover highlights and tidier tables. The other
  Devium apps pick up the same polish.
- **Devium is now in System Settings.** A new **Devium** section at the top of the list has Devium Tools, Updates,
  System storage, Clean up, App Manager, Make it faster, Look and desktop reset, Backup and move, Drivers, Health
  check, Battery charge limit, Privacy, Phone link, Background and extras, Coding tools, Printers, Get help, Devium
  Configure and Devium Updater. Each opens that page of Devium Tools and shows up when you search System Settings.
- **Devium Tools > System storage:** where your disk space went, in one picture. A coloured bar for each disk split into
  System, Apps, Games, Documents, Downloads, Pictures, Videos, Music, Code and projects, Caches and logs, and Other,
  with the size of each, buttons to open the folder or jump to Clean up, and every drive with its free space. It only
  looks, nothing is deleted. Search "storage" in Spotlight to open it.
- **Spotlight polish:** every result has a small label (App, Setting, File, Web, Answer...), the hint under the box says
  what Enter will do, the window fades in, and results are drawn cleaner. It remembers what you open, so apps you use a
  lot rank higher, and pressing Down in an empty box shows your recent apps and commands.
- **Spotlight always fits its contents:** the window grows and shrinks smoothly as you type, and when you delete your
  search it goes back to just the search bar.
- **Spotlight keys:** Alt+1 to Alt+8 opens that result, Ctrl+N / Ctrl+P (or Ctrl+J / Ctrl+K) and PageUp / PageDown
  move through results, and Up on the first result goes to the last.
- **Spotlight replaces KDE's built-in search (KRunner):** Alt+Space and Alt+F2 now open Spotlight as well as
  Meta+Space, and KRunner's own shortcuts are switched off.
- **Spotlight is exempt from tiling:** on Hyprland, Super+Space opens it as a floating box near the top of the screen
  that never joins the tiled windows (it makes sure of that itself, whatever Hyprland version you have), and pressing
  Super+Space again closes it instead of opening a second copy. On KDE it never joins the automatic tiling either.
- **Meta+Shift+G turns glass mode off** (the see-through windows), and pressing it again brings it back. It's the
  `devium-glass` command (`off` / `on` / no word to switch), works on KDE and Hyprland, and keeps Customise in step.
- **Devium Configure can't be closed the first time until Devium is fully set up:** closing it shows "Sorry, you can't
  close Configure until Devium is fully set up." (Not on the live ISO, and not for Customise.)

## Fixed
- **fastfetch in narrow and tall windows:** lines are cut to the window width, and in narrow windows CPU, GPU,
  Memory, Disk and Packages show short versions (no clock speed, percentage or file system), so nothing wraps under
  the logo.

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
