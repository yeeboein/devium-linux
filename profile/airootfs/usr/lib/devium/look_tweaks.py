#!/usr/bin/env python3
"""Devium look tweaks: optional changes to how Devium looks and feels (Devium Configure > Customise).

Every tweak can be turned on and off again; turning it off puts back how Devium normally is.
Works on KDE Plasma, Xfce and Hyprland (each tweak says where it works).

  look_tweaks.py list              every tweak for this desktop (JSON)
  look_tweaks.py status            which tweaks are on (JSON)
  look_tweaks.py set ID=on ID=off  turn tweaks on or off
  look_tweaks.py reapply           apply everything that's on again (after a theme change)
  look_tweaks.py reset             turn every tweak off
"""
import json
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")
CFG = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(HOME, ".config")))
STATE = os.path.join(CFG, "devium", "tweaks.json")
HYPR_FILE = os.path.join(CFG, "hypr", "devium-look.conf")

KDE = shutil.which("plasmashell") is not None
XFCE = shutil.which("xfwm4") is not None and not KDE
HYPR = (shutil.which("Hyprland") is not None or shutil.which("hyprctl") is not None) and not KDE and not XFCE

CATEGORIES = [
    ("tiling", "Tiling", "Windows arrange themselves, like Hyprland"),
    ("gestures", "Touchpad gestures", "Swipe with three fingers, like GNOME"),
    ("windows", "Windows", "Title bars, buttons and how windows behave"),
    ("glass", "See-through and blur", "Transparent windows, blur and glass"),
    ("motion", "Animations and effects", "How things move, open and close"),
    ("desktop", "Desktop and screen edges", "Hot corners, workspaces, the dock"),
    ("clock", "Clock and notifications", "The clock, notifications and sounds"),
    ("mouse", "Mouse, keyboard and clicking", "Cursor, clicking and focus"),
    ("keyboard", "Keyboard and sound", "Typing, special keys and volume"),
    ("power", "Power and lock screen", "Sleep, the screen and locking"),
    ("files", "Files", "The file manager"),
    ("terminal", "Terminal", "How the terminal looks"),
    ("comfort", "Easy on the eyes", "Night light, text size and contrast"),
]

TWEAKS = []


def T(id, cat, name, desc, kde=(), kde_js=None, xfce=(), hypr=(), lines=None, func=None, group=None):
    """kde: (file, group, key, on_value[, off_value])  off_value None = back to the default
       kde_js: (javascript when on, javascript when off) run in Plasma
       xfce: (channel, property, type, on_value[, off_value])
       hypr: lines for ~/.config/hypr/devium-look.conf
       lines: {file: [lines]} added to other config files (removed again when off)
       func: name of a function below for anything more involved
       group: tweaks in the same group can't be on together (e.g. button layouts)"""
    TWEAKS.append({"id": id, "cat": cat, "name": name, "desc": desc, "kde": list(kde), "kde_js": kde_js,
                   "xfce": list(xfce), "hypr": list(hypr), "lines": lines or {}, "func": func, "group": group})


DECO = "org.kde.kdecoration2"
# ---------------------------------------------------------------------------- windows
T("mac-buttons", "windows", "macOS-style window buttons",
  "Close, minimise and maximise on the left, like a Mac",
  kde=[("kwinrc", DECO, "ButtonsOnLeft", "XIA", "M"), ("kwinrc", DECO, "ButtonsOnRight", "", "IAX")],
  xfce=[("xfwm4", "/general/button_layout", "string", "CHM|O", "O|HMC")], group="buttons")
T("close-only", "windows", "Only a close button", "No minimise or maximise buttons, just ✕",
  kde=[("kwinrc", DECO, "ButtonsOnLeft", "", "M"), ("kwinrc", DECO, "ButtonsOnRight", "X", "IAX")],
  xfce=[("xfwm4", "/general/button_layout", "string", "O|C", "O|HMC")], group="buttons")
T("red-close", "windows", "Red circle around the close button", "Makes ✕ easy to spot",
  kde=[("breezerc", "Windeco", "OutlineCloseButton", "true")])
T("big-buttons", "windows", "Bigger title bar buttons", "Easier to hit, good for touch screens",
  kde=[("breezerc", "Windeco", "ButtonSize", "ButtonLarge")])
T("center-title", "windows", "Window titles in the middle", "Centre the title on the title bar",
  kde=[("breezerc", "Windeco", "TitleAlignment", "AlignCenter")],
  xfce=[("xfwm4", "/general/title_alignment", "string", "center")])
T("no-borders", "windows", "No window borders", "Only the title bar, no frame around the window",
  kde=[("kwinrc", DECO, "BorderSize", "None"), ("kwinrc", DECO, "BorderSizeAuto", "false")],
  hypr=["general:border_size = 0"], group="borders")
T("thick-borders", "windows", "Thicker accent borders", "A clear coloured border around the window you're using",
  hypr=["general:border_size = 4"], group="borders")
T("borderless-max", "windows", "No title bar on maximised windows", "More room when a window fills the screen",
  kde=[("kwinrc", "Windows", "BorderlessMaximizedWindows", "true")])
T("big-shadows", "windows", "Bigger window shadows", "Windows float more clearly above each other",
  kde=[("breezerc", "Common", "ShadowSize", "ShadowVeryLarge")],
  hypr=["decoration:shadow:enabled = true", "decoration:shadow:range = 24", "decoration:shadow:render_power = 2"], group="shadows")
T("no-shadows", "windows", "No window shadows", "Flat look, a bit lighter on old computers",
  kde=[("breezerc", "Common", "ShadowSize", "ShadowNone")], xfce=[("xfwm4", "/general/show_frame_shadow", "bool", "false")],
  hypr=["decoration:shadow:enabled = false"], group="shadows")
T("center-windows", "windows", "Open new windows in the middle", "New windows appear centred on the screen",
  kde=[("kwinrc", "Windows", "Placement", "Centered")], xfce=[("xfwm4", "/general/placement_mode", "string", "center")])
T("no-drag-maximise", "windows", "Don't maximise when dragged to the top", "Dragging a window to the top edge leaves it as it is",
  kde=[("kwinrc", "Windows", "ElectricBorderMaximize", "false")])
T("no-edge-snap", "windows", "Don't snap windows to screen edges", "Turns off side-by-side snapping",
  kde=[("kwinrc", "Windows", "ElectricBorderTiling", "false")], xfce=[("xfwm4", "/general/tile_on_move", "bool", "false", "true")])
T("round-corners", "windows", "Extra-round window corners", "Softer, more rounded windows",
  hypr=["decoration:rounding = 18"], group="corners")
T("square-corners", "windows", "Square window corners", "Sharp corners, no rounding",
  hypr=["decoration:rounding = 0"], group="corners")
