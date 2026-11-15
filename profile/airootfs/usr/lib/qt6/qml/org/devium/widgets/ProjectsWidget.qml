import QtQuick
ProjectsView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 350; height: 290
    Connections { target: w.runner; function onDone(args, out) { if (args === "projects") { try { w.repos = JSON.parse(out) } catch (e) {} } } }
    Timer { interval: 20000; running: !!w.runner; repeat: true; triggeredOnStart: true; onTriggered: w.runner.run("projects") }
    onOpen: (path) => w.runner.run("open " + path)
    onTerminal: (path) => w.runner.run("term " + path)
}
