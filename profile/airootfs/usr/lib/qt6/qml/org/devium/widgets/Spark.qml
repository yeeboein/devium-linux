// A smooth little line chart (the tide curve) with a "now" marker.
import QtQuick

Canvas {
    id: s
    property var values: []
    property real nowAt: 0
    height: 46
    onValuesChanged: requestPaint()
    onWidthChanged: requestPaint()
    onPaint: {
        var ctx = getContext("2d"); ctx.reset()
        var v = values || []; if (v.length < 2) return
        var lo = Math.min.apply(null, v), hi = Math.max.apply(null, v), span = Math.max(0.05, hi - lo)
        function X(i) { return i * width / (v.length - 1) }
        function Y(x) { return height - 4 - (x - lo) / span * (height - 10) }
        var g = ctx.createLinearGradient(0, 0, 0, height)
        g.addColorStop(0, Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.45))
        g.addColorStop(1, Qt.rgba(Theme.accent.r, Theme.accent.g, Theme.accent.b, 0.0))
        ctx.beginPath(); ctx.moveTo(0, height)
        for (var i = 0; i < v.length; i++) ctx.lineTo(X(i), Y(v[i]))
        ctx.lineTo(width, height); ctx.closePath(); ctx.fillStyle = g; ctx.fill()
        ctx.beginPath(); ctx.lineWidth = 2; ctx.strokeStyle = Theme.accent
        for (var k = 0; k < v.length; k++) k ? ctx.lineTo(X(k), Y(v[k])) : ctx.moveTo(X(k), Y(v[k]))
        ctx.stroke()
        var nx = nowAt * width, ni = Math.round(nowAt * (v.length - 1))
        ctx.fillStyle = Theme.ink; ctx.beginPath(); ctx.arc(nx, Y(v[ni]), 4, 0, 2 * Math.PI); ctx.fill()
    }
}
