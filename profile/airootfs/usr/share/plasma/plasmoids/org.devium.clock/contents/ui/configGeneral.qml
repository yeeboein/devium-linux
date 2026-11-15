import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_twelveHour: twelveHour.checked
    property alias cfg_greetByName: greetByName.checked
    Kirigami.FormLayout {
        QQC2.CheckBox { id: twelveHour; text: "12-hour clock" }
        QQC2.CheckBox { id: greetByName; text: "Greet me by name" }
    }
}
