// Devium widgets on Hyprland (Wayland), drawn by Quickshell on the desktop layer behind your windows.
// Started by devium-desk-widgets; pick widgets in Devium Tools > Look. Drag a widget to move it.
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import org.devium.widgets

ShellRoot {
    id: root
    readonly property string cfgPath: Quickshell.env("HOME") + "/.config/devium/desk-widgets.json"
    property var cfg: ({ widgets: [] })
    property bool ignoreNext: false   // our own save shouldn't reload everything
    readonly property var types: ({ clock: clockC, weather: weatherC, sea: seaC, system: systemC,
                                    focus: focusC, projects: projectsC, servers: serversC, links: linksC })

    FileView {
        id: file
        path: root.cfgPath
        blockLoading: true
        watchChanges: true
        onFileChanged: { if (root.ignoreNext) { root.ignoreNext = false; return } if (!saveTimer.running) reload() }
        onLoaded: { try { root.cfg = JSON.parse(text()) } catch (e) { root.cfg = { widgets: [] } } }
    }
    Timer { id: saveTimer; interval: 600; onTriggered: { root.ignoreNext = true; file.setText(JSON.stringify(root.cfg, null, 1) + "\n") } }

    // run /usr/lib/devium/widget-data and hand the answer to the widgets
    QtObject {
        id: runner
        signal done(string args, string out)
        function run(args) { procC.createObject(root, { args: args }) }
    }
    Component {
        id: procC
        Process {
            id: proc
            property string args
            running: true
            command: {
                var i = args.indexOf(" "), head = i < 0 ? args : args.substring(0, i), rest = i < 0 ? "" : args.substring(i + 1)
                return ["/usr/lib/devium/widget-data"].concat((head === "open" || head === "term") && rest ? [head, rest] : args.split(" "))
            }
            stdout: StdioCollector { onStreamFinished: { runner.done(proc.args, text); proc.destroy() } }
        }
    }

    Component { id: clockC; ClockWidget {} }
    Component { id: weatherC; WeatherWidget {} }
    Component { id: seaC; SeaWidget {} }
    Component { id: systemC; SystemWidget {} }
    Component { id: focusC; FocusWidget {} }
    Component { id: projectsC; ProjectsWidget {} }
    Component { id: serversC; ServersWidget {} }
    Component { id: linksC; LinksWidget {} }

    Variants {
        model: (root.cfg.widgets || []).map(function (w, i) { return i })
        PanelWindow {
            id: win
            required property var modelData          // the widget's number in the settings
            readonly property var w: root.cfg.widgets[modelData] || ({})
            readonly property int index: modelData
            screen: Quickshell.screens[0]
            anchors.top: true
            anchors.left: true
            margins.left: w.x !== undefined ? w.x : (screen ? screen.width - 380 : 900)
            margins.top: w.y !== undefined ? w.y : 60 + index * 260
            exclusionMode: ExclusionMode.Ignore
            exclusiveZone: 0
            color: "transparent"
            WlrLayershell.namespace: "devium-widgets"
            WlrLayershell.layer: WlrLayer.Bottom
            WlrLayershell.keyboardFocus: WlrKeyboardFocus.None
            implicitWidth: loader.item ? loader.item.width : 300
            implicitHeight: loader.item ? loader.item.height : 200
            Loader {
                id: loader
                sourceComponent: root.types[win.w.id] || null
                onLoaded: {
                    item.runner = runner
                    item.place = root.cfg.place || ""
                    item.imperial = !!root.cfg.imperial
                }
            }
            // drag anywhere on the card to move it
            MouseArea {
                anchors.fill: parent; z: -1
                property point start
                property point startMargins
                onPressed: (m) => { start = mapToGlobal(m.x, m.y); startMargins = Qt.point(win.margins.left, win.margins.top) }
                onPositionChanged: (m) => {
                    var p = mapToGlobal(m.x, m.y)
                    win.margins.left = Math.max(0, startMargins.x + p.x - start.x)
                    win.margins.top = Math.max(0, startMargins.y + p.y - start.y)
                }
                onReleased: {
                    root.cfg.widgets[win.index].x = Math.round(win.margins.left)
                    root.cfg.widgets[win.index].y = Math.round(win.margins.top)
                    saveTimer.restart()
                }
            }
        }
    }
}
