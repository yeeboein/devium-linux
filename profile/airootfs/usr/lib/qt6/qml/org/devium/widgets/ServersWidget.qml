import QtQuick
ServersView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 310; height: 220
    Connections { target: w.runner; function onDone(args, out) { if (args === "ports") { try { w.servers = JSON.parse(out) } catch (e) {} } } }
    Timer { id: poll; interval: 5000; running: !!w.runner; repeat: true; triggeredOnStart: true; onTriggered: w.runner.run("ports") }
    onOpen: (port) => Qt.openUrlExternally("http://localhost:" + port)
    onStop: (pid) => { w.runner.run("stop " + pid); soon.restart() }
    Timer { id: soon; interval: 800; onTriggered: w.runner.run("ports") }
}
