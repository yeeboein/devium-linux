import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_place: place.text
    property alias cfg_imperial: imperial.checked
    Kirigami.FormLayout {
        QQC2.TextField { id: place; Kirigami.FormData.label: "Place:"; placeholderText: "e.g. Salthill, Galway"; Layout.preferredWidth: Kirigami.Units.gridUnit * 16 }
        QQC2.Label { text: "Leave empty to use your approximate location (from your IP address)"; wrapMode: Text.WordWrap; opacity: 0.7; Layout.preferredWidth: Kirigami.Units.gridUnit * 18 }
        QQC2.CheckBox { id: imperial; text: "Use feet and °F" }
    }
}
