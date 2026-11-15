// Devium widget pack: shared colours and sizes. The accent follows the accent colour picked in
// Devium Tools > Look (each widget binds `accent` to KDE's highlight colour).
pragma Singleton
import QtQuick

QtObject {
    property color accent: "#8fb4d8"
    readonly property color accent2: Qt.hsla((accent.hslHue + 0.07) % 1.0, accent.hslSaturation * 0.85,
                                             Math.min(0.92, accent.hslLightness + 0.06), 1)
    readonly property color card: "#d9242a32"
    readonly property color cardBorder: "#2effffff"
    readonly property color well: "#1affffff"
    readonly property color ink: "#eef2f7"
    readonly property color soft: "#c4ccd6"
    readonly property color subtle: "#8a96a4"
    readonly property color good: "#8fd4b8"
    readonly property color warn: "#e8cd96"
    readonly property color bad: "#e89ca0"
    readonly property string font: "Noto Sans"
    readonly property int radius: 22
    readonly property int pad: 18
}
