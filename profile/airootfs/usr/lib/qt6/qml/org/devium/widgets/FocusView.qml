// Focus timer (Pomodoro): 25 minutes of work, then a 5 minute break.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property int workMinutes: 25
    property int breakMinutes: 5
    property int doneToday: 0
    property bool onBreak: false
    property bool running: false
    property int remaining: workMinutes * 60
    signal finished(bool wasBreak)
    implicitWidth: 260; implicitHeight: 250
    Timer {
        interval: 1000; repeat: true; running: v.running
        onTriggered: {
            if (v.remaining > 0) { v.remaining--; return }
            v.running = false
            v.finished(v.onBreak)
            v.onBreak = !v.onBreak
            v.remaining = (v.onBreak ? v.breakMinutes : v.workMinutes) * 60
        }
    }
    function fmt(s) { var m = Math.floor(s / 60), r = s % 60; return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r }
    ColumnLayout {
        anchors.fill: parent; spacing: 8
        Header { Layout.fillWidth: true; icon: v.onBreak ? "☕" : "🎯"; title: v.onBreak ? "Break" : "Focus"
                 note: v.doneToday ? v.doneToday + " done today" : "" }
        Ring {
            Layout.alignment: Qt.AlignHCenter
            width: 120; height: 124; thickness: 8
            value: 1 - v.remaining / ((v.onBreak ? v.breakMinutes : v.workMinutes) * 60)
            text: v.fmt(v.remaining); label: ""
            colour: v.onBreak ? Theme.good : Theme.accent
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter; spacing: 8
            Pill { text: v.running ? "Pause" : (v.remaining < (v.onBreak ? v.breakMinutes : v.workMinutes) * 60 ? "Resume" : "Start"); primary: true
                   onClicked: v.running = !v.running }
            Pill { text: "Reset"; onClicked: { v.running = false; v.onBreak = false; v.remaining = v.workMinutes * 60 } }
        }
    }
}
