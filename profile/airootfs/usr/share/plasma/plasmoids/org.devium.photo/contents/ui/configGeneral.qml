import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import QtQuick.Dialogs
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_folder: folder.text
    property alias cfg_image: image.text
    property alias cfg_interval: interval.value
    property alias cfg_shuffle: shuffle.checked
    property alias cfg_crop: crop.checked
    property alias cfg_caption: caption.checked

    FolderDialog { id: folderDialog; onAccepted: folder.text = String(selectedFolder).replace("file://", "") }
    FileDialog {
        id: fileDialog
        nameFilters: ["Pictures (*.jpg *.jpeg *.png *.webp *.gif *.bmp)"]
        onAccepted: image.text = String(selectedFile).replace("file://", "")
    }

    Kirigami.FormLayout {
        RowLayout {
            Kirigami.FormData.label: "Slideshow folder:"
            QQC2.TextField { id: folder; placeholderText: "Your Pictures folder"; Layout.preferredWidth: Kirigami.Units.gridUnit * 14 }
            QQC2.Button { icon.name: "folder-open"; onClicked: folderDialog.open() }
        }
        RowLayout {
            Kirigami.FormData.label: "Or one picture:"
            QQC2.TextField { id: image; placeholderText: "Leave empty for a slideshow"; Layout.preferredWidth: Kirigami.Units.gridUnit * 14 }
            QQC2.Button { icon.name: "document-open"; onClicked: fileDialog.open() }
            QQC2.Button { icon.name: "edit-clear"; onClicked: image.text = ""; visible: image.text.length > 0 }
        }
        QQC2.SpinBox { id: interval; Kirigami.FormData.label: "Seconds per picture:"; from: 3; to: 3600 }
        QQC2.CheckBox { id: shuffle; text: "Random order" }
        QQC2.CheckBox { id: crop; text: "Fill the widget (crop the picture)" }
        QQC2.CheckBox { id: caption; text: "Show the picture's name" }
    }
}