T("small-gaps", "windows", "Small gaps between windows", "More space for your apps", hypr=["general:gaps_in = 2", "general:gaps_out = 4"], group="gaps")
T("big-gaps", "windows", "Big gaps between windows", "Airy look with the wallpaper showing between windows",
  hypr=["general:gaps_in = 8", "general:gaps_out = 22"], group="gaps")
T("master-layout", "windows", "One big window plus a stack", "Hyprland's master layout instead of splitting in half",
  hypr=["general:layout = master"])

# ---------------------------------------------------------------------------- glass
T("glass-inactive", "glass", "See-through windows in the background", "Windows you're not using are slightly transparent",
  kde=[("kwinrc", "Plugins", "translucencyEnabled", "true"), ("kwinrc", "Effect-translucency", "Inactive", "88")],
  xfce=[("xfwm4", "/general/inactive_opacity", "int", "88", "100")], hypr=["decoration:inactive_opacity = 0.9"],
  group="glass-level")
T("glass-moving", "glass", "See-through while moving", "Windows become transparent while you drag them",
  kde=[("kwinrc", "Plugins", "translucencyEnabled", "true"), ("kwinrc", "Effect-translucency", "MoveResize", "75")],
  xfce=[("xfwm4", "/general/move_opacity", "int", "80", "100")])
T("glass-all", "glass", "Glass mode: see-through everything",
  "Every window lets a little frosted wallpaper through, the dock and terminal too. Videos, games and "
  "photo apps stay solid, so they still look right",
  kde=[("kwinrc", "Plugins", "blurEnabled", "true")],
  kde_js=("panels().forEach(function(p){ p.opacity = 'translucent'; });",
          "panels().forEach(function(p){ p.opacity = 'adaptive'; });"),
  xfce=[("xfwm4", "/general/inactive_opacity", "int", "86", "100"), ("xfwm4", "/general/frame_opacity", "int", "88", "100"),
        ("xfwm4", "/general/popup_opacity", "int", "92", "100"), ("xfwm4", "/general/move_opacity", "int", "85", "100")],
  hypr=["decoration:active_opacity = 0.93", "decoration:inactive_opacity = 0.86",
        "decoration:blur:enabled = true", "decoration:blur:size = 7", "decoration:blur:passes = 3",
        "decoration:blur:noise = 0.02", "decoration:blur:vibrancy = 0.2",
        "windowrulev2 = opaque, fullscreen:1",
        "windowrulev2 = opaque, class:^(mpv|vlc|celluloid|io.github.celluloid_player.Celluloid|steam|steam_app_.*|"
        "gamescope|com.obsproject.Studio|obs|gimp|org.gimp.GIMP|krita|org.kde.krita|kdenlive|org.kde.kdenlive|"
        "darktable|blender|org.kde.gwenview|loupe|org.gnome.Loupe)$"],
  func="glass_all", group="glass-level")
T("glass-always", "glass", "See-through all the time",
  "Every window is see-through, always: the one you're using, background windows, videos, games and full-screen "
  "apps. Strong frosted blur behind, the dock and terminal too",
  kde=[("kwinrc", "Plugins", "blurEnabled", "true")],
  kde_js=("panels().forEach(function(p){ p.opacity = 'translucent'; });",
          "panels().forEach(function(p){ p.opacity = 'adaptive'; });"),
  hypr=["decoration:active_opacity = 0.85", "decoration:inactive_opacity = 0.85", "decoration:fullscreen_opacity = 0.85",
        "decoration:blur:enabled = true", "decoration:blur:size = 8", "decoration:blur:passes = 3",
        "decoration:blur:noise = 0.02", "decoration:blur:vibrancy = 0.2"],
  func="glass_always", group="glass-level")
T("glass-menus", "glass", "See-through menus", "Menus and pop-ups let the window behind show through",
  kde=[("kwinrc", "Plugins", "translucencyEnabled", "true"), ("kwinrc", "Effect-translucency", "Menus", "88"),
       ("kwinrc", "Effect-translucency", "DropdownMenus", "88"), ("kwinrc", "Effect-translucency", "PopupMenus", "88")])
T("glass-titlebars", "glass", "See-through title bars", "Title bars let the content behind show through",
  kde=[("kwinrc", "Plugins", "translucencyEnabled", "true"), ("kwinrc", "Effect-translucency", "Decoration", "80")],
  xfce=[("xfwm4", "/general/frame_opacity", "int", "85", "100")])
T("blur", "glass", "Blur behind see-through things", "Frosted glass behind menus, the dock and transparent windows",
  kde=[("kwinrc", "Plugins", "blurEnabled", "true")], hypr=["decoration:blur:enabled = true", "decoration:blur:size = 8",
                                                              "decoration:blur:passes = 2"])
T("strong-blur", "glass", "Strong blur", "Extra frosty glass",
  kde=[("kwinrc", "Plugins", "blurEnabled", "true"), ("kwinrc", "Effect-blur", "BlurStrength", "14")],
  hypr=["decoration:blur:enabled = true", "decoration:blur:size = 12", "decoration:blur:passes = 3"])
T("glass-dock", "glass", "See-through dock", "The dock lets the wallpaper show through",
  kde_js=("panels().forEach(function(p){ p.opacity = 'translucent'; });",
          "panels().forEach(function(p){ p.opacity = 'adaptive'; });"), group="dock-opacity")
T("solid-dock", "glass", "Solid dock", "An opaque dock that's always easy to read",
  kde_js=("panels().forEach(function(p){ p.opacity = 'opaque'; });",
          "panels().forEach(function(p){ p.opacity = 'adaptive'; });"), group="dock-opacity")
T("glass-bar", "glass", "See-through top bar", "Waybar lets the wallpaper show through",
  lines={"~/.config/waybar/style.css": ["window#waybar { background: rgba(36, 42, 50, 0.55); }"]},
  func="waybar_reload")

# ---------------------------------------------------------------------------- motion
T("wobbly", "motion", "Wobbly windows", "Windows wobble like jelly when you move them",
  kde=[("kwinrc", "Plugins", "wobblywindowsEnabled", "true")])
T("magic-lamp", "motion", "Magic lamp minimise", "Windows pour into the dock like a genie when you minimise, like a Mac",
  kde=[("kwinrc", "Plugins", "magiclampEnabled", "true"), ("kwinrc", "Plugins", "squashEnabled", "false")])
T("glide", "motion", "Windows glide in and out", "A smooth 3D glide when windows open and close",
  kde=[("kwinrc", "Plugins", "glideEnabled", "true"), ("kwinrc", "Plugins", "scaleEnabled", "false")],
  group="close-anim")
