// Devium login screen for SDDM (Qt 6). Plain QtQuick, so it works without Plasma
// (KDE Plasma and Hyprland editions).
import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#2b323b"

    readonly property color accent: config.accent || "#8fb4d8"
    readonly property color accent2: config.accent2 || "#b4b8e0"
    readonly property color ink: "#eef2f7"
    readonly property color soft: "#c4ccd6"
    property int sessionIndex: (sessionModel && sessionModel.lastIndex >= 0) ? sessionModel.lastIndex : 0

    // ---- the mountains, slightly darkened so the text reads well
    Image {
        anchors.fill: parent
        source: config.background || "background.jpg"
        fillMode: Image.PreserveAspectCrop
        smooth: true
        asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#40141a22" }
            GradientStop { position: 0.55; color: "#26141a22" }
            GradientStop { position: 1.0; color: "#b0141a22" }
        }
    }

    // ---- Devium logo, top left
    Row {
        anchors { left: parent.left; top: parent.top; margins: 36 }
        spacing: 14
        Image { source: "logo-white.png"; width: 44; height: 44; fillMode: Image.PreserveAspectFit; smooth: true }
        Text {
            text: "Devium"
            color: root.ink
            font.family: "Noto Sans"; font.pixelSize: 26; font.weight: Font.DemiBold
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    // ---- big clock
    Column {
        id: clock
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height * 0.17
        spacing: 2
        Text {
            id: timeText
            anchors.horizontalCenter: parent.horizontalCenter
            color: root.ink
            font.family: "Noto Sans"; font.pixelSize: 120; font.weight: Font.Bold
            style: Text.Raised; styleColor: "#33000000"
        }
        Text {
            id: dateText
            anchors.horizontalCenter: parent.horizontalCenter
            color: root.soft
            font.family: "Noto Sans"; font.pixelSize: 26
        }
        Timer {
            interval: 1000; running: true; repeat: true; triggeredOnStart: true
            onTriggered: {
                var now = new Date()
                timeText.text = Qt.formatTime(now, "hh:mm")
                dateText.text = Qt.formatDate(now, "dddd d MMMM")
            }
        }
    }

    // ---- the login card
    Rectangle {
        id: card
        width: 420
        height: col.implicitHeight + 56
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height * 0.48
        radius: 28
        color: "#b3242a32"
        border.color: "#33ffffff"
        border.width: 1

        Column {
            id: col
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 28 }
            spacing: 14

            // avatar: the user's picture, or the Devium logo in a circle
            Rectangle {
                width: 92; height: 92; radius: 46
                anchors.horizontalCenter: parent.horizontalCenter
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: root.accent }
                    GradientStop { position: 1.0; color: root.accent2 }
                }
                Image {
                    anchors.centerIn: parent
                    source: "logo-white.png"; width: 54; height: 54
                    fillMode: Image.PreserveAspectFit; smooth: true
                }
            }

            TextField {
                id: userField
                width: parent.width
                height: 50
                text: userModel.lastUser
                placeholderText: "User name"
                color: root.ink
                placeholderTextColor: "#8a96a4"
                font.family: "Noto Sans"; font.pixelSize: 18
                horizontalAlignment: TextInput.AlignHCenter
                leftPadding: 16; rightPadding: 16
                background: Rectangle { radius: 14; color: "#33ffffff"; border.color: userField.activeFocus ? root.accent : "#22ffffff"; border.width: 1 }
                KeyNavigation.tab: passwordField
                onAccepted: passwordField.forceActiveFocus()
            }

            Item {
                width: parent.width
                height: 50
                TextField {
                    id: passwordField
                    anchors { left: parent.left; right: goButton.left; rightMargin: 10 }
                    height: 50
                    echoMode: TextInput.Password
                    placeholderText: "Password"
                    color: root.ink
                    placeholderTextColor: "#8a96a4"
                    font.family: "Noto Sans"; font.pixelSize: 18
                    leftPadding: 16; rightPadding: 16
                    background: Rectangle { radius: 14; color: "#33ffffff"; border.color: passwordField.activeFocus ? root.accent : "#22ffffff"; border.width: 1 }
                    focus: true
                    onAccepted: root.doLogin()
                    KeyNavigation.backtab: userField
                }
                Rectangle {
                    id: goButton
                    width: 50; height: 50; radius: 14
                    anchors.right: parent.right
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: goArea.containsMouse ? Qt.lighter(root.accent, 1.1) : root.accent }
                        GradientStop { position: 1.0; color: goArea.containsMouse ? Qt.lighter(root.accent2, 1.1) : root.accent2 }
                    }
                    Text { anchors.centerIn: parent; text: "➜"; color: "#1b2026"; font.pixelSize: 24 }
                    MouseArea { id: goArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: root.doLogin() }
                }
            }

            Text {
                id: message
                width: parent.width
                horizontalAlignment: Text.AlignHCenter
                color: "#f0b2b5"
                font.family: "Noto Sans"; font.pixelSize: 15
                text: ""
                visible: text.length > 0
            }
        }
    }

    // ---- bottom bar: session on the left, restart / shut down on the right
    Row {
        anchors { left: parent.left; bottom: parent.bottom; margins: 30 }
        spacing: 10
        Text { text: "Desktop:"; color: root.soft; font.family: "Noto Sans"; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter }
        ComboBox {
            id: sessionBox
            width: 240; height: 40
            model: sessionModel
            textRole: "name"
            currentIndex: root.sessionIndex
            onActivated: root.sessionIndex = currentIndex
            font.family: "Noto Sans"; font.pixelSize: 15
            contentItem: Text {
                leftPadding: 14
                text: sessionBox.displayText
                color: root.ink
                font: sessionBox.font
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }
            background: Rectangle { radius: 12; color: "#66242a32"; border.color: "#33ffffff"; border.width: 1 }
        }
    }

    Row {
        anchors { right: parent.right; bottom: parent.bottom; margins: 30 }
        spacing: 12
        Repeater {
            model: [
                { label: "Restart", act: "reboot", ok: sddm.canReboot },
                { label: "Shut down", act: "poweroff", ok: sddm.canPowerOff }
            ]
            delegate: Rectangle {
                visible: modelData.ok
                width: btnText.implicitWidth + 36; height: 40; radius: 12
                color: btnArea.containsMouse ? "#99242a32" : "#66242a32"
                border.color: "#33ffffff"; border.width: 1
                Text { id: btnText; anchors.centerIn: parent; text: modelData.label; color: root.ink; font.family: "Noto Sans"; font.pixelSize: 15 }
                MouseArea {
                    id: btnArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                    onClicked: modelData.act === "reboot" ? sddm.reboot() : sddm.powerOff()
                }
            }
        }
    }

    // ---- logging in
    function doLogin() {
        message.text = ""
        sddm.login(userField.text, passwordField.text, root.sessionIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            message.text = "That password didn't work. Try again."
            passwordField.text = ""
            passwordField.forceActiveFocus()
            shake.start()
        }
    }

    SequentialAnimation {
        id: shake
        NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"; to: -14; duration: 50 }
        NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"; to: 14; duration: 70 }
        NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"; to: -8; duration: 60 }
        NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"; to: 0; duration: 50 }
    }

    Component.onCompleted: {
        if (userField.text.length === 0)
            userField.forceActiveFocus()
        else
            passwordField.forceActiveFocus()
    }
}
