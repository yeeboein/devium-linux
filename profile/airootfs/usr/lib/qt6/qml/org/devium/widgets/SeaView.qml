// Sea conditions card: waves, swell, water temperature, wind and the tide.
import QtQuick
import QtQuick.Layouts

Card {
    id: v
    property var info: ({ ok: false, place: "", error: "Loading…" })
    property bool loading: false
    signal refresh()
    implicitWidth: 340; implicitHeight: 300
    ColumnLayout {
        anchors.fill: parent
        spacing: 10
        Header { Layout.fillWidth: true; icon: "🌊"; title: "Sea"; note: v.info.place || "" }
        // big line: wave height + how it feels
        RowLayout {
            visible: v.info.ok
            spacing: 12
            Text { text: v.info.waves || ""; color: Theme.ink; font.family: Theme.font; font.pixelSize: 40; font.weight: Font.Bold }
            Column {
                Layout.alignment: Qt.AlignVCenter
                Rectangle {
                    radius: 10; height: 22; width: rt.implicitWidth + 18
                    color: v.info.rating ? Qt.rgba(Theme[v.info.rating.level].r, Theme[v.info.rating.level].g, Theme[v.info.rating.level].b, 0.22) : "transparent"
                    Text { id: rt; anchors.centerIn: parent; text: v.info.rating ? v.info.rating.text : ""
                           color: v.info.rating ? Theme[v.info.rating.level] : Theme.ink; font.family: Theme.font; font.pixelSize: 12; font.weight: Font.DemiBold }
                }
                Text { text: "waves " + (v.info.waveArrow || "") + " from " + (v.info.waveDir || "") + (v.info.period ? " · every " + v.info.period : "")
                       color: Theme.soft; font.family: Theme.font; font.pixelSize: 12; topPadding: 4 }
            }
        }
        GridLayout {
            visible: v.info.ok
            columns: 3; columnSpacing: 18; rowSpacing: 4
            Stat { label: "Swell"; value: v.info.swell || "–"; sub: v.info.swellDir ? "from " + v.info.swellDir : "" }
            Stat { label: "Water"; value: v.info.water || "–" }
            Stat { label: "Wind " + (v.info.windArrow || ""); value: v.info.wind || "–"; sub: v.info.windSub || "" }
        }
        Spark { visible: v.info.ok && (v.info.curve || []).length > 1; Layout.fillWidth: true; values: v.info.curve || []; nowAt: v.info.nowAt || 0 }
        RowLayout {
            visible: v.info.ok
            Text { text: v.info.tideText || ""; color: Theme.soft; font.family: Theme.font; font.pixelSize: 12; Layout.fillWidth: true; elide: Text.ElideRight }
            Text { text: v.info.sun || ""; color: Theme.subtle; font.family: Theme.font; font.pixelSize: 11 }
        }
        Text {
            visible: !v.info.ok
            Layout.fillWidth: true; Layout.fillHeight: true
            text: v.loading ? "Checking the sea…" : (v.info.error || "")
            color: Theme.soft; font.family: Theme.font; font.pixelSize: 13; wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter
        }
        Item { Layout.fillHeight: true; visible: v.info.ok }
    }
    MouseArea { anchors.fill: parent; z: -1; onDoubleClicked: v.refresh() }
}