T("fall-apart", "motion", "Closed windows fall apart", "Windows break into pieces when you close them",
  kde=[("kwinrc", "Plugins", "fallapartEnabled", "true")], group="close-anim")
T("fade-desktops", "motion", "Fade between workspaces", "Fade instead of sliding when you switch workspace",
  kde=[("kwinrc", "Plugins", "fadedesktopEnabled", "true"), ("kwinrc", "Plugins", "slideEnabled", "false")],
  hypr=["animation = workspaces, 1, 5, default, fade"])
T("bouncy", "motion", "Bouncy animations", "Windows pop open with a little bounce",
  hypr=["bezier = deviumBounce, 0.05, 0.9, 0.1, 1.08", "animation = windows, 1, 5, deviumBounce, popin 80%"])
T("fast-anim", "motion", "Faster animations", "Everything moves twice as fast",
  kde=[("kdeglobals", "KDE", "AnimationDurationFactor", "0.5")], hypr=["animations:first_launch_animation = false",
                                                                      "animation = global, 1, 3, default"], group="speed")
T("slow-anim", "motion", "Slower, smoother animations", "Relaxed, smooth motion",
  kde=[("kdeglobals", "KDE", "AnimationDurationFactor", "1.5")], hypr=["animation = global, 1, 9, default"], group="speed")
T("no-anim", "motion", "No animations", "Instant, nothing moves. Fastest on old computers",
  kde=[("kdeglobals", "KDE", "AnimationDurationFactor", "0")], hypr=["animations:enabled = false"], group="speed")
T("dim-inactive", "motion", "Dim windows you're not using", "The window you're using stands out",
  kde=[("kwinrc", "Plugins", "diminactiveEnabled", "true")], hypr=["decoration:dim_inactive = true", "decoration:dim_strength = 0.12"])
T("dim-admin", "motion", "Dim the screen for password prompts", "The screen dims when an app asks for your password",
  kde=[("kwinrc", "Plugins", "dimscreenEnabled", "true")])
T("sheet-dialogs", "motion", "Dialogs slide down from the window", "Like a Mac, dialogs come out of the title bar",
  kde=[("kwinrc", "Plugins", "sheetEnabled", "true")])
T("mouse-click", "motion", "Show mouse clicks", "A ring where you click: great for videos and teaching",
  kde=[("kwinrc", "Plugins", "mouseclickEnabled", "true")])
T("snap-helper", "motion", "Show the centre while moving", "Lines show the middle of the screen as you move a window",
  kde=[("kwinrc", "Plugins", "snaphelperEnabled", "true")])

# ---------------------------------------------------------------------------- desktop
T("corner-overview", "desktop", "Top-left corner: see all windows", "Push the mouse into the top-left corner",
  kde=[("kwinrc", "Effect-overview", "BorderActivate", "7")])
T("corner-desktop", "desktop", "Bottom-right corner: show the desktop", "Push the mouse into the bottom-right corner",
  kde=[("kwinrc", "ElectricBorders", "BottomRight", "ShowDesktop")])
T("corner-lock", "desktop", "Top-right corner: lock the screen", "Push the mouse into the top-right corner",
  kde=[("kwinrc", "ElectricBorders", "TopRight", "LockScreen")])
T("corner-launcher", "desktop", "Bottom-left corner: open the app menu", "Push the mouse into the bottom-left corner",
  kde=[("kwinrc", "ElectricBorders", "BottomLeft", "ApplicationLauncher")])
T("four-desktops", "desktop", "Four workspaces", "Four desktops to spread your windows over (Ctrl+F1–F4)",
  kde=[("kwinrc", "Desktops", "Number", "4"), ("kwinrc", "Desktops", "Rows", "1")],
  xfce=[("xfwm4", "/general/workspace_count", "int", "4", "1")])
T("dock-edge", "desktop", "Dock touches the bottom edge", "A classic dock instead of a floating one",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom') p.floating = false; });",
          "panels().forEach(function(p){ if (p.location=='bottom') p.floating = true; });"))
T("dock-autohide", "desktop", "Hide the dock until you need it", "Push the mouse to the bottom to show it",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom') p.hiding = 'autohide'; });",
          "panels().forEach(function(p){ if (p.location=='bottom') p.hiding = 'none'; });"), group="dock-hide")
T("dock-dodge", "desktop", "Dock moves out of the way of windows", "Hides only when a window would cover it",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom') p.hiding = 'dodgewindows'; });",
          "panels().forEach(function(p){ if (p.location=='bottom') p.hiding = 'none'; });"), group="dock-hide")
T("dock-big", "desktop", "Bigger dock", "Larger dock and app icons",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom') p.height = Math.round(gridUnit * 3.6); });",
          "panels().forEach(function(p){ if (p.location=='bottom') p.height = Math.round(gridUnit * 2.8); });"))
T("no-desktop-icons", "desktop", "Clean desktop (no icons)", "Hide files and folders on the desktop",
  xfce=[("xfce4-desktop", "/desktop-icons/style", "int", "0", "2")])
T("wallpaper-dim-dark", "desktop", "Darker wallpaper", "Dims the wallpaper a little so windows stand out",
  func="dim_wallpaper")

# ---------------------------------------------------------------------------- clock
T("clock-seconds", "clock", "Show seconds on the clock", "",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showSeconds', 2); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showSeconds', 0); }); });"),
  func="waybar_clock")
T("clock-12h", "clock", "12-hour clock (AM / PM)", "",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('use24hFormat', 0); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('use24hFormat', 1); }); });"))
T("clock-date", "clock", "Show the date next to the time", "",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showDate', true); w.writeConfig('dateDisplayFormat', 'BesideTime'); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showDate', false); }); });"))
T("notify-top", "clock", "Notifications at the top right", "Like a Mac",
  kde=[("plasmanotifyrc", "Notifications", "PopupPosition", "TopRight")],
  xfce=[("xfce4-notifyd", "/notify-location", "int", "2")], group="notify-pos")
T("notify-bottom", "clock", "Notifications at the bottom right", "Like Windows",
  kde=[("plasmanotifyrc", "Notifications", "PopupPosition", "BottomRight")],
  xfce=[("xfce4-notifyd", "/notify-location", "int", "3")], group="notify-pos")
T("notify-short", "clock", "Notifications go away faster", "Pop-ups disappear after 3 seconds",
  kde=[("plasmanotifyrc", "Notifications", "PopupTimeout", "3000")], xfce=[("xfce4-notifyd", "/expire-timeout", "int", "3")])
T("no-sounds", "clock", "No system sounds", "Silence the little beeps and event sounds",
  kde=[("kdeglobals", "Sounds", "Enable", "false")], xfce=[("xsettings", "/Net/EnableEventSounds", "bool", "false")])
