// Devium default desktop: a big floating bar at the bottom with the start button and apps
// CENTRED (the start menu opens from the middle of the screen), tray and clock on the right.
// It hides when a window covers it. (ArchPill lives at the top of the screen.)

var dock = new Panel;
dock.location = "bottom";
dock.height = 2 * Math.ceil(gridUnit * 3.4 / 2);   // big icons (part of the Devium theme)
try { dock.floating = true; } catch (e) {}
try { dock.alignment = "center"; } catch (e) {}
try { dock.lengthMode = "fill"; } catch (e) {}      // full width, so the middle is the middle
try { dock.hiding = "dodgewindows"; } catch (e) {}  // hide when a window covers it

dock.addWidget("org.kde.plasma.panelspacer");       // flexible space: pushes the apps to the centre

var launcher = dock.addWidget("org.kde.plasma.kickoff");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "/usr/share/devium/start-button.png");

var tasks = dock.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", [
    "preferred://filemanager",
    "preferred://browser",
    "applications:org.kde.konsole.desktop",
    "applications:org.kde.kate.desktop",
    "applications:devium-snip.desktop",
    "applications:org.kde.discover.desktop",
    "applications:devium-welcome.desktop"
].join(","));
tasks.writeConfig("iconSpacing", "2");

dock.addWidget("org.kde.plasma.panelspacer");       // flexible space on the other side
dock.addWidget("org.kde.plasma.systemtray");
dock.addWidget("org.kde.plasma.digitalclock");

var allDesktops = desktops();
for (var i = 0; i < allDesktops.length; i++) {
    var d = allDesktops[i];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    d.writeConfig("Image", "file:///usr/share/wallpapers/Devium/");
    d.writeConfig("FillMode", "2");   // scaled and cropped
}
