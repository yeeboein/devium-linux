// Now playing card: the cover, title, artist, a progress bar, the lyric line being sung, and the controls.
// `info` comes from `widget-data nowplaying`; the card emits control("playpause" | "next" | "previous").
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var info: ({})
    signal control(string action)
    readonly property bool active: !!info.title
    readonly property bool playing: info.status === "Playing"
    property real posAt: 0              // the position when `info` last arrived (seconds)
    property double stamp: Date.now()
    property real now: 0                // the position now: moved on smoothly between updates
    readonly property real length: info.length || 0
    readonly property var lines: info.lyrics || []
    readonly property int cur: {
        var c = -1
        for (var i = 0; i < lines.length; i++) if (lines[i].t <= now + 0.25) c = i
        return c
    }
    readonly property string lyric: cur >= 0 ? (lines[cur].w || "♪") : ""
    implicitWidth: 340; implicitHeight: 208

    onInfoChanged: { posAt = info.position || 0; stamp = Date.now(); now = posAt }
    Timer {
        interval: 250; repeat: true; running: v.active && v.playing
        onTriggered: v.now = v.posAt + (Date.now() - v.stamp) / 1000
    }

    // a play/pause/next/previous button drawn with a canvas, so it needs no icon font
    component Btn: Item {
        property string kind: "play"
        signal clicked()
        width: 38; height: 34
        Rectangle { anchors.fill: parent; radius: 12; color: area.containsMouse ? Theme.well : "transparent" }
        Canvas {
            anchors.centerIn: parent; width: 18; height: 18
            property string k: parent.kind
            onKChanged: requestPaint()
            onPaint: {
                var c = getContext("2d"); c.reset(); c.fillStyle = Theme.ink
                if (k === "play") { c.beginPath(); c.moveTo(4, 2); c.lineTo(16, 9); c.lineTo(4, 16); c.closePath(); c.fill() }
                else if (k === "pause") { c.fillRect(3, 2, 4, 14); c.fillRect(11, 2, 4, 14) }
                else if (k === "next") { c.beginPath(); c.moveTo(2, 2); c.lineTo(12, 9); c.lineTo(2, 16); c.closePath(); c.fill(); c.fillRect(13, 2, 3, 14) }
                else { c.beginPath(); c.moveTo(16, 2); c.lineTo(6, 9); c.lineTo(16, 16); c.closePath(); c.fill(); c.fillRect(2, 2, 3, 14) }
            }
        }
        MouseArea { id: area; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: parent.clicked() }
    }

    ColumnLayout {
        anchors.fill: parent; spacing: 10
        Header { Layout.fillWidth: true; icon: "♪"; title: "Now playing"; note: v.active ? (v.info.player || "") : "" }

        // nothing playing
        ColumnLayout {
            visible: !v.active; Layout.fillWidth: true; Layout.fillHeight: true; spacing: 4
            Item { Layout.fillHeight: true }
            Text { Layout.alignment: Qt.AlignHCenter; text: "Nothing is playing"; color: Theme.soft
                   font.family: Theme.font; font.pixelSize: 15; font.weight: Font.DemiBold }
            Text { Layout.alignment: Qt.AlignHCenter; text: "Start a song in Spotify or your browser"; color: Theme.subtle
                   font.family: Theme.font; font.pixelSize: 12 }
            Item { Layout.fillHeight: true }
        }

        // the song
        RowLayout {
            visible: v.active; Layout.fillWidth: true; spacing: 14
            Item {
                id: coverBox
                Layout.preferredWidth: 92; Layout.preferredHeight: 92
                Rectangle {          // shown until the picture is ready (or when there is none)
                    anchors.fill: parent; radius: 14; visible: !cover.ready
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: Theme.accent }
                        GradientStop { position: 1.0; color: Theme.accent2 }
                    }
                    Text { anchors.centerIn: parent; text: "♪"; color: "#1b2026"; font.pixelSize: 40; font.weight: Font.Bold }
                }
                // the cover with rounded corners, drawn with a 2D canvas (works without 3D acceleration)
                Canvas {
                    id: cover
                    anchors.fill: parent
                    property string src: v.info.art || ""
                    property bool ready: false
                    visible: ready
                    onSrcChanged: { ready = false; if (src) loadImage(src); requestPaint() }
                    Component.onCompleted: if (src) loadImage(src)
                    onImageLoaded: { ready = true; requestPaint() }
                    onPaint: {
                        var ctx = getContext("2d"); ctx.reset()
                        if (!src || !isImageLoaded(src)) { ready = false; return }
                        ready = true
                        var r = 14, w = width, h = height
                        ctx.beginPath(); ctx.moveTo(r, 0); ctx.arcTo(w, 0, w, h, r); ctx.arcTo(w, h, 0, h, r)
                        ctx.arcTo(0, h, 0, 0, r); ctx.arcTo(0, 0, w, 0, r); ctx.closePath(); ctx.clip()
                        ctx.drawImage(src, 0, 0, w, h)
                    }
                }
            }
            ColumnLayout {
                Layout.fillWidth: true; Layout.fillHeight: true; spacing: 2
                Text { Layout.fillWidth: true; text: v.info.title || ""; color: Theme.ink; elide: Text.ElideRight
                       font.family: Theme.font; font.pixelSize: 16; font.weight: Font.DemiBold }
                Text { Layout.fillWidth: true; text: v.info.artist || ""; color: Theme.soft; elide: Text.ElideRight
                       font.family: Theme.font; font.pixelSize: 13 }
                Text { Layout.fillWidth: true; text: v.info.album || ""; color: Theme.subtle; elide: Text.ElideRight
                       font.family: Theme.font; font.pixelSize: 11 }
                Item { Layout.fillHeight: true }
                RowLayout {
                    Layout.alignment: Qt.AlignLeft; spacing: 2
                    Btn { kind: "previous"; onClicked: v.control("previous") }
                    Btn { kind: v.playing ? "pause" : "play"; onClicked: v.control("playpause") }
                    Btn { kind: "next"; onClicked: v.control("next") }
                }
            }
        }

        // progress and the lyric line
        Rectangle {
            visible: v.active; Layout.fillWidth: true; height: 4; radius: 2; color: Theme.well
            Rectangle {
                height: parent.height; radius: 2
                width: v.length > 0 ? parent.width * Math.max(0, Math.min(1, v.now / v.length)) : 0
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: Theme.accent }
                    GradientStop { position: 1.0; color: Theme.accent2 }
                }
            }
        }
        Text {
            visible: v.active; Layout.fillWidth: true; Layout.preferredHeight: 20
            text: v.lyric; color: Theme.accent; elide: Text.ElideRight
            font.family: Theme.font; font.pixelSize: 13; font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
        }
    }
}