T("no-badges", "clock", "No unread badges on dock icons", "Hide the little number bubbles",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('smartLaunchersEnabled', false); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('smartLaunchersEnabled', true); }); });"))

# ---------------------------------------------------------------------------- mouse
T("single-click", "mouse", "Open files with one click", "Like links on a web page",
  kde=[("kdeglobals", "KDE", "SingleClick", "true")], xfce=[("thunar", "/misc-single-click", "bool", "true")])
T("big-cursor", "mouse", "Bigger mouse pointer", "Easier to see",
  kde=[("kcminputrc", "Mouse", "cursorSize", "36")], xfce=[("xsettings", "/Gtk/CursorThemeSize", "int", "36")],
  hypr=["env = XCURSOR_SIZE,36", "env = HYPRCURSOR_SIZE,36"], group="cursor")
T("huge-cursor", "mouse", "Huge mouse pointer", "Very easy to see",
  kde=[("kcminputrc", "Mouse", "cursorSize", "48")], xfce=[("xsettings", "/Gtk/CursorThemeSize", "int", "48")],
  hypr=["env = XCURSOR_SIZE,48", "env = HYPRCURSOR_SIZE,48"], group="cursor")
T("shake-cursor", "mouse", "Shake the mouse to find it", "The pointer grows when you shake the mouse",
  kde=[("kwinrc", "Plugins", "shakecursorEnabled", "true")])
T("hide-cursor-typing", "mouse", "Hide the pointer while typing", "It comes back when you move the mouse",
  kde=[("kwinrc", "Plugins", "hidecursorEnabled", "true"), ("kwinrc", "Effect-hidecursor", "HideOnTyping", "true")],
  hypr=["cursor:hide_on_key_press = true"])
T("focus-follows", "mouse", "Focus follows the mouse", "The window under the pointer becomes active, no click needed",
  kde=[("kwinrc", "Windows", "FocusPolicy", "FocusFollowsMouse")], xfce=[("xfwm4", "/general/click_to_focus", "bool", "false", "true")])
T("natural-scroll", "mouse", "Natural scrolling", "Content follows your fingers, like a phone or a Mac",
  xfce=[("pointers", "/Natural_scrolling", "bool", "true")], hypr=["input:natural_scroll = true", "input:touchpad:natural_scroll = true"],
  func="kde_natural_scroll")
T("tap-click", "mouse", "Tap the touchpad to click", "No need to press it down",
  hypr=["input:touchpad:tap-to-click = true"], func="kde_tap_click")

# ---------------------------------------------------------------------------- terminal
T("term-glass", "terminal", "See-through terminal", "The terminal lets your wallpaper show through",
  lines={"~/.config/kitty/kitty.conf": ["background_opacity 0.86"]},
  xfce=[("xfce4-terminal", "/background-mode", "string", "TERMINAL_BACKGROUND_TRANSPARENT"),
        ("xfce4-terminal", "/background-darkness", "double", "0.86")], func="konsole_glass")
T("term-big-font", "terminal", "Bigger terminal text", "Easier to read code",
  lines={"~/.config/kitty/kitty.conf": ["font_size 13.0"]}, xfce=[("xfce4-terminal", "/font-use-system", "bool", "false"), ("xfce4-terminal", "/font-name", "string", "JetBrains Mono 13")],
  func="konsole_font")
T("term-block-cursor", "terminal", "Blinking block cursor", "A classic chunky blinking cursor",
  lines={"~/.config/kitty/kitty.conf": ["cursor_shape block", "cursor_blink_interval 0.6"]},
  xfce=[("xfce4-terminal", "/misc-cursor-shape", "string", "TERMINAL_CURSOR_SHAPE_BLOCK"),
        ("xfce4-terminal", "/misc-cursor-blinks", "bool", "true")])
T("term-padding", "terminal", "Roomy terminal", "More space around the text",
  lines={"~/.config/kitty/kitty.conf": ["window_padding_width 14"]})

# ---------------------------------------------------------------------------- comfort
T("night-light", "comfort", "Night light", "Warmer colours in the evening, easier on your eyes and sleep",
  kde=[("kwinrc", "NightColor", "Active", "true"), ("kwinrc", "NightColor", "Mode", "Automatic"),
       ("kwinrc", "NightColor", "NightTemperature", "4200")], group="night")
T("night-always", "comfort", "Warm colours all day", "Always a little warmer, never harsh blue",
  kde=[("kwinrc", "NightColor", "Active", "true"), ("kwinrc", "NightColor", "Mode", "Constant"),
       ("kwinrc", "NightColor", "NightTemperature", "5000")], group="night")
T("accent-wallpaper", "comfort", "Accent colour from the wallpaper", "The highlight colour matches your wallpaper",
  kde=[("kdeglobals", "General", "accentColorFromWallpaper", "true")])
T("compact-text", "comfort", "Smaller text", "Fits more on the screen",
  kde=[("kdeglobals", "General", "font", "Noto Sans,9,-1,5,400,0,0,0,0,0,0,0,0,0,0,1")],
  xfce=[("xsettings", "/Gtk/FontName", "string", "Noto Sans 9")], group="text")
T("large-text", "comfort", "Larger text", "Easier to read",
  kde=[("kdeglobals", "General", "font", "Noto Sans,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1")],
  xfce=[("xsettings", "/Gtk/FontName", "string", "Noto Sans 12")], group="text")
T("bold-titles", "comfort", "Bold window titles", "Titles stand out more",
  kde=[("kdeglobals", "WM", "activeFont", "Noto Sans,10,-1,5,700,0,0,0,0,0,0,0,0,0,0,1")],
  xfce=[("xfwm4", "/general/title_font", "string", "Noto Sans Bold 10")])
T("high-contrast-borders", "comfort", "Easy-to-see window outlines", "A strong outline around every window",
  kde=[("breezerc", "Common", "OutlineIntensity", "OutlineHigh")], hypr=["general:col.inactive_border = rgb(8a96a4)"])


# ---------------------------------------------------------------------------- touchpad gestures (beta17)
T("gnome-gestures", "gestures", "Three-finger gestures like GNOME",
  "Swipe up with three fingers for the overview, down for the desktop, left and right to change workspace "
  "(a new one appears past the last, like GNOME). KDE's four-finger gestures keep working",
  kde=[("kwinrc", "Plugins", "devium-gesturesEnabled", "true", "false")],
  hypr=["gesture = 3, horizontal, workspace"])


