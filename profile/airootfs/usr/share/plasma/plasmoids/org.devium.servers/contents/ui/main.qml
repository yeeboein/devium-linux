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
    property var servers: []
    P5Support.DataSource {
        id: exec
        engine: "executable"
        connectedSources: []
        onNewData: (source, d) => { disconnectSource(source); root.got(source, d["stdout"] || "") }
    }
    function run(args) { exec.connectSource("/usr/lib/devium/widget-data " + args) }
    function got(src, out) { if (src.indexOf(" ports") > 0) { try { root.servers = JSON.parse(out) } catch (e) {} } }
    Timer { interval: 5000; running: true; repeat: true; triggeredOnStart: true; onTriggered: root.run("ports") }
    fullRepresentation: ServersView {
        Layout.minimumWidth: 310; Layout.minimumHeight: 220
        Layout.preferredWidth: 310; Layout.preferredHeight: 220
        servers: root.servers
        onOpen: (port) => Qt.openUrlExternally("http://localhost:" + port)
        onStop: (pid) => { root.run("stop " + pid); refreshSoon.restart() }
        Timer { id: refreshSoon; interval: 800; onTriggered: root.run("ports") }
    }
}
