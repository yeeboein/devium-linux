// Git projects card: every repo in ~/Projects with its branch and what's waiting.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var repos: []
    signal open(string path)
    signal terminal(string path)
    implicitWidth: 360; implicitHeight: 300
    ColumnLayout {
        anchors.fill: parent; spacing: 6
        Header { Layout.fillWidth: true; icon: "📁"; title: "Projects"; note: v.repos.length === 1 ? "1 repo" : v.repos.length ? v.repos.length + " repos" : "" }
        Repeater {
            model: v.repos.slice(0, 7)
            Rectangle {
                Layout.fillWidth: true; height: 36; radius: 12
                color: area.containsMouse ? "#22ffffff" : "transparent"
                RowLayout {
                    anchors { fill: parent; leftMargin: 8; rightMargin: 8 }
                    spacing: 8
                    Rectangle { width: 8; height: 8; radius: 4
                                color: modelData.dirty ? Theme.warn : (modelData.ahead ? Theme.accent : Theme.good) }
                    Column {
                        Layout.fillWidth: true
                        Text { text: modelData.name; color: Theme.ink; font.family: Theme.font; font.pixelSize: 13; font.weight: Font.DemiBold
                               elide: Text.ElideRight; width: parent.width }
                        Text { text: "⎇ " + modelData.branch + "  ·  " + modelData.when; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11 }
                    }
                    Text {
                        text: (modelData.dirty ? "✎" + modelData.dirty + " " : "") + (modelData.ahead ? "↑" + modelData.ahead + " " : "") +
                              (modelData.behind ? "↓" + modelData.behind : "") || "✓"
                        color: modelData.dirty || modelData.ahead || modelData.behind ? Theme.warn : Theme.good
                        font.family: Theme.font; font.pixelSize: 12
                    }
                }
                MouseArea { id: area; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                            acceptedButtons: Qt.LeftButton | Qt.RightButton
                            onClicked: (m) => m.button === Qt.RightButton ? v.terminal(modelData.path) : v.open(modelData.path) }
            }
        }
        Text { visible: !v.repos.length; Layout.fillWidth: true; wrapMode: Text.WordWrap
               text: "No Git projects in ~/Projects yet. Start one: devium-new-project my-app"
               color: Theme.soft; font.family: Theme.font; font.pixelSize: 13 }
        Item { Layout.fillHeight: true }
        Text { text: "Click: open in your editor · Right-click: terminal"; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 10 }
    }
}
