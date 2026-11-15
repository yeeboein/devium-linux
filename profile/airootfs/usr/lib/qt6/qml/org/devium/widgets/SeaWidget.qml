// Sea widget with its own data (used on Xfce and Hyprland; Plasma has its own glue).
import QtQuick
import "Sea.js" as SeaData
SeaView {
    id: w
    property string place: ""
    property bool imperial: false
    property var runner: null
    width: 330; height: 290
    function reload() { loading = true; SeaData.load(place, imperial, function (m) { w.info = m; w.loading = false }) }
    onRefresh: reload()
    onPlaceChanged: reload()
    Timer { interval: 30 * 60 * 1000; running: true; repeat: true; triggeredOnStart: true; onTriggered: w.reload() }
}
