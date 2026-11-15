import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import org.devium.widgets

PlasmoidItem {
    id: root
    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: Plasmoid.formFactor === PlasmaCore.Types.Planar ? fullRepresentation : compactRepresentation
    // the accent colour picked in Devium Tools > Look (KDE's highlight colour)
    Binding { target: Theme; property: "accent"; value: Kirigami.Theme.highlightColor }
    property var info: ({ ok: false, error: "" })
    property bool loading: true
    function reload() {
        loading = true
        Sea.load(Plasmoid.configuration.place, Plasmoid.configuration.imperial, function (m) { root.info = m; root.loading = false })
    }
    Timer { interval: 30 * 60 * 1000; running: true; repeat: true; triggeredOnStart: true; onTriggered: root.reload() }
    Connections {
        target: Plasmoid.configuration
        function onPlaceChanged() { root.reload() }
        function onImperialChanged() { root.reload() }
    }
    Plasmoid.contextualActions: [ PlasmaCore.Action { text: "Refresh"; icon.name: "view-refresh"; onTriggered: root.reload() } ]
    toolTipMainText: "Sea"
    toolTipSubText: info.ok ? info.waves + " waves, water " + info.water + " (" + info.place + ")" : (info.error || "")
    fullRepresentation: SeaView {
        Layout.minimumWidth: 330; Layout.minimumHeight: 290
        Layout.preferredWidth: 330; Layout.preferredHeight: 290
        info: root.info; loading: root.loading
        onRefresh: root.reload()
    }
}
