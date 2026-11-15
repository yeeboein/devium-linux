import QtQuick
FocusView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 250; height: 240
    onFinished: (wasBreak) => {
        if (w.runner) w.runner.run("focus " + (wasBreak ? "break" : "work"))
        if (!wasBreak) w.doneToday++
    }
}
