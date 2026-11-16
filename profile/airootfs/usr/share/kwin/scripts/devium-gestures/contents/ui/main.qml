// Devium Gestures: three-finger touchpad gestures like GNOME (KDE's own four-finger gestures keep working).
//   swipe up      the overview (all windows and workspaces)
//   swipe down    show the desktop (again to bring the windows back)
//   swipe left    the next workspace; past the last one a new empty workspace appears, like GNOME
//   swipe right   the previous workspace
import QtQuick
import org.kde.kwin

Item {
    id: root

    DBusCall {
        id: shortcut
        service: "org.kde.kglobalaccel"
        path: "/component/kwin"
        dbusInterface: "org.kde.kglobalaccel.Component"
        method: "invokeShortcut"
    }

    function invoke(name) {
        shortcut.arguments = [name];
        shortcut.call();
    }

    function indexOfDesktop(list, desktop) {
        for (let i = 0; i < list.length; i++)
            if (list[i] === desktop) return i;
        return -1;
    }

    function inUse(desktop) {
        const wins = Workspace.windowList();
        for (let i = 0; i < wins.length; i++) {
            const w = wins[i];
            if (!w.normalWindow || w.skipTaskbar) continue;
            if (w.onAllDesktops) continue;
            if (indexOfDesktop(w.desktops, desktop) >= 0) return true;
        }
        return false;
    }

    function step(delta) {
        const list = Workspace.desktops;
        const i = indexOfDesktop(list, Workspace.currentDesktop);
        if (i < 0) return;
        let j = i + delta;
        if (j < 0) return;
        if (j >= list.length) {
            // only add a workspace when this one has windows on it (no pile of empty ones), and at most 9
            if (!inUse(list[i]) || list.length >= 9) return;
            Workspace.createDesktop(list.length, "");
            j = Workspace.desktops.length - 1;
        }
        Workspace.currentDesktop = Workspace.desktops[j];
    }

    SwipeGestureHandler {
        direction: SwipeGestureHandler.Direction.Up
        fingerCount: 3
        deviceType: SwipeGestureHandler.Device.Touchpad
        onActivated: root.invoke("Overview")
    }
    SwipeGestureHandler {
        direction: SwipeGestureHandler.Direction.Down
        fingerCount: 3
        deviceType: SwipeGestureHandler.Device.Touchpad
        onActivated: root.invoke("Show Desktop")
    }
    SwipeGestureHandler {
        direction: SwipeGestureHandler.Direction.Left
        fingerCount: 3
        deviceType: SwipeGestureHandler.Device.Touchpad
        onActivated: root.step(1)
    }
    SwipeGestureHandler {
        direction: SwipeGestureHandler.Direction.Right
        fingerCount: 3
        deviceType: SwipeGestureHandler.Device.Touchpad
        onActivated: root.step(-1)
    }
}