# ---------------------------------------------------------------------------- tiling (beta16)
T("tiling", "tiling", "Automatic tiling (like Hyprland)",
  "New windows split the screen by themselves, with gaps. Meta+Shift+Space floats a window, Meta+Shift+T turns "
  "tiling off for a moment, Meta+Alt+arrows swap windows, drag one onto another to swap them",
  kde=[("kwinrc", "Plugins", "devium-tilingEnabled", "true", "false"),
       ("kwinrc", "Plugins", "devium-snap-assistEnabled", "false", "true")])
T("tiling-master", "tiling", "Tiling: one big window and a stack", "The first window takes the left side, the rest stack on the right",
  kde=[("kwinrc", "Script-devium-tiling", "layout", "master")])
T("tiling-no-gaps", "tiling", "Tiling: no gaps", "Windows touch each other, for the most space",
  kde=[("kwinrc", "Script-devium-tiling", "gap", "0")], group="tile-gaps")
T("tiling-big-gaps", "tiling", "Tiling: big gaps", "Lots of wallpaper between windows",
  kde=[("kwinrc", "Script-devium-tiling", "gap", "22")], group="tile-gaps")

# ---------------------------------------------------------------------------- more windows
T("no-titlebars", "windows", "No title bars at all", "Clean, borderless windows. Close them with Alt+F4 or the dock",
  func="no_titlebars")
T("small-buttons", "windows", "Smaller title bar buttons", "Slimmer title bars",
  kde=[("breezerc", "Windeco", "ButtonSize", "ButtonSmall")], group="button-size")
T("big-borders", "windows", "Wide window borders", "Easier to grab a window's edge to resize it",
  kde=[("kwinrc", DECO, "BorderSize", "Large"), ("kwinrc", DECO, "BorderSizeAuto", "false")], group="borders")
T("switcher-grid", "windows", "Alt+Tab shows big previews", "A grid of window thumbnails when you press Alt+Tab",
  kde=[("kwinrc", "TabBox", "LayoutName", "thumbnail_grid")], group="tabbox")
T("switcher-cover", "windows", "Alt+Tab: cover switch", "Windows flip past in 3D, like album covers",
  kde=[("kwinrc", "TabBox", "LayoutName", "coverswitch")], group="tabbox")
T("switcher-flip", "windows", "Alt+Tab: flip switch", "Windows stacked in 3D that you flip through",
  kde=[("kwinrc", "TabBox", "LayoutName", "flipswitch")], group="tabbox")
T("switcher-all", "windows", "Alt+Tab shows every workspace", "Switch to windows on other workspaces too",
  kde=[("kwinrc", "TabBox", "DesktopMode", "0")])

# ---------------------------------------------------------------------------- dock and desktop
T("dock-left", "desktop", "Dock on the left", "The dock stands on the left side of the screen",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom' || p.location=='top') p.location='left'; });",
          "panels().forEach(function(p){ if (p.location=='left') p.location='bottom'; });"), group="dock-pos")
T("dock-top", "desktop", "Dock at the top", "The dock sits along the top of the screen",
  kde_js=("panels().forEach(function(p){ if (p.location=='bottom' || p.location=='left') p.location='top'; });",
          "panels().forEach(function(p){ if (p.location=='top' && p.widgets('org.kde.plasma.appmenu').length==0) p.location='bottom'; });"),
  group="dock-pos")
T("mac-top-bar", "desktop", "macOS-style top bar", "A thin bar at the top with the app's menus, the clock and the tray",
  kde_js=("var have=false; panels().forEach(function(p){ if (p.widgets('org.kde.plasma.appmenu').length) have=true; });"
          "if (!have) { var p = new Panel; p.location='top'; p.height=Math.round(gridUnit*1.6);"
          "p.addWidget('org.kde.plasma.kickoff'); p.addWidget('org.kde.plasma.appmenu');"
          "p.addWidget('org.kde.plasma.panelspacer'); p.addWidget('org.kde.plasma.systemtray');"
          "p.addWidget('org.kde.plasma.digitalclock'); }",
          "panels().forEach(function(p){ if (p.location=='top' && p.widgets('org.kde.plasma.appmenu').length) p.remove(); });"))
T("home-pages", "desktop", "Home screen pages (like iPhone)",
  "Pages of apps and widgets on your desktop that you swipe between. Press and hold (or Edit) to add apps, "
  "widgets and pages; icons wiggle, \u2715 removes them",
  kde_js=("desktops().forEach(function(d){ if (d.widgets('org.devium.home').length == 0) {"
          " var g = screenGeometry(d.screen);"
          " d.addWidget('org.devium.home', 0, 0, g.width, g.height - Math.round(gridUnit * 5)); } });",
          "desktops().forEach(function(d){ d.widgets('org.devium.home').forEach(function(w){ w.remove(); }); });"))
