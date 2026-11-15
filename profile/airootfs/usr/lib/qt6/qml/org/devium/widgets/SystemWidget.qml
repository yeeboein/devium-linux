import QtQuick
SystemView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 330; height: 190
    Connections { target: w.runner; function onDone(args, out) { if (args === "sys") { try { w.info = JSON.parse(out) } catch (e) {} } } }
    Timer { interval: 4000; running: !!w.runner; repeat: true; triggeredOnStart: true; onTriggered: w.runner.run("sys") }
}
