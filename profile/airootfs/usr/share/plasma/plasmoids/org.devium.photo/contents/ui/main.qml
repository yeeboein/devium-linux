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
    Binding { target: Theme; property: "accent"; value: Kirigami.Theme.highlightColor }
    fullRepresentation: PhotoView {
        Layout.minimumWidth: 160; Layout.minimumHeight: 120
        Layout.preferredWidth: 330; Layout.preferredHeight: 250
        folder: Plasmoid.configuration.folder
        image: Plasmoid.configuration.image
        interval: Plasmoid.configuration.interval
        shuffle: Plasmoid.configuration.shuffle
        crop: Plasmoid.configuration.crop
        caption: Plasmoid.configuration.caption
    }
}
