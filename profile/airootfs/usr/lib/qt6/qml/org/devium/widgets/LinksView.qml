// Devium shortcuts: the Devium apps one click away.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    signal launch(string cmd)
    property var links: [
        { icon: "🔎", name: "Spotlight", cmd: "devium-spotlight" },
        { icon: "🧰", name: "Tools", cmd: "devium-tools" },
        { icon: "🧩", name: "Configure", cmd: "devium-setup-wizard" },
        { icon: "⬆️", name: "Updates", cmd: "devium-tools updates" },
        { icon: "🧹", name: "Clean up", cmd: "devium-tools clean" },
        { icon: "💻", name: "Coding", cmd: "devium-tools coding" },
        { icon: "❤️", name: "Health", cmd: "devium-tools health" },
        { icon: "⌨️", name: "Terminal", cmd: "konsole" }
    ]
    implicitWidth: 320; implicitHeight: 200
    ColumnLayout {
        anchors.fill: parent; spacing: 8
        Header { Layout.fillWidth: true; icon: "✨"; title: "Devium" }
        GridLayout {
            columns: 4; rowSpacing: 6; columnSpacing: 6; Layout.fillWidth: true
            Repeater {
                model: v.links
                Rectangle {
                    Layout.fillWidth: true; height: 58; radius: 14
                    color: a.containsMouse ? "#2effffff" : Theme.well
                    Column {
                        anchors.centerIn: parent; spacing: 2
                        Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.icon; font.pixelSize: 20 }
                        Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.name; color: Theme.soft
                               font.family: Theme.font; font.pixelSize: 10 }
                    }
                    MouseArea { id: a; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: v.launch(modelData.cmd) }
                }
            }
        }
    }
}
