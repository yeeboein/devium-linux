// A round progress ring with the value in the middle (CPU, memory, disk...).
import QtQuick

Item {
    id: ring
    property real value: 0          // 0..1
    property string label: ""
    property string text: Math.round(value * 100) + "%"
    property color colour: value > 0.9 ? Theme.bad : value > 0.75 ? Theme.warn : Theme.accent
    property real thickness: 7
    width: 84; height: 104
    Canvas {
        id: c
        width: ring.width; height: ring.width
        onPaint: {
            var ctx = getContext("2d"); ctx.reset()
            var r = width / 2 - ring.thickness / 2, cx = width / 2, cy = height / 2
            ctx.lineWidth = ring.thickness; ctx.lineCap = "round"
            ctx.strokeStyle = Theme.well; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI); ctx.stroke()
            var g = ctx.createLinearGradient(0, 0, width, height)
            g.addColorStop(0, ring.colour); g.addColorStop(1, ring.colour === Theme.accent ? Theme.accent2 : ring.colour)
            ctx.strokeStyle = g; ctx.beginPath()
            ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + 2 * Math.PI * Math.max(0.001, Math.min(1, ring.value)))
            ctx.stroke()
        }
        Connections { target: ring; function onValueChanged() { c.requestPaint() } function onColourChanged() { c.requestPaint() } }
        Connections { target: Theme; function onAccentChanged() { c.requestPaint() } }
    }
    Text {
        anchors.centerIn: c
        text: ring.text; color: Theme.ink; font.family: Theme.font; font.pixelSize: ring.width * 0.21; font.weight: Font.Bold
    }
    Text {
        anchors { top: c.bottom; topMargin: 4; horizontalCenter: c.horizontalCenter }
        text: ring.label; color: Theme.soft; font.family: Theme.font; font.pixelSize: 12
    }
}
