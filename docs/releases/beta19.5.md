# Devium beta19.5

Three editions: **KDE Plasma**, **Xfce** and **Hyprland**. A fix for fastfetch, a much tidier menu, and icons that follow your accent colour.

## Updating
From beta19, the **Update Devium** button in Devium Updater works as usual (or run
`pkexec /usr/lib/devium/devium-helper refresh beta19.5` in a terminal). Then **log out and back in**. From beta18.5 or
earlier, the same terminal command works too.

## Fixed
- **fastfetch no longer breaks in a narrow or oddly sized window.** In beta19, `fastfetch` could print "Unsupported
  module option: --cpu-format" and then fail every time at that window size, because the newer fastfetch no longer
  accepts that kind of option. The short CPU, GPU, Memory, Disk and Packages lines now live in their own config
  files, and if fastfetch ever fails for any reason, Devium runs the normal layout instead of showing an error.

## New
- **Fewer apps in the menu and in Spotlight.** Devium Updater, Wallpapers, Screenshot Editor, Snip and About Devium no
  longer have their own menu entries: they are all in **Devium Tools** (new tiles for Wallpapers, Screenshot
  Editor, What's new and About Devium, next to Configure and Updater). Searching "devium" in Spotlight now shows
  just Devium Tools. You can still find the others by name, e.g. type "screenshot" or "updater" in Spotlight.
- **Devium Configure moves into Devium Tools after your first setup.** On a brand-new install it is its own app so you
  can find it; once the first setup has finished, its separate menu entry goes away and you open it from Devium
  Tools (or Spotlight, or System Settings > Devium).
- **App icons follow your accent colour.** When you pick a new accent colour in Devium Tools > Look, the Devium app
  icons (the gradient tiles for every app, folder and file type) change to that colour too, not just the windows.
  Pick the Devium blue (or Reset desktop) to go back. It only changes your own copy in ~/.local/share/icons.
- **Websites installed as apps get a proper Devium icon.** When you "Install as app" a site in Brave, Chrome, Chromium
  and other Chromium-based browsers, its favicon is put on the Devium gradient tile like every other app, in your accent
  colour. It happens a few seconds after you install the app, and again when you change the accent colour.
- **Meta+Shift+G turns off everything see-through,** not just glass mode: glass mode, see-through all the time,
  see-through background and moving windows, menus, title bars, the blur behind them, the dock, the top bar and the
  terminal. Press it again to bring back exactly what was on. (Pictures and Solid dock options are left alone.)

## Tip for VirtualBox
Turn on **EFI**, give it **20 GB** of disk and **4 GB** of RAM, and remove the ISO after installing.
