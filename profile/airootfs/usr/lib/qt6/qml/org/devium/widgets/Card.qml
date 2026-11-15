// A frosted Devium card with a soft accent glow along the top.
import QtQuick

Rectangle {
    id: card
    default property alias content: inner.data
    property bool glow: true
    radius: Theme.radius
    color: Theme.card
    border.color: Theme.cardBorder
    border.width: 1
    clip: true
    Rectangle {   // accent line at the top
        visible: card.glow
        anchors { left: parent.left; right: parent.right; top: parent.top; leftMargin: card.radius; rightMargin: card.radius }
        height: 2; radius: 1
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "transparent" }
            GradientStop { position: 0.3; color: Theme.accent }
            GradientStop { position: 0.7; color: Theme.accent2 }
            GradientStop { position: 1.0; color: "transparent" }
        }
    }
    Item {
        id: inner
        anchors.fill: parent
        anchors.margins: Theme.pad
    }
}
