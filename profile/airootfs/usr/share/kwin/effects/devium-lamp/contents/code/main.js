"use strict";
// Devium magic lamp close: a closed window narrows and pours down into its dock icon, like a genie.
// Minimising uses KWin's own Magic Lamp effect; this does the same look for closing, plus a soft
// open animation (the Scale and Fade effects are turned off while this is on, so they don't fight it).

function closeTime() { return animationTime(400); }
function openTime() { return animationTime(200); }

function wanted(w) {
    if (effects.hasActiveFullScreenEffect) return false;
    if (!w || !w.visible) return false;
    return w.normalWindow || w.dialog;
}

function geometryOf(w) {
    return w.frameGeometry || w.geometry;
}

// where the window pours to: its dock/taskbar icon when the dock says where it is, else the bottom middle
function target(w) {
    var icon = w.iconGeometry;
    if (icon && icon.width > 0 && icon.height > 0)
        return { x: icon.x + icon.width / 2, y: icon.y + icon.height / 2 };
    var area = null;
    try { area = w.screen.geometry; } catch (e) { area = null; }
    if (!area) area = effects.virtualScreenGeometry;
    return { x: area.x + area.width / 2, y: area.y + area.height };
}

effects.windowClosed.connect(function (w) {
    if (!wanted(w) || w.skipsCloseAnimation) return;
    if (!effect.grab(w, Effect.WindowClosedGrabRole)) return;
    if (w.deviumLampIn) { cancel(w.deviumLampIn); delete w.deviumLampIn; }
    var g = geometryOf(w), t = target(w);
    var dx = t.x - (g.x + g.width / 2), dy = t.y - (g.y + g.height / 2);
    animate({
        window: w,
        duration: closeTime(),
        animations: [
            // narrows quickly, like the neck of the lamp...
            { type: Effect.Scale, curve: QEasingCurve.OutCubic, from: { value1: 1, value2: 1 }, to: { value1: 0.1, value2: 1 } },
            // ...then gets shorter as it pours in
            { type: Effect.Scale, curve: QEasingCurve.InCubic, from: { value1: 1, value2: 1 }, to: { value1: 1, value2: 0.04 } },
            // slides sideways over the icon early, and drops into it late
            { type: Effect.Translation, curve: QEasingCurve.OutCubic, from: { value1: 0, value2: 0 }, to: { value1: dx, value2: 0 } },
            { type: Effect.Translation, curve: QEasingCurve.InQuad, from: { value1: 0, value2: 0 }, to: { value1: 0, value2: dy } },
            { type: Effect.Opacity, curve: QEasingCurve.InQuart, from: 1, to: 0 }
        ]
    });
});

effects.windowAdded.connect(function (w) {
    if (!wanted(w)) return;
    if (!effect.grab(w, Effect.WindowAddedGrabRole)) return;
    w.deviumLampIn = animate({
        window: w,
        duration: openTime(),
        curve: QEasingCurve.OutCubic,
        animations: [
            { type: Effect.Scale, from: 0.92, to: 1 },
            { type: Effect.Opacity, from: 0, to: 1 }
        ]
    });
});

effect.animationEnded.connect(function (w, id) {
    if (w.deviumLampIn === id) {
        delete w.deviumLampIn;
        try { effect.ungrab(w, Effect.WindowAddedGrabRole); } catch (e) { }
    }
});
