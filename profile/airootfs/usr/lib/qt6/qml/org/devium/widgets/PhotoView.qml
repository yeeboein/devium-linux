// Photo card: one picture, or a slideshow from a folder, with rounded corners and a soft cross-fade.
// Rounded corners are drawn with a 2D canvas, so it works even without 3D acceleration.
import QtQuick
import Qt.labs.folderlistmodel
import QtCore

Item {
    id: v
    property string folder: ""            // a folder of pictures, or...
    property string image: ""             // ...one picture (wins if set)
    property int interval: 15             // seconds per picture
    property bool shuffle: true
    property bool crop: true              // fill the card (crop) or show the whole picture (fit)
    property bool caption: false          // show the file name
    property int index: 0
    readonly property int count: v.image ? 1 : files.count
    readonly property string current: v.image ? toUrl(v.image)
                                      : (files.count ? String(files.get(Math.min(index, files.count - 1), "fileUrl")) : "")
    implicitWidth: 330; implicitHeight: 250

    function toUrl(p) { return !p ? "" : (p.indexOf("://") > 0 ? p : "file://" + p) }

    FolderListModel {
        id: files
        folder: v.image ? "" : (v.folder ? v.toUrl(v.folder) : StandardPaths.writableLocation(StandardPaths.PicturesLocation))
        nameFilters: ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.gif", "*.bmp", "*.JPG", "*.JPEG", "*.PNG", "*.WEBP"]
        showDirs: false
        sortField: FolderListModel.Name
        onCountChanged: if (v.index >= count) v.index = 0
    }
    Timer {
        interval: Math.max(3, v.interval) * 1000
        running: v.count > 1
        repeat: true
        onTriggered: v.index = v.shuffle ? (v.index + 1 + Math.floor(Math.random() * Math.max(1, v.count - 1))) % v.count
                                         : (v.index + 1) % v.count
    }

    // two canvases: the new picture fades in over the old one
    property int front: 0
    function show() {
        if (!a || !b || !current) return
        var c = front === 0 ? b : a
        if (c.src === current && c.isImageLoaded(current)) { front = (c === a ? 0 : 1); c.requestPaint(); return }
        c.src = current
        c.loadImage(current)
        if (c.isImageLoaded(current)) {      // pictures on disk can load at once, without the "loaded" signal
            c.requestPaint()
            front = (c === a ? 0 : 1)
        }
    }
    onCurrentChanged: show()
    onCropChanged: { if (a) a.requestPaint(); if (b) b.requestPaint() }
    Component.onCompleted: Qt.callLater(show)
    Repeater {
        model: 2
        Canvas {
            id: cv
            property string src: ""
            anchors.fill: parent
            opacity: (index === 0 && v.front === 0) || (index === 1 && v.front === 1) ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: 900; easing.type: Easing.InOutQuad } }
            Component.onCompleted: { if (index === 0) a = cv; else b = cv }
            onImageLoaded: { requestPaint(); v.front = index }
            onWidthChanged: requestPaint()
            onHeightChanged: requestPaint()
            onPaint: {
                var ctx = getContext("2d")
                ctx.reset()
                var r = Theme.radius
                ctx.beginPath()
                ctx.moveTo(r, 0); ctx.lineTo(width - r, 0); ctx.quadraticCurveTo(width, 0, width, r)
                ctx.lineTo(width, height - r); ctx.quadraticCurveTo(width, height, width - r, height)
                ctx.lineTo(r, height); ctx.quadraticCurveTo(0, height, 0, height - r)
                ctx.lineTo(0, r); ctx.quadraticCurveTo(0, 0, r, 0)
                ctx.closePath()
                ctx.fillStyle = Theme.card
                ctx.fill()
                if (!src || !isImageLoaded(src)) return
                ctx.save()
                ctx.clip()
                var img = probe.status === Image.Ready && probe.source == src ? probe : null
                var iw = img ? img.implicitWidth : width, ih = img ? img.implicitHeight : height
                var s = v.crop ? Math.max(width / iw, height / ih) : Math.min(width / iw, height / ih)
                var dw = iw * s, dh = ih * s
                ctx.drawImage(src, (width - dw) / 2, (height - dh) / 2, dw, dh)
                ctx.restore()
            }
        }
    }
    property Canvas a: null
    property Canvas b: null
    // knows each picture's real size (for crop / fit)
    Image {
        id: probe
        visible: false
        source: v.current
        onStatusChanged: if (status === Image.Ready) { if (v.a) v.a.requestPaint(); if (v.b) v.b.requestPaint() }
    }

    // thin border, the same as the other Devium cards
    Rectangle {
        anchors.fill: parent; radius: Theme.radius
        color: "transparent"; border.color: Theme.cardBorder; border.width: 1
    }
    // caption
    Rectangle {
        visible: v.caption && v.current !== ""
        anchors { left: parent.left; right: parent.right; bottom: parent.bottom; margins: 10 }
        height: 30; radius: 12; color: "#99242a32"
        Text {
            anchors { fill: parent; leftMargin: 12; rightMargin: 12 }
            verticalAlignment: Text.AlignVCenter
            text: decodeURIComponent(v.current.split("/").pop()).replace(/\.[^.]+$/, "")
            color: Theme.ink; font.family: Theme.font; font.pixelSize: 13; elide: Text.ElideRight
        }
    }
    // nothing to show
    Column {
        visible: v.current === ""
        anchors.centerIn: parent
        spacing: 6
        Text { anchors.horizontalCenter: parent.horizontalCenter; text: "🖼️"; font.pixelSize: 40 }
        Text {
            width: v.width - 40; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap
            text: "No pictures found. Put some in your Pictures folder, or pick a folder in the widget's settings."
            color: Theme.soft; font.family: Theme.font; font.pixelSize: 13
        }
    }
    MouseArea {
        anchors.fill: parent; z: -1
        acceptedButtons: Qt.LeftButton
        onDoubleClicked: if (v.current) Qt.openUrlExternally(v.current)
    }
}
