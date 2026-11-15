// Weather card: now, and the next five days.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var info: ({ ok: false, place: "", error: "Loading…" })
    property bool loading: false
    signal refresh()
    implicitWidth: 340; implicitHeight: 250
    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        Header { Layout.fillWidth: true; icon: "🌤️"; title: "Weather"; note: v.info.place || "" }
        RowLayout {
            visible: v.info.ok; spacing: 14
            Text { text: v.info.icon || ""; font.pixelSize: 46 }
            Column {
                Text { text: v.info.temp || ""; color: Theme.ink; font.family: Theme.font; font.pixelSize: 40; font.weight: Font.Bold }
                Text { text: (v.info.text || "") + " · " + (v.info.feels || ""); color: Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
            }
            Item { Layout.fillWidth: true }
            Column {
                spacing: 3
                Text { anchors.right: parent.right; text: "💨 " + (v.info.wind || ""); color: Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
                Text { anchors.right: parent.right; text: "💧 " + (v.info.humidity || ""); color: Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
                Text { anchors.right: parent.right; visible: v.info.uv !== null && v.info.uv !== undefined
                       text: "UV " + v.info.uv; color: v.info.uv >= 6 ? Theme.warn : Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
            }
        }
        Rectangle { visible: v.info.ok; Layout.fillWidth: true; height: 1; color: Theme.cardBorder }
        RowLayout {
            visible: v.info.ok; Layout.fillWidth: true; spacing: 0
            Repeater {
                model: v.info.days || []
                Column {
                    Layout.fillWidth: true; spacing: 2
                    Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.day; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11 }
                    Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.icon; font.pixelSize: 20 }
                    Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.hi; color: Theme.ink; font.family: Theme.font; font.pixelSize: 13; font.weight: Font.DemiBold }
                    Text { anchors.horizontalCenter: parent.horizontalCenter; text: modelData.lo; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 12 }
                }
            }
        }
        Text {
            visible: v.info.ok; text: v.info.sun || ""; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11
        }
        Text {
            visible: !v.info.ok; Layout.fillWidth: true; Layout.fillHeight: true
            text: v.loading ? "Checking the weather…" : (v.info.error || "")
            color: Theme.soft; font.family: Theme.font; font.pixelSize: 13; wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter
        }
        Item { Layout.fillHeight: true; visible: v.info.ok }
    }
}
