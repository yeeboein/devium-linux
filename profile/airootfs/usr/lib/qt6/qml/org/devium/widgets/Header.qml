// Small widget title: an emoji or symbol, the name, and an optional note on the right.
import QtQuick

Item {
    property string icon: ""
    property string title: ""
    property string note: ""
    width: parent ? parent.width : 200
    height: 22
    Row {
        spacing: 7
        anchors.verticalCenter: parent.verticalCenter
        Text { text: parent.parent.icon; font.pixelSize: 15; anchors.verticalCenter: parent.verticalCenter; visible: text.length }
        Text {
            text: parent.parent.title.toUpperCase()
            color: Theme.soft; font.family: Theme.font; font.pixelSize: 11; font.weight: Font.DemiBold
            font.letterSpacing: 1.4
            anchors.verticalCenter: parent.verticalCenter
        }
    }
    Text {
        anchors { right: parent.right; verticalCenter: parent.verticalCenter }
        text: parent.note; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11
        elide: Text.ElideLeft; width: Math.min(implicitWidth, parent.width * 0.55); horizontalAlignment: Text.AlignRight
    }
}
