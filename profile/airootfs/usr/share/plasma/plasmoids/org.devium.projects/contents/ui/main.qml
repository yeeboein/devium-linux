import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import org.devium.widgets
import org.kde.plasma.plasma5support as P5Support

PlasmoidItem {
    id: root
    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: Plasmoid.formFactor === PlasmaCore.Types.Planar ? fullRepresentation : compactRepresentation
    // the accent colour picked in Devium Tools > Look (KDE's highlight colour)
    Binding { target: Theme; property: "accent"; value: Kirigami.Theme.highlightColor }
    property var repos: []
    P5Support.DataSource {
        id: exec
        engine: "executable"
        connectedSources: []
        onNewData: (source, d) => { disconnectSource(source); root.got(source, d["stdout"] || "") }
    }
    function run(args) { exec.connectSource("/usr/lib/devium/widget-data " + args) }
    function got(src, out) { if (src.indexOf(" projects") > 0) { try { root.repos = JSON.parse(out) } catch (e) {} } }
    Timer { interval: 20000; running: true; repeat: true; triggeredOnStart: true; onTriggered: root.run("projects") }
    fullRepresentation: ProjectsView {
        Layout.minimumWidth: 350; Layout.minimumHeight: 290
        Layout.preferredWidth: 350; Layout.preferredHeight: 290
        repos: root.repos
        onOpen: (path) => root.run("open '" + path.replace(/'/g, "") + "'")
        onTerminal: (path) => root.run("term '" + path.replace(/'/g, "") + "'")
    }
}
