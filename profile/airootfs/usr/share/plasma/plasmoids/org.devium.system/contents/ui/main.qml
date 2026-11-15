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
    property var info: ({})
    P5Support.DataSource {
        id: exec
        engine: "executable"
        connectedSources: []
        onNewData: (source, d) => { disconnectSource(source); root.got(source, d["stdout"] || "") }
    }
    function run(args) { exec.connectSource("/usr/lib/devium/widget-data " + args) }
    function got(src, out) { try { root.info = JSON.parse(out) } catch (e) {} }
    Timer { interval: 4000; running: true; repeat: true; triggeredOnStart: true; onTriggered: root.run("sys") }
    toolTipMainText: "System"
    toolTipSubText: "CPU " + (info.cpu || 0) + "%"
    fullRepresentation: SystemView {
        Layout.minimumWidth: 330; Layout.minimumHeight: 190
        Layout.preferredWidth: 330; Layout.preferredHeight: 190
        info: root.info
        MouseArea { anchors.fill: parent; z: -1; onDoubleClicked: exec.connectSource("/usr/lib/devium/widget-data launch devium-tools health") }
    }
}
