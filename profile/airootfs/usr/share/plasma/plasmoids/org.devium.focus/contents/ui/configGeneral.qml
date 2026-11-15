import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_workMinutes: workMinutes.value
    property alias cfg_breakMinutes: breakMinutes.value
    Kirigami.FormLayout {
        QQC2.SpinBox { id: workMinutes; Kirigami.FormData.label: "Focus minutes:"; from: 1; to: 180 }
        QQC2.SpinBox { id: breakMinutes; Kirigami.FormData.label: "Break minutes:"; from: 1; to: 180 }
    }
}