T("dock-this-desktop", "desktop", "Dock shows only this workspace's windows", "Windows on other workspaces don't appear in the dock",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('showOnlyCurrentDesktop', true); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('showOnlyCurrentDesktop', false); }); });"))
T("dock-no-grouping", "desktop", "Don't group windows in the dock", "Every window gets its own dock icon",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('groupingStrategy', 0); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.icontasks').forEach(function(w){ w.currentConfigGroup=['General']; w.writeConfig('groupingStrategy', 1); }); });"))
T("empty-session", "desktop", "Start with a clean desktop", "Don't reopen the apps you had open last time",
  kde=[("ksmserverrc", "General", "loginMode", "emptySession")])
T("no-logout-confirm", "desktop", "Log out and shut down without asking", "No \"are you sure?\" screen",
  kde=[("ksmserverrc", "General", "confirmLogout", "false")])

# ---------------------------------------------------------------------------- clock, sound, notifications
T("week-numbers", "clock", "Week numbers in the calendar", "",
  kde_js=("panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showWeekNumbers', true); }); });",
          "panels().forEach(function(p){ p.widgets('org.kde.plasma.digitalclock').forEach(function(w){ w.currentConfigGroup=['Appearance']; w.writeConfig('showWeekNumbers', false); }); });"))
T("quiet-fullscreen", "clock", "No pop-ups over full-screen apps", "Notifications wait while you watch a video or play a game",
  kde=[("plasmanotifyrc", "DoNotDisturb", "WhenFullscreen", "true")])
T("louder", "keyboard", "Allow volume up to 150%", "For quiet laptop speakers",
  kde=[("plasmaparc", "General", "RaiseMaximumVolume", "true")])
T("silent-volume-keys", "keyboard", "No click when changing the volume", "Silence the little sound the volume keys make",
  kde=[("plasmaparc", "General", "AudioFeedback", "false")])

# ---------------------------------------------------------------------------- keyboard
T("numlock", "keyboard", "Num Lock on when you log in", "The number pad works straight away",
  kde=[("kcminputrc", "Keyboard", "NumLock", "0")], xfce=[("keyboards", "/Default/Numlock", "bool", "true")],
  hypr=["input:numlock_by_default = true"])
T("fast-repeat", "keyboard", "Faster key repeat", "Holding a key repeats it sooner and faster",
  kde=[("kcminputrc", "Keyboard", "RepeatDelay", "250"), ("kcminputrc", "Keyboard", "RepeatRate", "40")],
  xfce=[("keyboards", "/Default/KeyRepeat/Delay", "int", "250"), ("keyboards", "/Default/KeyRepeat/Rate", "int", "40")],
  hypr=["input:repeat_delay = 250", "input:repeat_rate = 40"])
T("caps-escape", "keyboard", "Caps Lock works as Escape", "Popular with Vim users",
  kde=[("kxkbrc", "Layout", "Options", "caps:escape"), ("kxkbrc", "Layout", "ResetOldOptions", "true")],
  hypr=["input:kb_options = caps:escape"], group="xkb")
T("caps-ctrl", "keyboard", "Swap Caps Lock and Ctrl", "Ctrl where Caps Lock is, easier on your hands",
  kde=[("kxkbrc", "Layout", "Options", "ctrl:swapcaps"), ("kxkbrc", "Layout", "ResetOldOptions", "true")],
  hypr=["input:kb_options = ctrl:swapcaps"], group="xkb")
T("compose-key", "keyboard", "Right Alt is a compose key", "Type é, ñ, ü and more: Right Alt, then ' and e",
  kde=[("kxkbrc", "Layout", "Options", "compose:ralt"), ("kxkbrc", "Layout", "ResetOldOptions", "true")],
  hypr=["input:kb_options = compose:ralt"], group="xkb")

# ---------------------------------------------------------------------------- mouse
T("fast-pointer", "mouse", "Faster mouse pointer", "The pointer moves further for the same hand movement",
  hypr=["input:sensitivity = 0.45"], func="kde_fast_pointer")
T("left-handed", "mouse", "Left-handed mouse", "Swap the left and right buttons",
  xfce=[("pointers", "/Default/RightHanded", "bool", "false")], hypr=["input:left_handed = true"], func="kde_left_handed")

# ---------------------------------------------------------------------------- power and lock screen
T("lock-5min", "power", "Lock the screen after 5 minutes", "When you step away",
  kde=[("kscreenlockerrc", "Daemon", "Autolock", "true"), ("kscreenlockerrc", "Daemon", "Timeout", "5")], group="lock")
T("lock-never", "power", "Never lock the screen by itself", "Only when you lock it (Meta+L)",
  kde=[("kscreenlockerrc", "Daemon", "Autolock", "false")], group="lock")
T("lock-no-resume", "power", "Don't lock after sleep", "Opening the lid takes you straight back in",
  kde=[("kscreenlockerrc", "Daemon", "LockOnResume", "false")])
T("screen-off-10", "power", "Turn the screen off after 10 minutes", "Saves power when you're away",
  kde=[("powerdevilrc", "AC|Display", "TurnOffDisplayIdleTimeoutSec", "600"),
       ("powerdevilrc", "Battery|Display", "TurnOffDisplayIdleTimeoutSec", "600")])
T("no-sleep-ac", "power", "Never sleep when plugged in", "Good for downloads and long builds",
  kde=[("powerdevilrc", "AC|SuspendAndShutdown", "AutoSuspendAction", "0")])
T("lid-ac-nothing", "power", "Closing the lid does nothing when plugged in", "Use the laptop with an external screen",
  kde=[("powerdevilrc", "AC|SuspendAndShutdown", "LidAction", "0")])

# ---------------------------------------------------------------------------- files
T("dolphin-split", "files", "File manager opens in split view", "Two folders side by side, handy for copying",
  kde=[("dolphinrc", "General", "SplitView", "true")])
T("dolphin-path", "files", "Show the full folder path", "The location bar shows the whole path as text",
  kde=[("dolphinrc", "General", "ShowFullPath", "true")])
T("hidden-files", "files", "Show hidden files", "Files starting with a dot (like .config) are shown",
  xfce=[("thunar", "/last-show-hidden", "bool", "true")], func="dolphin_hidden")
T("thunar-path", "files", "Full path in the window title", "Thunar shows where you are in the title",
  xfce=[("thunar", "/misc-full-path-in-window-title", "bool", "true")])

# ---------------------------------------------------------------------------- comfort
T("colourblind", "comfort", "Colour-blind friendly colours", "Adjusts colours so red and green are easier to tell apart",
  kde=[("kwinrc", "Plugins", "colorblindnesscorrectionEnabled", "true")])
T("invert", "comfort", "Invert colours with Meta+Ctrl+I", "Turns the screen negative, for very bright light or low vision",
  kde=[("kwinrc", "Plugins", "invertEnabled", "true")])

# ---------------------------------------------------------------------------- Xfce
T("xfce-no-compositor", "glass", "Turn off visual effects (Xfce)", "No shadows or transparency: fastest on old laptops",
  xfce=[("xfwm4", "/general/use_compositing", "bool", "false", "true")])
T("xfce-snap-windows", "windows", "Windows snap to each other", "Dragged windows line up with nearby windows",
  xfce=[("xfwm4", "/general/snap_to_windows", "bool", "true")])
T("xfce-shade", "windows", "Double-click a title bar to roll it up", "The window shrinks to just its title bar",
  xfce=[("xfwm4", "/general/double_click_action", "string", "shade")])

# ---------------------------------------------------------------------------- helpers
def run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20, **kw)
    except (OSError, subprocess.TimeoutExpired):
        return None


def kset(file, group, key, value):
    """Write (or with value None, delete) a KDE setting. Nested groups are written "AC|Display"."""
    tool = shutil.which("kwriteconfig6") or "kwriteconfig6"
    cmd = [tool, "--notify", "--file", file]
    for g in group.split("|"):
        cmd += ["--group", g]
    cmd += ["--key", key]
    run(cmd + (["--delete"] if value is None else [value]))


def xset(channel, prop, typ, value):
    if value is None:
        run(["xfconf-query", "-c", channel, "-p", prop, "-r"])
    else:
        run(["xfconf-query", "-c", channel, "-p", prop, "-n", "-t", typ, "-s", value])


def plasma_js(js):
    for q in ("qdbus6", "qdbus"):
        if shutil.which(q):
            run([q, "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", js])
            return


def edit_lines(path, tag, lines, on):
    """Add (or remove) lines marked with '# devium-look:<tag>' in a config file."""
    path = os.path.expanduser(path)
    mark = f"devium-look:{tag}"
    try:
        text = open(path).read()
    except OSError:
        text = None
    if text is None and not on:
        return
    if text is None and not os.path.isdir(os.path.dirname(path)):
        return   # that app isn't set up here
    comment = "/* " + mark + " */" if path.endswith(".css") else "# " + mark
    kept = [l for l in (text or "").splitlines() if mark not in l]
    if on:
        kept += [f"{l}  {comment}" for l in lines]
    with open(path, "w") as f:
        f.write("\n".join(kept).rstrip("\n") + "\n")


