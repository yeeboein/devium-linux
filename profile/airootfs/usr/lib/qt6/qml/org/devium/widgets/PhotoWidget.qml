// Photo widget with its own settings (used on Xfce and Hyprland; Plasma has its own glue).
import QtQuick
PhotoView {
    id: w
    property var runner: null
    property bool imperial: false
    property string place: ""
    width: 330; height: 250
}
