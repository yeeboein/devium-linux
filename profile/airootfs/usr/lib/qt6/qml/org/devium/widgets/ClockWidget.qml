import QtQuick
ClockView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 330; height: 165
    Connections { target: w.runner; function onDone(args, out) { if (args === "name") { try { w.name = JSON.parse(out) } catch (e) {} } } }
    Component.onCompleted: if (runner) runner.run("name")
}
