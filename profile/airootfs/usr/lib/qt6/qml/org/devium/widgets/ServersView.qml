// Dev servers card: what's listening on which port, open it or stop it.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var servers: []
    signal open(int port)
    signal stop(int pid)
    implicitWidth: 320; implicitHeight: 230
    ColumnLayout {
        anchors.fill: parent; spacing: 6
        Header { Layout.fillWidth: true; icon: "🚀"; title: "Dev servers"; note: v.servers.length ? v.servers.length + " running" : "" }
        Repeater {
            model: v.servers.slice(0, 5)
            RowLayout {
                Layout.fillWidth: true; spacing: 8
                Rectangle { width: 8; height: 8; radius: 4; color: Theme.good }
                Text { text: ":" + modelData.port; color: Theme.ink; font.family: Theme.font; font.pixelSize: 14; font.weight: Font.DemiBold
                       Layout.preferredWidth: 58 }
                Text { text: modelData.name; color: Theme.soft; font.family: Theme.font; font.pixelSize: 12; Layout.fillWidth: true; elide: Text.ElideRight }
                Pill { text: "Open"; height: 24; onClicked: v.open(modelData.port) }
                Pill { text: "Stop"; height: 24; onClicked: v.stop(modelData.pid) }
            }
        }
        Text { visible: !v.servers.length; Layout.fillWidth: true; wrapMode: Text.WordWrap
               text: "Nothing running. Start a dev server (npm run dev, flask run…) and it shows up here."
               color: Theme.soft; font.family: Theme.font; font.pixelSize: 13 }
        Item { Layout.fillHeight: true }
    }
}
