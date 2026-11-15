// System card: CPU, memory and disk rings, plus temperature, battery and uptime.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var info: ({})
    implicitWidth: 340; implicitHeight: 200
    ColumnLayout {
        anchors.fill: parent; spacing: 10
        Header { Layout.fillWidth: true; icon: "💻"; title: "System"; note: v.info.uptime ? "up " + v.info.uptime : "" }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter; spacing: 20
            Ring { value: (v.info.cpu || 0) / 100; label: "CPU" }
            Ring { value: v.info.ramTotal ? v.info.ramUsed / v.info.ramTotal : 0; label: "Memory"
                   text: v.info.ramUsed !== undefined ? (v.info.ramUsed / 1073741824).toFixed(1) + "G" : "–" }
            Ring { value: v.info.diskTotal ? v.info.diskUsed / v.info.diskTotal : 0; label: "Disk" }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter; spacing: 18
            Text { visible: v.info.temp !== null && v.info.temp !== undefined; text: "🌡 " + Math.round(v.info.temp || 0) + "°C"
                   color: (v.info.temp || 0) >= 85 ? Theme.bad : (v.info.temp || 0) >= 70 ? Theme.warn : Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
            Text { visible: v.info.battery !== null && v.info.battery !== undefined
                   text: (v.info.charging ? "⚡ " : "🔋 ") + (v.info.battery || 0) + "%"
                   color: (v.info.battery || 100) <= 15 && !v.info.charging ? Theme.bad : Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
            Text { text: v.info.diskTotal ? "💾 " + ((v.info.diskTotal - v.info.diskUsed) / 1073741824).toFixed(0) + " GB free" : ""
                   color: Theme.soft; font.family: Theme.font; font.pixelSize: 12 }
        }
    }
}
