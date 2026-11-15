import QtQuick
LinksView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 310; height: 190
    onLaunch: (cmd) => { if (w.runner) w.runner.run("launch " + cmd) }
}
