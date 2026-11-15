// A small "label / value" block.
import QtQuick

Column {
    property string label: ""
    property string value: "–"
    property string sub: ""
    property color valueColour: Theme.ink
    spacing: 1
    Text { text: parent.label; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11 }
    Text { text: parent.value; color: parent.valueColour; font.family: Theme.font; font.pixelSize: 17; font.weight: Font.DemiBold }
    Text { text: parent.sub; color: Theme.soft; font.family: Theme.font; font.pixelSize: 11; visible: text.length }
}
