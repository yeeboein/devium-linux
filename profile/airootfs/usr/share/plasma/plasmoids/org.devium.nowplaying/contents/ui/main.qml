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
    function got(src, out) {
        if (src.indexOf("nowplaying") < 0) return
        try { root.info = JSON.parse(out) } catch (e) {}
    }
    // quick while a song is on, slow when nothing is playing (light on old laptops)
    Timer { interval: root.info.title ? 2000 : 6000; running: true; repeat: true; triggeredOnStart: true
            onTriggered: root.run("nowplaying") }
    Timer { id: refresh; interval: 500; onTriggered: root.run("nowplaying") }
    toolTipMainText: info.title ? info.title : "Now playing"
    toolTipSubText: info.title ? (info.artist || "") : "Nothing is playing"
    fullRepresentation: NowPlayingView {
        Layout.minimumWidth: 300; Layout.minimumHeight: 200
        Layout.preferredWidth: 340; Layout.preferredHeight: 208
        info: root.info
        onControl: (action) => { root.run("media " + action); refresh.restart() }
    }
}
