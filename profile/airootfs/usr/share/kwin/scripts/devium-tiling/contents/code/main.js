// Devium Tiling (KWin 6 script): automatic tiling like Hyprland's "dwindle" layout.
//  - every new window splits the space of the last one (side by side, then top/bottom, and so on)
//  - gaps around and between windows (Devium Configure > Customise can change them)
//  - dialogs, pop-ups, full-screen and minimised windows are left alone
// Shortcuts (change them in System Settings > Shortcuts > KWin):
//   Meta+Shift+Space   float / tile the active window
//   Meta+Shift+T       tiling on / off
//   Meta+Alt+Left/Right   swap the window with the previous / next one
//   Meta+Alt+Return    make the active window the main (first) one
// Drag a tiled window onto another one to swap them.

var gap = readConfig("gap", 10);
var layout = readConfig("layout", "dwindle");    // "dwindle" or "master"
var masterRatio = 0.55;
var enabled = true;
var order = [];          // tiled windows, in the order they were opened
var floating = {};       // internalId -> true for windows you floated
var busy = false;        // we're moving windows ourselves

function key(w) { return String(w.internalId); }

function onThisDesktop(w) {
    if (w.onAllDesktops) return true;
    var ds = w.desktops || [];
    for (var i = 0; i < ds.length; i++)
        if (ds[i] === workspace.currentDesktop) return true;
    return false;
}

function tileable(w) {
    return w && w.normalWindow && !w.transient && !w.specialWindow && !w.minimized && !w.fullScreen &&
        !w.skipTaskbar && w.resizeable && w.moveable && !floating[key(w)] && onThisDesktop(w);
}

// Split `rect` for n windows. Returns a list of rectangles.
function dwindle(r, n) {
    var out = [];
    for (var i = 0; i < n; i++) {
        if (i === n - 1) { out.push(r); break; }
        var a, b;
        if (r.width >= r.height) {           // split side by side
            var w1 = Math.floor((r.width - gap) / 2);
            a = { x: r.x, y: r.y, width: w1, height: r.height };
            b = { x: r.x + w1 + gap, y: r.y, width: r.width - w1 - gap, height: r.height };
        } else {                             // split top and bottom
            var h1 = Math.floor((r.height - gap) / 2);
            a = { x: r.x, y: r.y, width: r.width, height: h1 };
            b = { x: r.x, y: r.y + h1 + gap, width: r.width, height: r.height - h1 - gap };
        }
        out.push(a);
        r = b;
    }
    return out;
}

// One big window on the left, the rest stacked on the right.
function master(r, n) {
    if (n === 1) return [r];
    var mw = Math.floor((r.width - gap) * masterRatio);
    var out = [{ x: r.x, y: r.y, width: mw, height: r.height }];
    var rest = n - 1;
    var sx = r.x + mw + gap, sw = r.width - mw - gap;
    var h = Math.floor((r.height - gap * (rest - 1)) / rest);
    for (var i = 0; i < rest; i++) {
        var y = r.y + i * (h + gap);
        out.push({ x: sx, y: y, width: sw, height: i === rest - 1 ? r.y + r.height - y : h });
    }
    return out;
}

function retile() {
    if (!enabled || busy) return;
    busy = true;
    try {
        var screens = workspace.screens;
        for (var s = 0; s < screens.length; s++) {
            var out = screens[s];
            var wins = order.filter(function (w) { return tileable(w) && w.output === out; });
            if (!wins.length) continue;
            var area = workspace.clientArea(KWin.PlacementArea, out, workspace.currentDesktop);
            var inner = { x: area.x + gap, y: area.y + gap, width: area.width - 2 * gap, height: area.height - 2 * gap };
            var rects = (layout === "master" ? master : dwindle)(inner, wins.length);
            for (var i = 0; i < wins.length; i++) {
                var w = wins[i], r = rects[i];
                if (w.maximizable) w.setMaximize(false, false);
                w.frameGeometry = { x: r.x, y: r.y, width: Math.max(r.width, 50), height: Math.max(r.height, 50) };
            }
        }
    } finally {
        busy = false;
    }
}

function remove(w) {
    var i = order.indexOf(w);
    if (i >= 0) order.splice(i, 1);
}

function swapWith(w, other) {
    var a = order.indexOf(w), b = order.indexOf(other);
    if (a < 0 || b < 0 || a === b) return;
    order[a] = other;
    order[b] = w;
    retile();
}

function contains(r, x, y) { return x >= r.x && x <= r.x + r.width && y >= r.y && y <= r.y + r.height; }

function add(w) {
    if (!w || !w.normalWindow || order.indexOf(w) >= 0) return;
    order.push(w);
    w.minimizedChanged.connect(retile);
    w.fullScreenChanged.connect(retile);
    w.outputChanged.connect(retile);
    w.desktopsChanged.connect(retile);
    w.interactiveMoveResizeFinished.connect(function () {
        if (!tileable(w)) return;
        // dropped onto another tiled window? swap them; otherwise snap back into place
        var g = w.frameGeometry, cx = g.x + g.width / 2, cy = g.y + g.height / 2;
        for (var i = 0; i < order.length; i++) {
            var o = order[i];
            if (o !== w && tileable(o) && o.output === w.output && contains(o.frameGeometry, cx, cy)) {
                swapWith(w, o);
                return;
            }
        }
        retile();
    });
    retile();
}

workspace.windowList().forEach(add);
workspace.windowAdded.connect(add);
workspace.windowRemoved.connect(function (w) { remove(w); delete floating[key(w)]; retile(); });
workspace.currentDesktopChanged.connect(retile);
if (workspace.screensChanged) workspace.screensChanged.connect(retile);

registerShortcut("DeviumTilingFloat", "Devium Tiling: float / tile the window", "Meta+Shift+Space", function () {
    var w = workspace.activeWindow;
    if (!w) return;
    if (floating[key(w)]) delete floating[key(w)];
    else floating[key(w)] = true;
    retile();
});
registerShortcut("DeviumTilingToggle", "Devium Tiling: on / off", "Meta+Shift+T", function () {
    enabled = !enabled;
    retile();
});
function neighbour(step) {
    var w = workspace.activeWindow;
    var list = order.filter(function (o) { return tileable(o) && w && o.output === w.output; });
    var i = list.indexOf(w);
    if (i < 0 || list.length < 2) return;
    swapWith(w, list[(i + step + list.length) % list.length]);
}
registerShortcut("DeviumTilingSwapPrev", "Devium Tiling: swap with the previous window", "Meta+Alt+Left", function () { neighbour(-1); });
registerShortcut("DeviumTilingSwapNext", "Devium Tiling: swap with the next window", "Meta+Alt+Right", function () { neighbour(1); });
registerShortcut("DeviumTilingMain", "Devium Tiling: make this the main window", "Meta+Alt+Return", function () {
    var w = workspace.activeWindow;
    var i = order.indexOf(w);
    if (i > 0) { order.splice(i, 1); order.unshift(w); retile(); }
});
