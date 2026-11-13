// Devium default desktop: a big floating dock in the middle of the screen that is exactly as
// wide as its icons (apps | start button | tray), and hides when a window covers it. (ArchPill lives at the top of the screen.)

var dock = new Panel;
dock.location = "bottom";
dock.height = 2 * Math.ceil(gridUnit * 3.4 / 2);   // big icons (part of the Devium theme)
try { dock.floating = true; } catch (e) {}
try { dock.alignment = "center"; } catch (e) {}
try { dock.lengthMode = "fit"; } catch (e) {}       // only as wide as its icons
try { dock.hiding = "dodgewindows"; } catch (e) {}  // hide when a window covers it

var tasks = dock.addWidget("org.kde.plasma.icontasks");   // your apps, left of the start button
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", "applications:org.kde.konsole.desktop");   // just the terminal to start with
tasks.writeConfig("iconSpacing", "2");

var launcher = dock.addWidget("org.kde.plasma.kickoff");  // start button in the middle of the dock
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "/usr/share/devium/start-button.png");

dock.addWidget("org.kde.plasma.marginsseparator");
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
