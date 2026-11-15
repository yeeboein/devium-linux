// The home screen: pages you swipe between, each with apps and Devium widgets.
// Long-press (or Edit) to rearrange: icons wiggle, ✕ removes, + adds apps, widgets and pages.
import QtQuick
import QtQuick.Controls as QQC2
import org.kde.kirigami as Kirigami
import org.devium.widgets

Item {
    id: home
    property var runner: null
    property string pagesJson: ""
    property var pages: []
    property bool editing: false
    property var allApps: []
    signal save(string json)

    readonly property var defaultPages: [
        { items: [ { t: "widget", k: "clock" }, { t: "widget", k: "weather" },
                   { t: "app", id: "org.kde.konsole" }, { t: "app", id: "org.kde.dolphin" },
                   { t: "app", id: "devium-tools" }, { t: "app", id: "devium-setup-wizard" },
                   { t: "app", id: "systemsettings" } ] },
        { items: [ { t: "widget", k: "photo" }, { t: "widget", k: "system" } ] }
    ]
    readonly property var widgetKinds: [
        { k: "clock", name: "Clock" }, { k: "weather", name: "Weather" }, { k: "sea", name: "Sea" },
        { k: "system", name: "System" }, { k: "photo", name: "Photo" }, { k: "focus", name: "Focus timer" },
        { k: "projects", name: "Git projects" }, { k: "servers", name: "Dev servers" }, { k: "links", name: "Devium shortcuts" }
    ]

    function load() {
        var p = null
        try { p = JSON.parse(pagesJson) } catch (e) {}
        pages = (p && p.length) ? p : JSON.parse(JSON.stringify(defaultPages))
    }
    function commit() { pages = pages.slice(); save(JSON.stringify(pages)) }
    function appInfo(id) {
        for (var i = 0; i < allApps.length; i++) if (allApps[i].id === id) return allApps[i]
        return { id: id, name: id.split(".").pop(), icon: id }
    }
    function removeItem(pageIdx, itemIdx) { pages[pageIdx].items.splice(itemIdx, 1); commit() }
    function addToCurrent(item) { pages[swipe.currentIndex].items.push(item); commit() }
    function addPage() { pages.push({ items: [] }); commit(); swipe.currentIndex = pages.length - 1 }
    function removePage(i) { if (pages.length > 1) { pages.splice(i, 1); commit() } }

    onPagesJsonChanged: load()
    Component.onCompleted: { load(); if (runner) runner.run("apps") }
    Connections {
        target: home.runner
        function onDone(args, out) { if (args === "apps") { try { home.allApps = JSON.parse(out) } catch (e) {} } }
    }

    QQC2.SwipeView {
        id: swipe
        anchors { fill: parent; bottomMargin: 50 }
        clip: true
        interactive: true
        Repeater {
            model: home.pages.length
            Item {
                id: pageItem
                readonly property int pageIdx: index
                Flow {
                    anchors { fill: parent; margins: 28 }
                    spacing: 22
                    Repeater {
                        model: (home.pages[pageItem.pageIdx] || { items: [] }).items
                        delegate: Item {
                            id: cell
                            readonly property var it: modelData
                            width: content.width; height: content.height
                            Loader {
                                id: content
                                sourceComponent: cell.it.t === "app" ? appTile : widgetTile
                                property var it: cell.it
                            }
                            // wiggle while editing, like iOS
                            SequentialAnimation on rotation {
                                running: home.editing; loops: Animation.Infinite
                                NumberAnimation { to: -1.6; duration: 110 + (index % 3) * 20 }
                                NumberAnimation { to: 1.6; duration: 110 + (index % 3) * 20 }
                            }
                            onRotationChanged: if (!home.editing && rotation !== 0) rotation = 0
                            Rectangle {   // remove
                                visible: home.editing
                                width: 26; height: 26; radius: 13; color: "#e6242a32"; border.color: Theme.cardBorder
                                anchors { left: parent.left; top: parent.top; margins: -8 }
                                Text { anchors.centerIn: parent; text: "✕"; color: Theme.ink; font.pixelSize: 13 }
                                MouseArea { anchors.fill: parent; onClicked: home.removeItem(pageItem.pageIdx, index) }
                            }
                        }
                    }
                }
                Text {
                    visible: (home.pages[pageItem.pageIdx] || { items: [] }).items.length === 0
                    anchors.centerIn: parent
                    text: home.editing ? "Empty page: press + to add apps and widgets" : "Press and hold to add apps and widgets"
                    color: Theme.soft; font.family: Theme.font; font.pixelSize: 16
                }
                // press and hold on the empty space to edit
                MouseArea {
                    anchors.fill: parent; z: -1
                    pressAndHoldInterval: 600
                    onPressAndHold: home.editing = true
                    onClicked: if (home.editing) home.editing = false
                }
            }
        }
    }

    // swipe with the touchpad or the mouse wheel too
    WheelHandler {
        property real acc: 0
        property double last: 0
        onWheel: (e) => {
            var d = Math.abs(e.angleDelta.x) > Math.abs(e.angleDelta.y) ? -e.angleDelta.x : -e.angleDelta.y
            acc += d
            var now = Date.now()
            if (now - last < 450) return
            if (acc > 100 && swipe.currentIndex < home.pages.length - 1) { swipe.currentIndex++; acc = 0; last = now }
            else if (acc < -100 && swipe.currentIndex > 0) { swipe.currentIndex--; acc = 0; last = now }
        }
    }

    // bottom bar: page dots, and the edit buttons while editing
    Rectangle {
        id: bar
        anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom; bottomMargin: 6 }
        height: 36; radius: 18
        width: barRow.implicitWidth + 28
        color: "#b3242a32"; border.color: Theme.cardBorder
        Row {
            id: barRow
            anchors.centerIn: parent
            spacing: 12
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 9
                Repeater {
                    model: home.pages.length
                    Rectangle {
                        width: index === swipe.currentIndex ? 22 : 8; height: 8; radius: 4
                        color: index === swipe.currentIndex ? Theme.accent : "#80ffffff"
                        Behavior on width { NumberAnimation { duration: 200 } }
                        MouseArea { anchors.fill: parent; anchors.margins: -6; onClicked: swipe.currentIndex = index }
                    }
                }
            }
            Rectangle { visible: true; width: 1; height: 18; color: Theme.cardBorder; anchors.verticalCenter: parent.verticalCenter }
            Pill { height: 26; visible: !home.editing; text: "Edit"; onClicked: home.editing = true }
            Pill { height: 26; visible: home.editing; text: "+ App"; onClicked: { appSheet.open(); search.text = "" } }
            Pill { height: 26; visible: home.editing; text: "+ Widget"; onClicked: widgetSheet.open() }
            Pill { height: 26; visible: home.editing; text: "+ Page"; onClicked: home.addPage() }
            Pill { height: 26; visible: home.editing && home.pages.length > 1; text: "Remove page"; onClicked: home.removePage(swipe.currentIndex) }
            Pill { height: 26; visible: home.editing; text: "Done"; primary: true; onClicked: home.editing = false }
        }
    }

    // ---- tiles
    Component {
        id: appTile
        Item {
            width: 104; height: 112
            readonly property var info: home.appInfo(parent ? parent.it.id : "")
            Rectangle {
                id: bubble
                width: 72; height: 72; radius: 20
                anchors.horizontalCenter: parent.horizontalCenter
                color: tileArea.containsMouse ? "#40ffffff" : "#26ffffff"
                border.color: Theme.cardBorder
                Kirigami.Icon { anchors.centerIn: parent; width: 52; height: 52; source: parent.parent.info.icon }
            }
            Rectangle {
                anchors { top: bubble.bottom; topMargin: 6; horizontalCenter: parent.horizontalCenter }
                width: Math.min(parent.width, label.implicitWidth + 14); height: 22; radius: 11
                color: "#80242a32"
                Text {
                    id: label
                    anchors.centerIn: parent; width: parent.width - 10
                    horizontalAlignment: Text.AlignHCenter; elide: Text.ElideRight
                    text: parent.parent.info.name; color: Theme.ink; font.family: Theme.font; font.pixelSize: 12
                }
            }
            MouseArea {
                id: tileArea; anchors.fill: parent; hoverEnabled: true
                pressAndHoldInterval: 600
                onPressAndHold: home.editing = true
                onClicked: if (!home.editing && home.runner) home.runner.run("open-app " + parent.info.id)
            }
        }
    }
    Component {
        id: widgetTile
        Loader {
            readonly property string kind: parent ? parent.it.k : ""
            sourceComponent: ({ clock: clockC, weather: weatherC, sea: seaC, system: systemC, photo: photoC,
                                focus: focusC, projects: projectsC, servers: serversC, links: linksC })[kind] || null
            onLoaded: if (item.hasOwnProperty("runner")) item.runner = home.runner
        }
    }
    Component { id: clockC; ClockWidget {} }
    Component { id: weatherC; WeatherWidget {} }
    Component { id: seaC; SeaWidget {} }
    Component { id: systemC; SystemWidget {} }
    Component { id: photoC; PhotoWidget {} }
    Component { id: focusC; FocusWidget {} }
    Component { id: projectsC; ProjectsWidget {} }
    Component { id: serversC; ServersWidget {} }
    Component { id: linksC; LinksWidget {} }

    // ---- add an app
    QQC2.Popup {
        id: appSheet
        anchors.centerIn: parent
        width: Math.min(460, home.width - 40); height: Math.min(560, home.height - 40)
        modal: true
        background: Rectangle { radius: Theme.radius; color: "#f2242a32"; border.color: Theme.cardBorder }
        contentItem: Column {
            spacing: 10
            Header { width: parent.width; icon: "➕"; title: "Add an app"; note: home.allApps.length + " apps" }
            QQC2.TextField { id: search; width: parent.width; placeholderText: "Search…" }
            ListView {
                width: parent.width; height: appSheet.height - 110; clip: true
                model: home.allApps.filter(function (a) { return !search.text || a.name.toLowerCase().indexOf(search.text.toLowerCase()) >= 0 })
                delegate: Rectangle {
                    width: ListView.view.width; height: 44; radius: 10
                    color: rowArea.containsMouse ? "#22ffffff" : "transparent"
                    Row {
                        anchors { verticalCenter: parent.verticalCenter; left: parent.left; leftMargin: 10 }
                        spacing: 12
                        Kirigami.Icon { width: 28; height: 28; source: modelData.icon }
                        Text { text: modelData.name; color: Theme.ink; font.family: Theme.font; font.pixelSize: 14; anchors.verticalCenter: parent.verticalCenter }
                    }
                    MouseArea { id: rowArea; anchors.fill: parent; hoverEnabled: true
                                onClicked: { home.addToCurrent({ t: "app", id: modelData.id }); appSheet.close() } }
                }
            }
        }
    }
    // ---- add a widget
    QQC2.Popup {
        id: widgetSheet
        anchors.centerIn: parent
        width: Math.min(420, home.width - 40)
        modal: true
        background: Rectangle { radius: Theme.radius; color: "#f2242a32"; border.color: Theme.cardBorder }
        contentItem: Column {
            spacing: 8
            Header { width: parent.width; icon: "🧩"; title: "Add a widget" }
            Flow {
                width: parent.width; spacing: 8
                Repeater {
                    model: home.widgetKinds
                    Pill { text: modelData.name; onClicked: { home.addToCurrent({ t: "widget", k: modelData.k }); widgetSheet.close() } }
                }
            }
        }
    }
}