def hypr_lines(tag, lines, on):
    os.makedirs(os.path.dirname(HYPR_FILE), exist_ok=True)
    if not os.path.exists(HYPR_FILE):
        open(HYPR_FILE, "w").write("# Devium look tweaks (Devium Configure > Customise). Changed by Devium; edit freely.\n")
    edit_lines(HYPR_FILE, tag, lines, on)
    main = os.path.join(CFG, "hypr", "hyprland.conf")   # make sure it's read
    try:
        text = open(main).read()
        if "devium-look.conf" not in text:
            open(main, "a").write("\n# Devium look tweaks\nsource = ~/.config/hypr/devium-look.conf\n")
    except OSError:
        pass


# ---- the more involved ones ---------------------------------------------------------------
def konsole_profile():
    name = run([shutil.which("kreadconfig6") or "kreadconfig6", "--file", "konsolerc", "--group", "Desktop Entry",
                "--key", "DefaultProfile"])
    name = (name.stdout.strip() if name else "") or "Devium.profile"
    user = os.path.join(HOME, ".local/share/konsole", name)
    if not os.path.exists(user):
        for d in ("/usr/share/konsole",):
            if os.path.exists(os.path.join(d, name)):
                os.makedirs(os.path.dirname(user), exist_ok=True)
                shutil.copy(os.path.join(d, name), user)
    return user if os.path.exists(user) else None


def konsole_glass(on):
    if not shutil.which("konsole"):
        return
    prof = konsole_profile()
    if not prof:
        return
    import configparser
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    cp.optionxform = str
    cp.read(prof)
    scheme = cp.get("Appearance", "ColorScheme", fallback="Breeze")
    base = scheme[:-5] if scheme.endswith("Glass") else scheme
    if on:
        src = next((p for p in (os.path.join(HOME, ".local/share/konsole", base + ".colorscheme"),
                                f"/usr/share/konsole/{base}.colorscheme") if os.path.exists(p)), None)
        if not src:
            return
        sc = configparser.ConfigParser(interpolation=None, strict=False)
        sc.optionxform = str
        sc.read(src)
        if not sc.has_section("General"):
            sc.add_section("General")
        sc.set("General", "Opacity", "0.86")
        sc.set("General", "Blur", "true")
        sc.set("General", "Description", base + " Glass")
        with open(os.path.join(HOME, ".local/share/konsole", base + "Glass.colorscheme"), "w") as f:
            sc.write(f, space_around_delimiters=False)
        new = base + "Glass"
    else:
        new = base
    if not cp.has_section("Appearance"):
        cp.add_section("Appearance")
    cp.set("Appearance", "ColorScheme", new)
    with open(prof, "w") as f:
        cp.write(f, space_around_delimiters=False)


def konsole_font(on):
    if not shutil.which("konsole"):
        return
    prof = konsole_profile()
    if prof:
        kset(prof, "Appearance", "Font", "JetBrains Mono,13,-1,5,400,0,0,0,0,0,0,0,0,0,0,1" if on else None)


def kde_input(key, on, value=None):
    """Natural scrolling / tap to click / pointer speed... for every touchpad and mouse KDE knows about."""
    if not KDE:
        return
    path = os.path.join(CFG, "kcminputrc")
    try:
        groups = re.findall(r"^\[(Libinput\]\[[^\n]+)\]$", open(path).read(), re.M)
    except OSError:
        groups = []
    for g in groups:
        parts = g.split("][")
        cmd = [shutil.which("kwriteconfig6") or "kwriteconfig6", "--file", "kcminputrc"]
        for p in parts:
            cmd += ["--group", p]
        if value is not None:
            run(cmd + ["--key", key] + ([value] if on else ["--delete"]))
        else:
            run(cmd + ["--key", key, "true" if on else "false"])


def kde_natural_scroll(on):
    kde_input("NaturalScroll", on)


def kde_fast_pointer(on):
    kde_input("PointerAcceleration", on, "0.45")


def kde_left_handed(on):
    kde_input("LeftHanded", on)


def kwin_rule(rule_id, props):
    """Add (props = dict) or remove (props = None) one KWin window rule, keeping everyone else's rules."""
    if not KDE:
        return
    import configparser
    path = os.path.join(CFG, "kwinrulesrc")
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    cp.optionxform = str
    cp.read(path)
    if not cp.has_section("General"):
        cp.add_section("General")
    rules = [r for r in cp.get("General", "rules", fallback="").split(",") if r and r != rule_id]
    if cp.has_section(rule_id):
        cp.remove_section(rule_id)
    if props:
        cp[rule_id] = props
        rules.append(rule_id)
    cp.set("General", "rules", ",".join(rules))
    cp.set("General", "count", str(len(rules)))
    with open(path, "w") as f:
        cp.write(f, space_around_delimiters=False)


def no_titlebars(on):
    kwin_rule("devium-noborder", {"Description": "Devium: no title bars (close windows with Alt+F4)", "wmclass": ".*",
                                  "wmclassmatch": "3", "wmclasscomplete": "false", "types": "1",
                                  "noborder": "true", "noborderrule": "2"} if on else None)


def dolphin_hidden(on):
    if KDE:
        kset("dolphinrc", "General", "GlobalViewProps", "true" if on else None)
        path = os.path.join(HOME, ".local/share/dolphin/view_properties/global/.directory")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        kset(path, "Settings", "HiddenFilesShown", "true" if on else None)


def kde_tap_click(on):
    kde_input("TapToClick", on)


SOLID_APPS = ("mpv|vlc|celluloid|io.github.celluloid_player.Celluloid|steam|steam_app_.*|gamescope|obs|"
              "com.obsproject.Studio|gimp|org.gimp.GIMP|krita|org.kde.krita|kdenlive|org.kde.kdenlive|darktable|"
              "blender|gwenview|org.kde.gwenview|okular|org.kde.okular|spectacle|org.kde.spectacle")


def glass_all(on):
    """KDE: window rules. Videos, games and photo apps stay solid; every other window is 93% (85% in the background)."""
    glass_rules(on, solid=True, active="93", inactive="85")


def glass_always(on):
    """KDE: every window 85% see-through, all the time, no exceptions."""
    glass_rules(on, solid=False, active="85", inactive="85")


