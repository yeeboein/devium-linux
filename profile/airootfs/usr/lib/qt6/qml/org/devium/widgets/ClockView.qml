// Big Devium clock with the date and a greeting.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property string name: ""
    property bool twelveHour: false
    property date now: new Date()
    glow: true
    implicitWidth: 340; implicitHeight: 170
    Timer { interval: 1000; running: true; repeat: true; onTriggered: v.now = new Date() }
    ColumnLayout {
        anchors.fill: parent; spacing: 0
        Text {
            text: {
                var h = v.now.getHours()
                var g = h < 5 ? "Good night" : h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening"
                return g + (v.name ? ", " + v.name : "")
            }
            color: Theme.soft; font.family: Theme.font; font.pixelSize: 14
        }
        RowLayout {
            spacing: 6
            Text {
                text: Qt.formatTime(v.now, v.twelveHour ? "h:mm" : "HH:mm")
                font.family: Theme.font; font.pixelSize: 64; font.weight: Font.Bold
                color: Theme.ink
            }
            Text {
                Layout.alignment: Qt.AlignBottom; bottomPadding: 14
                text: v.twelveHour ? Qt.formatTime(v.now, "AP") : Qt.formatTime(v.now, ":ss")
                color: Theme.accent; font.family: Theme.font; font.pixelSize: 20; font.weight: Font.DemiBold
            }
        }
        Text { text: Qt.formatDate(v.now, "dddd d MMMM"); color: Theme.soft; font.family: Theme.font; font.pixelSize: 15 }
        Item { Layout.fillHeight: true }
    }
}
