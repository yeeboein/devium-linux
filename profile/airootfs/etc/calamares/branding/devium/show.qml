import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation
    function nextSlide() { presentation.goToNextSlide(); }
    Timer { interval: 9000; running: presentation.activatedInCalamares; repeat: true; onTriggered: nextSlide() }

    Rectangle { anchors.fill: parent; color: "#2b323b"; z: -1 }

    Slide {
        Image { id: logo1; source: "logo.png"; width: 140; height: 140; fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter; y: parent.height * 0.18 }
        Text { anchors.top: logo1.bottom; anchors.topMargin: 24; anchors.horizontalCenter: parent.horizontalCenter
               width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap
               color: "#dde3ea"; font.pixelSize: 22
               text: "Installing Devium<br><span style='font-size:15px; color:#96b2d0'>Light. Fast. Made for coding.</span>" }
    }
    Slide {
        Text { anchors.centerIn: parent; width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter
               wrapMode: Text.WordWrap; color: "#dde3ea"; font.pixelSize: 18
               text: "<b>You choose what's installed</b><br><br>After you restart, <b>Devium Setup</b> lets you pick your browser, code editor, languages, games and apps. Every choice shows how much space it uses." }
    }
    Slide {
        Text { anchors.centerIn: parent; width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter
               wrapMode: Text.WordWrap; color: "#dde3ea"; font.pixelSize: 18
               text: "<b>Handy shortcuts</b><br><br>Meta+Shift+S: snip part of the screen<br>Meta+U: updates<br>Meta+T: Devium Tools<br>Type <b>support</b> in a terminal for helpful commands" }
    }
    Slide {
        Text { anchors.centerIn: parent; width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter
               wrapMode: Text.WordWrap; color: "#dde3ea"; font.pixelSize: 18
               text: "<b>Light on old laptops</b><br><br>Compressed memory, a battery saver and KDE Lite keep Devium fast, even with 2-4 GB of RAM." }
    }
    Slide {
        Text { anchors.centerIn: parent; width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter
               wrapMode: Text.WordWrap; color: "#dde3ea"; font.pixelSize: 18
               text: "<b>Dual boot</b><br><br>Installed next to Windows? When your computer starts, pick <b>Devium</b> or <b>Windows</b> from the boot menu." }
    }

    Slide {
        Text { anchors.centerIn: parent; width: parent.width * 0.8; horizontalAlignment: Text.AlignHCenter
               wrapMode: Text.WordWrap; color: "#dde3ea"; font.pixelSize: 18
               text: "<b>When it's finished</b><br><br>Shut down and <b>remove the USB stick</b> (or, in a virtual machine, <b>remove the ISO</b> from the virtual DVD drive), then start your computer. Otherwise the installer starts again." }
    }
    // "Join our Discord" button, always visible. Clicking it shows a QR code to scan with a phone
    // (the live system has no web browser).
    Rectangle {
        id: discordBtn
        z: 10
        anchors.right: parent.right; anchors.bottom: parent.bottom; anchors.margins: 14
        width: discordLabel.width + 28; height: 36; radius: 18
        color: discordArea.containsMouse ? "#6f7dd8" : "#5865f2"
        Text { id: discordLabel; anchors.centerIn: parent; color: "white"; font.pixelSize: 14; font.bold: true
               text: "Join the Devium Discord" }
        MouseArea { id: discordArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                    onClicked: qrPopup.visible = true }
    }
    Rectangle {
        id: qrPopup
        visible: false
        z: 20
        anchors.fill: parent
        color: "#e6242a32"
        MouseArea { anchors.fill: parent; onClicked: qrPopup.visible = false }
        Column {
            anchors.centerIn: parent
            spacing: 12
            Text { anchors.horizontalCenter: parent.horizontalCenter; color: "#dde3ea"; font.pixelSize: 20; font.bold: true
                   text: "Scan with your phone's camera" }
            Rectangle {
                anchors.horizontalCenter: parent.horizontalCenter
                width: Math.min(qrPopup.height * 0.55, 260); height: width; radius: 12; color: "white"
                Image { anchors.fill: parent; anchors.margins: 8; source: "discord-qr.png"; smooth: false
                        fillMode: Image.PreserveAspectFit }
            }
            Text { anchors.horizontalCenter: parent.horizontalCenter; color: "#96b2d0"; font.pixelSize: 16
                   text: "discord.gg/YTMattgyG3" }
            Text { anchors.horizontalCenter: parent.horizontalCenter; color: "#8a95a3"; font.pixelSize: 13
                   text: "Help, news and new betas. Click anywhere to close." }
        }
    }
}
