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
               text: "<b>Handy shortcuts</b><br><br>Meta+Shift+S: snip part of the screen<br>Meta+U: updates<br>Meta+F1: Devium Welcome<br>Type <b>support</b> in a terminal for helpful commands" }
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
}
