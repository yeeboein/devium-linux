// Devium Home: iPhone-style home screen pages for KDE (optional: Customise > "Home screen pages").
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasma5support as P5Support
import org.devium.widgets

PlasmoidItem {
    id: root
    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: fullRepresentation
    Binding { target: Theme; property: "accent"; value: Kirigami.Theme.highlightColor }

    // run /usr/lib/devium/widget-data (apps list, opening apps, the widgets' data)
    QtObject {
        id: runner
        signal done(string args, string out)
        function run(args) { exec.connectSource("/usr/lib/devium/widget-data " + args) }
    }
    P5Support.DataSource {
        id: exec
        engine: "executable"
        connectedSources: []
        onNewData: (source, d) => {
            disconnectSource(source)
            runner.done(source.replace("/usr/lib/devium/widget-data ", ""), d["stdout"] || "")
        }
    }

    fullRepresentation: HomeView {
        Layout.minimumWidth: 400; Layout.minimumHeight: 300
        Layout.preferredWidth: 1200; Layout.preferredHeight: 700
        runner: runner
        pagesJson: Plasmoid.configuration.pages
        onSave: (json) => Plasmoid.configuration.pages = json
    }
}
