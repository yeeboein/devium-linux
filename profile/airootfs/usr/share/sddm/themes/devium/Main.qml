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
    readonly property string avatarUrl: avatar === "" ? "" : (avatar.indexOf("/") === 0 ? "file://" + avatar : avatar)

    // The accounts on this computer (Guest gets its own button). The login card shows one account's name;
    // with several accounts, small arrows switch between them. Nobody types a user name.
    property var accounts: []          // [{ name, realName, icon }]
    property bool hasGuest: false
    property int current: 0
    readonly property var account: accounts.length ? accounts[Math.min(current, accounts.length - 1)] : ({ name: "", realName: "", icon: "" })
    readonly property string currentUser: account.name
    readonly property string displayName: account.realName && account.realName.length ? account.realName : account.name
    readonly property string avatar: customIcon(account.icon)
    Repeater {
        model: userModel
        delegate: Item {
            visible: false
            Component.onCompleted: {
                if (model.name === "guest") { root.hasGuest = true; return }
                var list = root.accounts.slice()
                list.push({ name: model.name, realName: model.realName || "", icon: model.icon ? String(model.icon) : "" })
                list.sort(function (a, b) { return a.name < b.name ? -1 : 1 })
                root.accounts = list
                for (var i = 0; i < list.length; i++)       // start on whoever logged in last
                    if (list[i].name === userModel.lastUser) root.current = i
            }
        }
    }
    function customIcon(icon) {
        // SDDM falls back to its own generic face; treat that as "no picture" and show the Devium logo
        var s = icon ? String(icon) : ""
        return (s.length === 0 || s.indexOf("/sddm/faces/") >= 0) ? "" : s
    }

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

            // avatar: the user's own picture in a circle, or the Devium logo
            Item {
                width: 92; height: 92
                anchors.horizontalCenter: parent.horizontalCenter
                Rectangle {
                    anchors.fill: parent; radius: width / 2
                    visible: photo.status !== Image.Ready
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
                // The user's own picture (KDE System Settings > Users), drawn as a circle with a 2D canvas:
                // works everywhere, even without 3D acceleration (unlike shader effects)
                Image { id: photo; source: root.avatarUrl; visible: false }      // only to know if it loads
                Canvas {
                    id: photoCanvas
                    anchors.fill: parent
                    visible: photo.status === Image.Ready
                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.reset()
                        if (!isImageLoaded(root.avatarUrl)) return
                        ctx.save()
                        ctx.beginPath()
                        ctx.arc(width / 2, height / 2, width / 2, 0, 2 * Math.PI)
                        ctx.closePath()
                        ctx.clip()
                        // crop to a centred square, like a profile picture
                        var w = photo.implicitWidth, h = photo.implicitHeight, side = Math.min(w, h)
                        ctx.drawImage(root.avatarUrl, (w - side) / 2, (h - side) / 2, side, side, 0, 0, width, height)
                        ctx.restore()
                    }
                    onImageLoaded: requestPaint()
                    Connections {
                        target: root
                        function onAvatarUrlChanged() { if (root.avatarUrl) photoCanvas.loadImage(root.avatarUrl) }
                    }
                    Connections { target: photo; function onStatusChanged() { photoCanvas.requestPaint() } }
                    Component.onCompleted: if (root.avatarUrl) loadImage(root.avatarUrl)
                }
                Rectangle {   // thin accent ring around the picture
                    anchors.fill: parent; radius: width / 2
                    color: "transparent"; border.color: root.accent; border.width: 2
                    visible: photo.status === Image.Ready
                }
            }

            // the account name: shown, not typed
            Item {
                width: parent.width
                height: 40
                Text {
                    anchors.centerIn: parent
                    text: root.displayName
                    color: root.ink
                    font.family: "Noto Sans"; font.pixelSize: 22; font.weight: Font.DemiBold
                    elide: Text.ElideRight
                    width: Math.min(implicitWidth, parent.width - 90)
                    horizontalAlignment: Text.AlignHCenter
                }
                Repeater {   // ‹ › only when there's more than one account
                    model: root.accounts.length > 1 ? [-1, 1] : []
                    delegate: Rectangle {
                        width: 32; height: 32; radius: 16
                        y: 4
                        x: modelData < 0 ? 0 : parent.width - width
                        color: arrowArea.containsMouse ? "#33ffffff" : "#1affffff"
                        Text { anchors.centerIn: parent; text: modelData < 0 ? "‹" : "›"; color: root.ink; font.pixelSize: 22 }
                        MouseArea {
                            id: arrowArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                root.current = (root.current + modelData + root.accounts.length) % root.accounts.length
                                message.text = ""; passwordField.text = ""; passwordField.forceActiveFocus()
                            }
                        }
                    }
                }
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

            Rectangle {
                id: guestButton
                visible: root.hasGuest
                width: parent.width; height: 40; radius: 14
                color: guestArea.containsMouse ? "#33ffffff" : "#1affffff"
                border.color: "#22ffffff"; border.width: 1
                Text {
                    anchors.centerIn: parent
                    text: "Use as Guest  ·  nothing is kept"
                    color: root.soft; font.family: "Noto Sans"; font.pixelSize: 15
                }
                MouseArea {
                    id: guestArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                    onClicked: { message.text = ""; sddm.login("guest", "", root.sessionIndex) }
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

    // ---- bottom right: restart / shut down (no desktop picker: Devium always starts its own desktop)
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
        sddm.login(root.currentUser, passwordField.text, root.sessionIndex)
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

    Component.onCompleted: passwordField.forceActiveFocus()
}
