// Now playing widget (used on Xfce and Hyprland; Plasma has its own glue).
import QtQuick
NowPlayingView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 340; height: 208
    Connections {
        target: w.runner
        function onDone(args, out) { if (args === "nowplaying") { try { w.info = JSON.parse(out) } catch (e) {} } }
    }
    onControl: (action) => { if (w.runner) { w.runner.run("media " + action); refresh.restart() } }
    Timer { id: refresh; interval: 500; onTriggered: if (w.runner) w.runner.run("nowplaying") }
    // quick while a song is on, slow when nothing is playing (light on old laptops)
    Timer { interval: w.active ? 2000 : 6000; running: !!w.runner; repeat: true; triggeredOnStart: true
            onTriggered: w.runner.run("nowplaying") }
}
