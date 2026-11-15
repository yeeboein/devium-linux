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
    P5Support.DataSource {
        id: exec
        engine: "executable"
        connectedSources: []
        onNewData: (source, d) => { disconnectSource(source); root.got(source, d["stdout"] || "") }
    }
    function run(args) { exec.connectSource("/usr/lib/devium/widget-data " + args) }
    function got(src, out) {}
    function today() { return Qt.formatDate(new Date(), "yyyy-MM-dd") }
    fullRepresentation: FocusView {
        Layout.minimumWidth: 250; Layout.minimumHeight: 240
        Layout.preferredWidth: 250; Layout.preferredHeight: 240
        workMinutes: Plasmoid.configuration.workMinutes
        breakMinutes: Plasmoid.configuration.breakMinutes
        doneToday: Plasmoid.configuration.doneDate === root.today() ? Plasmoid.configuration.doneCount : 0
        onFinished: (wasBreak) => {
            root.run("focus " + (wasBreak ? "break" : "work"))
            if (!wasBreak) {
                if (Plasmoid.configuration.doneDate !== root.today()) {
                    Plasmoid.configuration.doneDate = root.today()
                    Plasmoid.configuration.doneCount = 0
                }
                Plasmoid.configuration.doneCount = Plasmoid.configuration.doneCount + 1
            }
        }
    }
}
