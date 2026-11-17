// Devium Remember Windows: each app opens where you left it.
// When an app's window is closed (or you finish moving / resizing it), its size and position are saved in
// ~/.config/devium/window-places.conf. The next time that app opens a window, it's put back there, kept on screen
// and a little below the top edge so the top border can always be grabbed. Maximised windows open maximised.
// Not used for dialogs, popups, or when another window of the same app is already open (that one keeps KDE's
// normal placement, so windows don't pile up on top of each other).
import QtQuick
import QtCore
import org.kde.kwin

Item {
    id: root

    Settings {
        id: store
        location: StandardPaths.writableLocation(StandardPaths.GenericConfigLocation) + "/devium/window-places.conf"
        property string places: "{}"
    }

    readonly property var skip: ["plasmashell", "krunner", "org.kde.krunner", "kwin", "ksmserver", "kded6",
                                 "polkit-kde-authentication-agent-1", "org.kde.polkit-kde-authentication-agent-1",
                                 "devium-spotlight", "spectacle", "org.kde.spectacle", "xwaylandvideobridge"]

    function key(w) {
        return String(w.resourceClass || w.resourceName || "")
    }

    function wanted(w) {
        if (!w || !w.normalWindow || w.transient || w.skipTaskbar || w.specialWindow) return false
        if (w.fullScreen) return false
        const k = key(w)
        return k.length > 0 && root.skip.indexOf(k) < 0
    }

    function load() {
        try { return JSON.parse(store.places) } catch (e) { return {} }
    }

    function isMaximized(w) {
        const a = Workspace.clientArea(KWin.MaximizeArea, w)
        const g = w.frameGeometry
        return Math.abs(g.x - a.x) <= 2 && Math.abs(g.y - a.y) <= 2 &&
               Math.abs(g.width - a.width) <= 2 && Math.abs(g.height - a.height) <= 2
    }

    function save(w) {
        if (!wanted(w)) return
        const g = w.frameGeometry
        if (g.width < 120 || g.height < 80) return
        const all = load()
        const prev = all[key(w)]
        const max = isMaximized(w)
        // maximised: keep the size from before, just remember it was maximised
        all[key(w)] = max && prev ? { x: prev.x, y: prev.y, w: prev.w, h: prev.h, max: true }
                                  : { x: Math.round(g.x), y: Math.round(g.y), w: Math.round(g.width),
                                      h: Math.round(g.height), max: max }
        store.places = JSON.stringify(all)
    }

    function otherOpen(w) {
        const list = Workspace.windowList()
        for (let i = 0; i < list.length; i++) {
            const o = list[i]
            if (o !== w && o.normalWindow && !o.minimized && key(o) === key(w)) return true
        }
        return false
    }

    function restore(w) {
        if (!wanted(w) || otherOpen(w)) return
        const p = load()[key(w)]
        if (!p) return
        const a = Workspace.clientArea(KWin.PlacementArea, w)
        if (p.max && w.maximizable) {
            w.setMaximize(true, true)
            return
        }
        const gap = 8                                   // keep the top edge grabbable
        const width = Math.min(p.w, a.width)
        const height = Math.min(p.h, a.height - gap)
        let x = Math.max(a.x, Math.min(p.x, a.x + a.width - width))
        let y = Math.max(a.y + gap, Math.min(p.y, a.y + a.height - height))
        w.frameGeometry = Qt.rect(x, y, width, height)
    }

    function watch(w) {
        if (!wanted(w)) return
        w.interactiveMoveResizeFinished.connect(function () { root.save(w) })
    }

    Connections {
        target: Workspace
        function onWindowAdded(w) {
            root.restore(w)
            root.watch(w)
        }
        function onWindowRemoved(w) {
            root.save(w)
        }
    }

    Component.onCompleted: {
        const list = Workspace.windowList()
        for (let i = 0; i < list.length; i++) watch(list[i])
    }
}
