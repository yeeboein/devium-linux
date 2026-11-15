// A rounded button in the Devium style.
import QtQuick

Rectangle {
    id: pill
    property string text: ""
    property bool primary: false
    signal clicked()
    height: 30; width: label.implicitWidth + 26; radius: 15
    color: primary ? "transparent" : (area.containsMouse ? "#33ffffff" : Theme.well)
    gradient: primary ? grad : null
    Gradient {
        id: grad
        orientation: Gradient.Horizontal
        GradientStop { position: 0.0; color: area.containsMouse ? Qt.lighter(Theme.accent, 1.1) : Theme.accent }
        GradientStop { position: 1.0; color: area.containsMouse ? Qt.lighter(Theme.accent2, 1.1) : Theme.accent2 }
    }
    Text {
        id: label; anchors.centerIn: parent; text: pill.text
        color: pill.primary ? "#1b2026" : Theme.ink; font.family: Theme.font; font.pixelSize: 13
        font.weight: pill.primary ? Font.DemiBold : Font.Normal
    }
    MouseArea { id: area; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: pill.clicked() }
}