def glass_rules(on, solid, active, inactive):
    if KDE:
        kset("kwinrc", "Effect-translucency", "ActiveWindows", None)   # beta15's glass mode used this; not any more
        import configparser
        path = os.path.join(CFG, "kwinrulesrc")
        cp = configparser.ConfigParser(interpolation=None, strict=False)
        cp.optionxform = str
        cp.read(path)
        if not cp.has_section("General"):
            cp.add_section("General")
        rules = [r for r in cp.get("General", "rules", fallback="").split(",") if r and r not in ("devium-solid", "devium-glass")]
        for sec in ("devium-solid", "devium-glass"):
            if cp.has_section(sec):
                cp.remove_section(sec)
        if on and solid:
            cp["devium-solid"] = {"Description": "Devium glass mode: keep videos, games and photo apps solid",
                                  "wmclass": SOLID_APPS, "wmclassmatch": "3", "wmclasscomplete": "false",
                                  "opacityactive": "100", "opacityactiverule": "2",
                                  "opacityinactive": "100", "opacityinactiverule": "2"}
        if on:
            cp["devium-glass"] = {"Description": "Devium: every window see-through",
                                  "wmclass": ".*", "wmclassmatch": "3", "wmclasscomplete": "false", "types": "33",
                                  "opacityactive": active, "opacityactiverule": "2",
                                  "opacityinactive": inactive, "opacityinactiverule": "2"}
            rules = (["devium-solid"] if solid else []) + ["devium-glass"] + rules   # earlier rules win: solid apps first
        cp.set("General", "rules", ",".join(rules))
        cp.set("General", "count", str(len(rules)))
        with open(path, "w") as f:
            cp.write(f, space_around_delimiters=False)
        konsole_glass(on)


def waybar_reload(on):
    run(["pkill", "-SIGUSR2", "waybar"])


def waybar_clock(on):
    path = os.path.join(CFG, "waybar/config.jsonc")
    try:
        text = open(path).read()
    except OSError:
        return
    if on:
        text = text.replace('"{:%H:%M}"', '"{:%H:%M:%S}"').replace('"interval": 60', '"interval": 1')
    else:
        text = text.replace('"{:%H:%M:%S}"', '"{:%H:%M}"')
    open(path, "w").write(text)
    run(["pkill", "-SIGUSR2", "waybar"])


def dim_wallpaper(on):
    """KDE: a darker copy of the Devium wallpaper."""
    if not KDE:
        return
    src = "/usr/share/wallpapers/Devium/contents/images/1920x1080.jpg"
    out = os.path.join(HOME, ".local/share/devium/wallpaper-dim.jpg")
    if on:
        try:
            from PyQt6.QtGui import QGuiApplication, QImage, QPainter, QColor
            app = QGuiApplication.instance() or QGuiApplication(["x"])
            img = QImage(src)
            p = QPainter(img)
            p.fillRect(img.rect(), QColor(10, 14, 20, 90))
            p.end()
            os.makedirs(os.path.dirname(out), exist_ok=True)
            img.save(out, quality=92)
        except Exception:
            return
        target = out
    else:
        target = src
    if shutil.which("plasma-apply-wallpaperimage"):
        run(["plasma-apply-wallpaperimage", target])


# ---------------------------------------------------------------------------- applying
FUNC_DESKTOPS = {"glass_all": "any", "glass_always": "kde", "kde_fast_pointer": "kde", "kde_left_handed": "kde",
                 "no_titlebars": "kde", "dolphin_hidden": "kde", "konsole_glass": "kde", "konsole_font": "kde", "kde_natural_scroll": "kde", "kde_tap_click": "kde",
                 "dim_wallpaper": "kde", "waybar_reload": "hypr", "waybar_clock": "hypr"}


def available(t):
    if KDE:
        return bool(t["kde"] or t["kde_js"] or FUNC_DESKTOPS.get(t["func"]) in ("kde", "any"))
    if XFCE:
        return bool(t["xfce"])
    if HYPR:
        return bool(t["hypr"] or FUNC_DESKTOPS.get(t["func"]) == "hypr" or any("kitty" in k for k in t["lines"]))
    return False


def apply(t, on):
    if KDE:
        for e in t["kde"]:
            file, group, key, val = e[:4]
            off = e[4] if len(e) > 4 else None
            kset(file, group, key, val if on else off)
        if t["kde_js"]:
            plasma_js(t["kde_js"][0 if on else 1])
    if XFCE:
        for e in t["xfce"]:
            ch, prop, typ, val = e[:4]
            off = e[4] if len(e) > 4 else None
            xset(ch, prop, typ, val if on else off)
    if HYPR and t["hypr"]:
        hypr_lines(t["id"], t["hypr"], on)
    for path, lines in t["lines"].items():
        if "kitty" in path or (HYPR and "waybar" in path):
            edit_lines(path, t["id"], lines, on)
    if t["func"]:
        globals()[t["func"]](on)


def finish():
    """Tell the desktop to pick up the changes."""
    if KDE:
        for q in ("qdbus6", "qdbus"):
            if shutil.which(q):
                # restart the tiling script so new gaps / layout apply now (KWin reads script settings at start)
                for script in ("devium-tiling", "devium-gestures"):
                    run([q, "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.unloadScript", script])
                run([q, "org.kde.KWin", "/KWin", "reconfigure"])
                run([q, "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.start"])
                break
    if HYPR:
        run(["hyprctl", "reload"])


def load_state():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(s, f, indent=1, sort_keys=True)


def set_many(pairs):
    state = load_state()
    by_id = {t["id"]: t for t in TWEAKS}
    # turn things off first, so a tweak turned on afterwards wins (e.g. switching button layouts)
    for tid, on in sorted(pairs.items(), key=lambda kv: kv[1]):
        t = by_id.get(tid)
        if not t or not available(t):
            continue
        apply(t, on)
        state[tid] = on
        print(("on:  " if on else "off: ") + t["name"])
    save_state(state)
    finish()


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if a[0] == "list":
        cats = [{"id": c, "name": n, "desc": d} for c, n, d in CATEGORIES]
        print(json.dumps({"categories": cats, "tweaks": [
            {k: t[k] for k in ("id", "cat", "name", "desc", "group")} for t in TWEAKS if available(t)]}))
    elif a[0] == "status":
        print(json.dumps({k: v for k, v in load_state().items() if v}))
    elif a[0] == "set":
        pairs = {}
        for arg in a[1:]:
            k, _, v = arg.partition("=")
            pairs[k] = v.lower() in ("on", "1", "true", "yes")
        set_many(pairs)
    elif a[0] == "reapply":
        set_many({k: True for k, v in load_state().items() if v})
    elif a[0] == "reset":
        set_many({k: False for k, v in load_state().items() if v})
    return 0


if __name__ == "__main__":
    sys.exit(main())