// Devium Snap Assist (KWin 6 script)
// 1. Snap a window to the left or right half (drag it to the screen edge, or Meta+Left/Right).
// 2. If other windows are open, KDE shows them (Present Windows): click one and it fills the other half.
//    If not, the next window you open fills the other half.

var pending = null;          // { win, side, area } while waiting for the window for the other half

function halves(area) {
    var w = Math.floor(area.width / 2);
    return {
        left:  { x: area.x,     y: area.y, width: w,              height: area.height },
        right: { x: area.x + w, y: area.y, width: area.width - w, height: area.height }
    };
}

function near(a, b) { return Math.abs(a - b) <= 3; }

// "left" / "right" if the window fills exactly that half of its screen, otherwise null
function snappedSide(win) {
    var area = workspace.clientArea(KWin.MaximizeArea, win);
    var g = win.frameGeometry;
    var h = halves(area);
    if (!near(g.y, area.y) || !near(g.height, area.height) || !near(g.width, h.left.width))
        return null;
    if (near(g.x, h.left.x)) return { side: "left", area: area };
    if (near(g.x, h.right.x)) return { side: "right", area: area };
    return null;
}

function usable(win) {
    return win && win.normalWindow && !win.skipTaskbar && !win.minimized &&
        String(win.resourceClass || "").toLowerCase() !== "devium-spotlight";
}

function otherWindowsOpen(win) {
    var list = workspace.windowList();
    for (var i = 0; i < list.length; i++) {
        var o = list[i];
        if (o !== win && usable(o) && o.output === win.output)
            return true;
    }
    return false;
}

function watch(win) {
    if (!win || !win.normalWindow)
        return;
    win.frameGeometryChanged.connect(function () {
        if (win.move || win.resize)       // still being dragged
            return;
        var s = snappedSide(win);
        if (s) {
            if (pending && pending.win === win && pending.side === s.side)
                return;
            pending = { win: win, side: s.side, area: s.area };
            if (otherWindowsOpen(win)) {
                // show the other windows to pick from (KDE's "Present Windows")
                callDBus("org.kde.kglobalaccel", "/component/kwin", "org.kde.kglobalaccel.Component",
                         "invokeShortcut", "ExposeAll");
            }
        } else if (pending && pending.win === win) {
            pending = null;                // un-snapped: forget it
        }
    });
}

workspace.windowList().forEach(watch);
workspace.windowAdded.connect(watch);

workspace.windowActivated.connect(function (win) {
    if (!pending || !usable(win) || win === pending.win)
        return;
    var h = halves(pending.area);
    var r = pending.side === "left" ? h.right : h.left;
    pending = null;
    if (win.maximizable)
        win.setMaximize(false, false);
    win.frameGeometry = { x: r.x, y: r.y, width: r.width, height: r.height };
});
