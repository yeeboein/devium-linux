// Devium login screen for SDDM (Qt 6). Plain QtQuick with no shaders, so it works without Plasma and without
// 3D acceleration (KDE Plasma and Hyprland editions).
//
// It starts like a phone's lock screen: a big clock. Press any key, click or move the mouse and the sign-in card
// slides up. Typing straight away works too (the key goes into the password box). Spaces typed before the first
// character are ignored, so pressing Space to wake the screen doesn't end up in the password.
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
    readonly property color dim: "#8a96a4"
    property int sessionIndex: (sessionModel && sessionModel.lastIndex >= 0) ? sessionModel.lastIndex : 0
    readonly property string avatarUrl: avatar === "" ? "" : (avatar.indexOf("/") === 0 ? "file://" + avatar : avatar)

    // awake: the sign-in card is showing. busy: checking the password.
    property bool awake: false
    property bool busy: false
    property bool started: false

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
    function greeting() {
        var h = new Date().getHours()
        return h < 5 ? "Good night" : h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening"
    }
    function wake() {
        awake = true
        idle.restart()
        passwordField.forceActiveFocus()
    }

    // ---- the mountains: slightly darker, and a little more once the card is up so it reads well
    Image {
        id: bg
        anchors.fill: parent
        source: config.background || "background.jpg"
        fillMode: Image.PreserveAspectCrop
        smooth: true
        asynchronous: true
        scale: root.awake ? 1.04 : 1.0
        Behavior on scale { NumberAnimation { duration: 900; easing.type: Easing.OutCubic } }
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#38141a22" }
            GradientStop { position: 0.55; color: "#20141a22" }
            GradientStop { position: 1.0; color: "#b0141a22" }
        }
    }
    Rectangle {
        anchors.fill: parent
        color: "#141a22"
        opacity: root.awake ? 0.35 : 0.0
        Behavior on opacity { NumberAnimation { duration: 500; easing.type: Easing.OutCubic } }
    }

    // anything on the background wakes the screen
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        property point last: Qt.point(-1, -1)
        onPositionChanged: function (mouse) {
            // ignore the tiny "moves" some touchpads send on their own
            if (last.x >= 0 && (Math.abs(mouse.x - last.x) > 6 || Math.abs(mouse.y - last.y) > 6)) root.wake()
            last = Qt.point(mouse.x, mouse.y)
        }
        onClicked: root.wake()
    }

    // ---- Devium logo, top left
    Row {
        anchors { left: parent.left; top: parent.top; margins: 36 }
        spacing: 14
        opacity: root.started ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: 800 } }
        Image { source: "logo-white.png"; width: 40; height: 40; fillMode: Image.PreserveAspectFit; smooth: true }
        Text {
            text: "Devium"
            color: root.ink
            font.family: "Noto Sans"; font.pixelSize: 24; font.weight: Font.DemiBold
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    // ---- big clock: in the middle while resting, moves up when the card appears
    Column {
        id: clock
        anchors.horizontalCenter: parent.horizontalCenter
        y: root.awake ? parent.height * 0.12 : parent.height * 0.30
        scale: root.awake ? 0.78 : 1.0
        opacity: root.started ? 1 : 0
        spacing: 0
        Behavior on y { NumberAnimation { duration: 550; easing.type: Easing.OutCubic } }
        Behavior on scale { NumberAnimation { duration: 550; easing.type: Easing.OutCubic } }
        Behavior on opacity { NumberAnimation { duration: 900 } }
        Text {
            id: timeText
            anchors.horizontalCenter: parent.horizontalCenter
            color: root.ink
            font.family: "Noto Sans"; font.pixelSize: 144; font.weight: Font.Bold
            style: Text.Raised; styleColor: "#40000000"
        }
        Text {
            id: dateText
            anchors.horizontalCenter: parent.horizontalCenter
            color: root.soft
            font.family: "Noto Sans"; font.pixelSize: 28
            style: Text.Raised; styleColor: "#30000000"
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

    // ---- "press any key" hint while resting, on a soft dark pill so it reads over snow and fog
    Rectangle {
        id: hint
        property real pulse: 1.0
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height * 0.80
        width: hintText.implicitWidth + 40; height: 40; radius: 20
        color: "#b0222830"
        border.color: "#30ffffff"; border.width: 1
        opacity: root.awake ? 0 : pulse
        Text {
            id: hintText
            anchors.centerIn: parent
            text: "Press any key or click to sign in"
            color: root.ink
            font.family: "Noto Sans"; font.pixelSize: 16
        }
        SequentialAnimation {
            running: !root.awake; loops: Animation.Infinite
            NumberAnimation { target: hint; property: "pulse"; to: 0.75; duration: 1500; easing.type: Easing.InOutSine }
            NumberAnimation { target: hint; property: "pulse"; to: 1.0; duration: 1500; easing.type: Easing.InOutSine }
        }
    }

    // ---- the sign-in card (with a soft shadow made of a few faint layers, no shaders)
    Item {
        id: cardBox
        width: 420
        height: card.height
        anchors.horizontalCenter: parent.horizontalCenter
        y: root.awake ? parent.height * 0.40 : parent.height * 0.46
        opacity: root.awake ? 1 : 0
        visible: opacity > 0.01
        Behavior on y { NumberAnimation { duration: 500; easing.type: Easing.OutCubic } }
        Behavior on opacity { NumberAnimation { duration: 400; easing.type: Easing.OutCubic } }

        Repeater {
            model: 4
            Rectangle {
                x: -index * 3; y: 8 + index * 3
                width: cardBox.width + index * 6; height: card.height + index * 6
                radius: 28 + index * 3
                color: "#000000"; opacity: 0.07
            }
        }
        Rectangle {
            id: card
            width: parent.width
            height: col.implicitHeight + 56
            radius: 28
            color: "#c4222830"
            border.color: "#30ffffff"
            border.width: 1
            Rectangle {   // a faint highlight along the top edge
                anchors { left: parent.left; right: parent.right; top: parent.top; margins: 1 }
                height: parent.height / 2; radius: 27
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#14ffffff" }
                    GradientStop { position: 1.0; color: "#00ffffff" }
                }
            }

            Column {
                id: col
                anchors { left: parent.left; right: parent.right; top: parent.top; margins: 28 }
                spacing: 12

                // avatar: the user's own picture in a circle, or the Devium logo
                Item {
                    width: 96; height: 96
                    anchors.horizontalCenter: parent.horizontalCenter
                    Rectangle {   // soft glow ring
                        anchors.centerIn: parent
                        width: parent.width + 14; height: width; radius: width / 2
                        color: "transparent"; border.color: root.accent; border.width: 2; opacity: 0.35
                    }
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
                            source: "logo-white.png"; width: 56; height: 56
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
                }

                // greeting and the account name: shown, not typed
                Item {
                    width: parent.width
                    height: 58
                    Column {
                        anchors.centerIn: parent
                        spacing: 2
                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: root.greeting() + ","
                            color: root.dim
                            font.family: "Noto Sans"; font.pixelSize: 15
                        }
                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: root.displayName
                            color: root.ink
                            font.family: "Noto Sans"; font.pixelSize: 23; font.weight: Font.DemiBold
                            elide: Text.ElideRight
                            width: Math.min(implicitWidth, col.width - 90)
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                    Repeater {   // ‹ › only when there's more than one account
                        model: root.accounts.length > 1 ? [-1, 1] : []
                        delegate: Rectangle {
                            width: 34; height: 34; radius: 17
                            y: 12
                            x: modelData < 0 ? 0 : parent.width - width
                            color: arrowArea.containsMouse ? "#33ffffff" : "#16ffffff"
                            Behavior on color { ColorAnimation { duration: 120 } }
                            Text { anchors.centerIn: parent; text: modelData < 0 ? "‹" : "›"; color: root.ink; font.pixelSize: 22 }
                            MouseArea {
                                id: arrowArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    root.current = (root.current + modelData + root.accounts.length) % root.accounts.length
                                    message.text = ""; passwordField.text = ""; root.wake()
                                }
                            }
                        }
                    }
                }

                Item {
                    width: parent.width
                    height: 52
                    TextField {
                        id: passwordField
                        anchors { left: parent.left; right: goButton.left; rightMargin: 10 }
                        height: 52
                        echoMode: showPw.checked ? TextInput.Normal : TextInput.Password
                        passwordCharacter: "●"
                        placeholderText: "Password"
                        color: root.ink
                        placeholderTextColor: root.dim
                        selectionColor: root.accent
                        font.family: "Noto Sans"; font.pixelSize: 18
                        leftPadding: 18; rightPadding: 54
                        enabled: !root.busy
                        background: Rectangle {
                            radius: 15
                            color: passwordField.activeFocus ? "#40ffffff" : "#2affffff"
                            border.color: passwordField.activeFocus ? root.accent : "#22ffffff"
                            border.width: passwordField.activeFocus ? 2 : 1
                            Behavior on color { ColorAnimation { duration: 150 } }
                        }
                        focus: true
                        onAccepted: root.doLogin()
                        onTextChanged: idle.restart()
                        Keys.onPressed: function (event) {
                            if (!root.awake) root.wake()
                            idle.restart()
                            // Space before the first character only wakes the screen; it isn't part of the password.
                            // Spaces after the first character are typed as normal (passwords may contain spaces).
                            if (event.key === Qt.Key_Space && passwordField.text.length === 0) {
                                event.accepted = true
                                return
                            }
                            // Enter on an empty, still-hidden box just wakes the screen
                            if ((event.key === Qt.Key_Return || event.key === Qt.Key_Enter) && passwordField.text.length === 0) {
                                event.accepted = true
                                return
                            }
                            if (event.key === Qt.Key_Escape) {
                                passwordField.text = ""
                                event.accepted = true
                            }
                        }

                        // show / hide the password
                        AbstractButton {
                            id: showPw
                            checkable: true
                            width: 38; height: 38
                            anchors { right: parent.right; rightMargin: 8; verticalCenter: parent.verticalCenter }
                            visible: passwordField.text.length > 0
                            focusPolicy: Qt.NoFocus
                            background: Rectangle { radius: 10; color: showPw.hovered ? "#22ffffff" : "transparent" }
                            contentItem: Canvas {
                                id: eye
                                property bool open: showPw.checked
                                onOpenChanged: requestPaint()
                                onPaint: {
                                    var c = getContext("2d"); c.reset()
                                    var w = width, h = height
                                    c.strokeStyle = root.soft; c.fillStyle = root.soft; c.lineWidth = 1.8
                                    c.beginPath()
                                    c.moveTo(w * 0.15, h * 0.5)
                                    c.quadraticCurveTo(w * 0.5, h * 0.12, w * 0.85, h * 0.5)
                                    c.quadraticCurveTo(w * 0.5, h * 0.88, w * 0.15, h * 0.5)
                                    c.stroke()
                                    c.beginPath(); c.arc(w * 0.5, h * 0.5, w * 0.11, 0, 2 * Math.PI); c.fill()
                                    if (!open) {   // a line through it = hidden
                                        c.beginPath(); c.moveTo(w * 0.22, h * 0.8); c.lineTo(w * 0.78, h * 0.2); c.stroke()
                                    }
                                }
                            }
                            onToggled: passwordField.forceActiveFocus()
                        }
                    }
                    Rectangle {
                        id: goButton
                        width: 52; height: 52; radius: 15
                        anchors.right: parent.right
                        opacity: passwordField.text.length > 0 || root.busy ? 1 : 0.55
                        Behavior on opacity { NumberAnimation { duration: 150 } }
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0.0; color: goArea.containsMouse ? Qt.lighter(root.accent, 1.1) : root.accent }
                            GradientStop { position: 1.0; color: goArea.containsMouse ? Qt.lighter(root.accent2, 1.1) : root.accent2 }
                        }
                        Canvas {   // arrow
                            anchors.centerIn: parent; width: 24; height: 24
                            visible: !root.busy
                            onPaint: {
                                var c = getContext("2d"); c.reset()
                                c.strokeStyle = "#1b2026"; c.lineWidth = 2.6; c.lineCap = "round"; c.lineJoin = "round"
                                c.beginPath(); c.moveTo(4, 12); c.lineTo(20, 12); c.moveTo(13, 5); c.lineTo(20, 12); c.lineTo(13, 19)
                                c.stroke()
                            }
                        }
                        Canvas {   // spinner while the password is checked
                            id: spinner
                            anchors.centerIn: parent; width: 26; height: 26
                            visible: root.busy
                            onPaint: {
                                var c = getContext("2d"); c.reset()
                                c.strokeStyle = "#1b2026"; c.lineWidth = 3; c.lineCap = "round"
                                c.beginPath(); c.arc(13, 13, 10, 0, Math.PI * 1.4); c.stroke()
                            }
                            RotationAnimation on rotation { running: root.busy; from: 0; to: 360; duration: 900; loops: Animation.Infinite }
                        }
                        MouseArea { id: goArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: root.doLogin() }
                    }
                }

                // Caps Lock warning
                Row {
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing: 6
                    visible: typeof keyboard !== "undefined" && keyboard && keyboard.capsLock
                    Rectangle {
                        width: 18; height: 18; radius: 5; color: "#e8c98f"
                        anchors.verticalCenter: parent.verticalCenter
                        Text { anchors.centerIn: parent; text: "⇪"; color: "#1b2026"; font.pixelSize: 12; font.bold: true }
                    }
                    Text { text: "Caps Lock is on"; color: "#e8c98f"; font.family: "Noto Sans"; font.pixelSize: 14 }
                }

                Text {
                    id: message
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    color: "#f0b2b5"
                    font.family: "Noto Sans"; font.pixelSize: 15
                    text: ""
                    visible: text.length > 0
                }

                Rectangle {
                    id: guestButton
                    visible: root.hasGuest
                    width: parent.width; height: 42; radius: 14
                    color: guestArea.containsMouse ? "#2effffff" : "#14ffffff"
                    border.color: "#22ffffff"; border.width: 1
                    Behavior on color { ColorAnimation { duration: 120 } }
                    Text {
                        anchors.centerIn: parent
                        text: "Use as Guest  ·  nothing is kept"
                        color: root.soft; font.family: "Noto Sans"; font.pixelSize: 15
                    }
                    MouseArea {
                        id: guestArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: { message.text = ""; root.busy = true; sddm.login("guest", "", root.sessionIndex) }
                    }
                }
            }
        }
    }

    // ---- bottom right: sleep / restart / shut down (no desktop picker: Devium always starts its own desktop)
    Row {
        anchors { right: parent.right; bottom: parent.bottom; margins: 30 }
        spacing: 12
        opacity: root.started ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: 800 } }
        Repeater {
            model: [
                { label: "Sleep", act: "suspend", ok: sddm.canSuspend },
                { label: "Restart", act: "reboot", ok: sddm.canReboot },
                { label: "Shut down", act: "poweroff", ok: sddm.canPowerOff }
            ]
            delegate: Rectangle {
                visible: modelData.ok
                width: powerRow.implicitWidth + 30; height: 42; radius: 13
                color: btnArea.containsMouse ? "#a0242a32" : "#66242a32"
                border.color: btnArea.containsMouse ? "#55ffffff" : "#30ffffff"; border.width: 1
                Behavior on color { ColorAnimation { duration: 120 } }
                Row {
                    id: powerRow
                    anchors.centerIn: parent
                    spacing: 8
                    Canvas {
                        width: 18; height: 18
                        anchors.verticalCenter: parent.verticalCenter
                        property string kind: modelData.act
                        onPaint: {
                            var c = getContext("2d"); c.reset()
                            c.strokeStyle = root.ink; c.fillStyle = root.ink; c.lineWidth = 1.8; c.lineCap = "round"
                            if (kind === "poweroff") {
                                c.beginPath(); c.arc(9, 10, 6.5, -Math.PI * 0.32, Math.PI * 1.32); c.stroke()
                                c.beginPath(); c.moveTo(9, 2); c.lineTo(9, 9); c.stroke()
                            } else if (kind === "reboot") {
                                c.beginPath(); c.arc(9, 9.5, 6.5, -Math.PI * 0.15, Math.PI * 1.5); c.stroke()
                                c.beginPath(); c.moveTo(9, 0.8); c.lineTo(12.5, 3); c.lineTo(9, 5.4); c.closePath(); c.fill()
                            } else {   // moon
                                c.beginPath(); c.arc(9, 9, 7, Math.PI * 0.35, Math.PI * 1.65); c.arc(11.5, 7, 5.5, Math.PI * 1.25, Math.PI * 0.75, true); c.closePath(); c.fill()
                            }
                        }
                    }
                    Text { text: modelData.label; color: root.ink; font.family: "Noto Sans"; font.pixelSize: 15; anchors.verticalCenter: parent.verticalCenter }
                }
                MouseArea {
                    id: btnArea; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                    onClicked: modelData.act === "reboot" ? sddm.reboot() : modelData.act === "poweroff" ? sddm.powerOff() : sddm.suspend()
                }
            }
        }
    }

    // ---- back to the resting clock after a minute without typing (only if nothing was typed)
    Timer {
        id: idle
        interval: 60000
        onTriggered: if (passwordField.text.length === 0 && !root.busy) { root.awake = false; message.text = "" }
    }

    // ---- logging in
    function doLogin() {
        if (root.busy) return
        if (passwordField.text.length === 0) { root.wake(); return }
        message.text = ""
        root.busy = true
        sddm.login(root.currentUser, passwordField.text, root.sessionIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false
            message.text = "That password didn't work. Try again."
            passwordField.text = ""
            root.wake()
            shake.start()
        }
        function onLoginSucceeded() {
            message.text = ""
        }
    }

    SequentialAnimation {
        id: shake
        NumberAnimation { target: cardBox; property: "anchors.horizontalCenterOffset"; to: -14; duration: 50 }
        NumberAnimation { target: cardBox; property: "anchors.horizontalCenterOffset"; to: 14; duration: 70 }
        NumberAnimation { target: cardBox; property: "anchors.horizontalCenterOffset"; to: -8; duration: 60 }
        NumberAnimation { target: cardBox; property: "anchors.horizontalCenterOffset"; to: 0; duration: 50 }
    }

    Component.onCompleted: {
        started = true
        passwordField.forceActiveFocus()
    }
}
