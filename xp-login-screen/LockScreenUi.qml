import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.kscreenlocker as ScreenLocker
import org.kde.plasma.private.sessions

Item {
    id: lockScreenUi

    property bool selectedTile: true
    property bool showHintBalloon: false
    property string balloonTitle: "Password Hint:"
    property string balloonText: "Voer je Bazzite gebruikerswachtwoord in en druk op Enter."
    property bool welcomeMode: false
    property bool pendingSubmit: false

    readonly property string displayUserName: (typeof kscreenlocker_userName !== "undefined" && kscreenlocker_userName !== "")
        ? kscreenlocker_userName
        : "King Geoffrey"

    readonly property string displayUserAvatar: Qt.resolvedUrl("images/xp-avatar.png")

    SessionManagement {
        id: sessionManagement
    }

    function submitPassword() {
        showHintBalloon = false
        pendingSubmit = true
        authenticator.startAuthenticating()
        authenticator.respond(pwdInput.text)
    }

    Connections {
        target: authenticator

        function onFailed(kind) {
            if (kind !== 0) return
            pendingSubmit = false
            pwdInput.text = ""
            balloonTitle = "Did you forget your password?"
            balloonText = "Please type your password again.\nBe sure to use the correct uppercase and lowercase letters."
            showHintBalloon = true
            authenticator.startAuthenticating()
            pwdInput.forceActiveFocus()
        }

        function onSucceeded() {
            pendingSubmit = false
            welcomeMode = true
            unlockTimer.start()
        }

        function onPromptForSecretChanged(msg) {
            if (pendingSubmit) {
                pendingSubmit = false
                authenticator.respond(pwdInput.text)
            } else if (selectedTile) {
                pwdInput.forceActiveFocus()
            }
        }
    }

    Timer {
        id: unlockTimer
        interval: 650
        repeat: false
        onTriggered: Qt.quit()
    }

    Component.onCompleted: {
        if (Window.window) {
            Window.window.requestActivate()
        }
        authenticator.startAuthenticating()
        pwdInput.forceActiveFocus()
    }

    // === HOOFDCANVAS (Middenblauw #5a7edc met linksboven radiale gloed) ===
    Rectangle {
        anchors.fill: parent
        color: "#5a7edc"

        // Radiale lichte gloed linksboven (exact zoals origineel Windows XP)
        Image {
            x: -parent.width * 0.08
            y: topBar.height - parent.height * 0.14
            width: Math.round(parent.width * 0.56)
            height: Math.round(parent.width * 0.56)
            source: Qt.resolvedUrl("images/xp-radial-glow.svg")
            smooth: true
        }

        // Klik op de blauwe achtergrond deselecteert de gebruikerstegel (zoals in screenshot 2!)
        MouseArea {
            anchors.fill: parent
            onClicked: {
                lockScreenUi.showHintBalloon = false
                powerPopup.visible = false
                lockScreenUi.selectedTile = false
                bgKeyCatcher.forceActiveFocus()
            }
        }
    }

    // Vang toetsaanslagen op wanneer de tegel niet geselecteerd is zodat direct typen de tegel opent
    Item {
        id: bgKeyCatcher
        focus: !lockScreenUi.selectedTile
        Keys.onPressed: event => {
            if (!lockScreenUi.selectedTile && !lockScreenUi.welcomeMode) {
                lockScreenUi.selectedTile = true
                pwdInput.forceActiveFocus()
            }
        }
    }

    // === BOVENBALK (Donkerblauw #00309c met witte glanslijn onderaan) ===
    Rectangle {
        id: topBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: Math.max(76, Math.round(parent.height * 0.118))
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#002b8f" }
            GradientStop { position: 1.0; color: "#003399" }
        }

        // Witte horizontale glanslijn onderaan de bovenbalk
        Rectangle {
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 2
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.00; color: "#1c49b5" }
                GradientStop { position: 0.15; color: "#9ec2ff" }
                GradientStop { position: 0.36; color: "#ffffff" }
                GradientStop { position: 0.65; color: "#8cb3f5" }
                GradientStop { position: 1.00; color: "#2d5bc4" }
            }
        }
    }

    // === ONDERBALK (Donkerblauw met iconische oranje glanslijn bovenaan) ===
    Rectangle {
        id: bottomBar
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: Math.max(72, Math.round(parent.height * 0.112))
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "#283894" }
            GradientStop { position: 0.4; color: "#143091" }
            GradientStop { position: 1.0; color: "#002987" }
        }

        // Iconische oranje gloedlijn bovenaan de onderbalk
        Rectangle {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 2
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.00; color: "#283894" }
                GradientStop { position: 0.14; color: "#9c5636" }
                GradientStop { position: 0.36; color: "#ff9933" }
                GradientStop { position: 0.56; color: "#e87e25" }
                GradientStop { position: 0.84; color: "#3d4c9c" }
                GradientStop { position: 1.00; color: "#002987" }
            }
        }

        // Linksonder: Rode 3D "Turn off computer" knop + tekst
        Row {
            id: turnOffRow
            visible: !lockScreenUi.welcomeMode
            anchors.left: parent.left
            anchors.leftMargin: 32
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10

            Image {
                width: 28
                height: 28
                anchors.verticalCenter: parent.verticalCenter
                source: Qt.resolvedUrl("images/btn-power.svg")
                sourceSize.width: 56
                sourceSize.height: 56
                smooth: true
                scale: powerMouse.pressed ? 0.94 : 1.0

                MouseArea {
                    id: powerMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: powerPopup.visible = !powerPopup.visible
                }
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: "Turn off computer"
                color: powerTextMouse.containsMouse ? "#ffffcc" : "#ffffff"
                font.family: "Tahoma, 'Noto Sans', sans-serif"
                font.pixelSize: 15
                font.bold: false
                font.underline: powerTextMouse.containsMouse

                MouseArea {
                    id: powerTextMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: powerPopup.visible = !powerPopup.visible
                }
            }
        }

        // Rechtsonder: Twee regels XP uitlegtekst
        Column {
            visible: !lockScreenUi.welcomeMode
            anchors.right: parent.right
            anchors.rightMargin: 32
            anchors.verticalCenter: parent.verticalCenter
            spacing: 2

            Text {
                anchors.right: parent.right
                text: "After you log on, you can add or change accounts."
                color: "#dce8ff"
                font.family: "Tahoma, 'Noto Sans', sans-serif"
                font.pixelSize: 12
            }
            Text {
                anchors.right: parent.right
                text: "Just go to your Control Panel and click User Accounts."
                color: "#dce8ff"
                font.family: "Tahoma, 'Noto Sans', sans-serif"
                font.pixelSize: 12
            }
        }
    }

    // === HOOFDSCHERM INHOUD (Tijdens aanmelden / vergrendeling) ===
    Item {
        id: loginContent
        visible: !lockScreenUi.welcomeMode
        anchors.top: topBar.bottom
        anchors.bottom: bottomBar.top
        anchors.left: parent.left
        anchors.right: parent.right

        // Centrale verticale scheidingslijn (1px lichtblauwe vervagende lijn)
        Rectangle {
            id: centerDivider
            x: Math.round(parent.width * 0.49)
            y: Math.round(parent.height * 0.08)
            width: 1
            height: Math.round(parent.height * 0.84)
            gradient: Gradient {
                GradientStop { position: 0.00; color: "transparent" }
                GradientStop { position: 0.20; color: "#8cb0f2" }
                GradientStop { position: 0.50; color: "#c2daff" }
                GradientStop { position: 0.80; color: "#8cb0f2" }
                GradientStop { position: 1.00; color: "transparent" }
            }
        }

        // === LINKERHELFT: Microsoft Windows XP Logo + "To begin, click your user name" ===
        Column {
            anchors.right: centerDivider.left
            anchors.rightMargin: 42
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -18
            spacing: 20

            Image {
                anchors.right: parent.right
                width: 245
                height: 127
                source: Qt.resolvedUrl("images/xp-login-logo.svg")
                sourceSize.width: 490
                sourceSize.height: 254
                smooth: true
            }

            Text {
                anchors.right: parent.right
                text: "To begin, click your user name"
                color: "#ffffff"
                font.family: "Tahoma, 'Noto Sans', sans-serif"
                font.pixelSize: 19
                style: Text.Raised
                styleColor: "#3052a6"
            }
        }

        // === RECHTERHELFT: Gebruikerstegel(s) met Avatar + Wachtwoordveld ===
        Column {
            id: usersColumn
            anchors.left: centerDivider.right
            anchors.leftMargin: 36
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -10
            spacing: 18

            // Gebruikerstegel 1 (Hoofdgebruiker)
            Item {
                id: userTileBox
                width: 410
                height: lockScreenUi.selectedTile ? 92 : 74

                // Donkerblauwe XP selectie-achtergrond (vervaagt rechts naar transparant #5a7edc!)
                Rectangle {
                    id: selectedBg
                    anchors.fill: parent
                    radius: 6
                    visible: lockScreenUi.selectedTile
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.00; color: "#1140aa" }
                        GradientStop { position: 0.52; color: "#2153bf" }
                        GradientStop { position: 0.88; color: "#4b72d4" }
                        GradientStop { position: 1.00; color: "#5a7edc" }
                    }
                }

                // Witte/lichtblauwe rand boven, links en onder de geselecteerde gebruikerstegel
                Rectangle {
                    visible: lockScreenUi.selectedTile
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 4
                    height: 1
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "#a8c6ff" }
                        GradientStop { position: 0.7; color: "#7da3eb" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
                Rectangle {
                    visible: lockScreenUi.selectedTile
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 4
                    height: 1
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "#a8c6ff" }
                        GradientStop { position: 0.7; color: "#7da3eb" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
                Rectangle {
                    visible: lockScreenUi.selectedTile
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.topMargin: 3
                    anchors.bottomMargin: 3
                    width: 1
                    color: "#a8c6ff"
                }

                // Klik op de tegel om hem te selecteren
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        lockScreenUi.selectedTile = true
                        pwdInput.forceActiveFocus()
                    }
                }

                // Vierkante Gebruikersavatar met gele/gouden rand (indien geselecteerd) of witte rand
                Rectangle {
                    id: avatarBorder
                    x: 12
                    y: 10
                    width: 58
                    height: 58
                    radius: 4
                    color: "#1b439c"
                    border.width: 2
                    border.color: lockScreenUi.selectedTile
                        ? "#ffcc00"
                        : (tileHover.containsMouse ? "#ffe680" : "#e6f0ff")

                    Image {
                        anchors.fill: parent
                        anchors.margins: 2
                        source: lockScreenUi.displayUserAvatar
                        fillMode: Image.PreserveAspectCrop
                        smooth: true
                    }

                    MouseArea {
                        id: tileHover
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            lockScreenUi.selectedTile = true
                            pwdInput.forceActiveFocus()
                        }
                    }
                }

                // Gebruikersnaam + Status (of Wachtwoordveld als geselecteerd)
                Column {
                    anchors.left: avatarBorder.right
                    anchors.leftMargin: 14
                    anchors.top: avatarBorder.top
                    anchors.topMargin: -2
                    spacing: 3

                    Text {
                        text: lockScreenUi.displayUserName
                        color: "#ffffff"
                        font.family: "Tahoma, 'Noto Sans', sans-serif"
                        font.pixelSize: 18
                        font.bold: lockScreenUi.selectedTile
                        style: Text.Raised
                        styleColor: "#0d2e7a"
                    }

                    // Status wanneer NIET geselecteerd (zoals in screenshot 2: "4 programs running.")
                    Text {
                        visible: !lockScreenUi.selectedTile
                        text: "Logged on"
                        color: "#001f66"
                        font.family: "Tahoma, 'Noto Sans', sans-serif"
                        font.pixelSize: 12
                        font.bold: true
                    }

                    // Wachtwoord-sectie wanneer WEL geselecteerd (zoals in screenshot 1!)
                    Column {
                        visible: lockScreenUi.selectedTile
                        spacing: 3

                        Text {
                            text: "Type your password"
                            color: "#ffffff"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 11
                        }

                        Row {
                            spacing: 6

                            // Wit Windows XP wachtwoordveld
                            Rectangle {
                                width: 184
                                height: 25
                                radius: 2
                                color: "#ffffff"
                                border.color: "#10377d"
                                border.width: 1

                                TextInput {
                                    id: pwdInput
                                    anchors.fill: parent
                                    anchors.leftMargin: 6
                                    anchors.rightMargin: 6
                                    verticalAlignment: TextInput.AlignVCenter
                                    echoMode: TextInput.Password
                                    passwordCharacter: "●"
                                    color: "#000000"
                                    font.family: "Tahoma, 'Noto Sans', sans-serif"
                                    font.pixelSize: 13
                                    selectByMouse: true
                                    selectionColor: "#316ac5"
                                    selectedTextColor: "#ffffff"
                                    clip: true
                                    focus: true

                                    onAccepted: lockScreenUi.submitPassword()
                                    onTextChanged: {
                                        if (text.length > 0) {
                                            lockScreenUi.showHintBalloon = false
                                        }
                                    }
                                    Keys.onEscapePressed: {
                                        lockScreenUi.showHintBalloon = false
                                        lockScreenUi.selectedTile = false
                                    }
                                }
                            }

                            // Groene 3D Pijl-knop [ -> ]
                            Image {
                                width: 25
                                height: 25
                                source: Qt.resolvedUrl("images/btn-go.svg")
                                sourceSize.width: 50
                                sourceSize.height: 50
                                smooth: true
                                scale: goBtnMouse.pressed ? 0.92 : 1.0

                                MouseArea {
                                    id: goBtnMouse
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: lockScreenUi.submitPassword()
                                }
                            }

                            // Blauwe 3D Vraagteken-knop [ ? ]
                            Image {
                                id: helpBtnImg
                                width: 25
                                height: 25
                                source: Qt.resolvedUrl("images/btn-help.svg")
                                sourceSize.width: 50
                                sourceSize.height: 50
                                smooth: true
                                scale: helpBtnMouse.pressed ? 0.92 : 1.0

                                MouseArea {
                                    id: helpBtnMouse
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        lockScreenUi.balloonTitle = "Password Hint:"
                                        lockScreenUi.balloonText = "Voer je Bazzite gebruikerswachtwoord in en klik op het groene pijltje."
                                        lockScreenUi.showHintBalloon = !lockScreenUi.showHintBalloon
                                        pwdInput.forceActiveFocus()
                                    }
                                }
                            }
                        }
                    }
                }

                // Authentieke Windows XP gele ballon-tooltip onder het wachtwoordveld / ?-icoon
                Rectangle {
                    id: hintBalloon
                    visible: lockScreenUi.showHintBalloon && lockScreenUi.selectedTile
                    x: 84
                    y: 96
                    width: 280
                    height: balloonCol.implicitHeight + 16
                    radius: 6
                    color: "#ffffe1"
                    border.color: "#000000"
                    border.width: 1
                    z: 50

                    Column {
                        id: balloonCol
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 4

                        Text {
                            text: lockScreenUi.balloonTitle
                            color: "#000000"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 11
                            font.bold: true
                        }
                        Text {
                            width: parent.width
                            text: lockScreenUi.balloonText
                            color: "#000000"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }
        }
    }

    // === "welcome" SCHERM BIJ AANMELDEN / ONTGRENDELEN (Exact zoals screenshot 3!) ===
    Item {
        id: welcomeOverlay
        visible: lockScreenUi.welcomeMode
        anchors.top: topBar.bottom
        anchors.bottom: bottomBar.top
        anchors.left: parent.left
        anchors.right: parent.right

        // Schaduwtekst
        Text {
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: 43
            anchors.verticalCenterOffset: -3
            text: "welcome"
            color: "#2b4ea2"
            font.family: "Arial, Tahoma, 'Noto Sans', sans-serif"
            font.pixelSize: 48
            font.bold: true
            font.italic: true
        }

        // Voorgrondtekst
        Text {
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: 40
            anchors.verticalCenterOffset: -6
            text: "welcome"
            color: "#ffffff"
            font.family: "Arial, Tahoma, 'Noto Sans', sans-serif"
            font.pixelSize: 48
            font.bold: true
            font.italic: true
        }
    }

    // === KLEIN XP MENU VOOR "Turn off computer" LINKSONDER ===
    Rectangle {
        id: powerPopup
        visible: false
        anchors.left: parent.left
        anchors.leftMargin: 32
        anchors.bottom: bottomBar.top
        anchors.bottomMargin: 6
        width: 190
        height: pwrCol.implicitHeight + 8
        radius: 3
        color: "#ffffff"
        border.color: "#00309c"
        border.width: 1
        z: 100

        Column {
            id: pwrCol
            anchors.fill: parent
            anchors.margins: 4
            spacing: 2

            Rectangle {
                width: parent.width; height: 26; radius: 2
                color: p1Mouse.containsMouse ? "#316ac5" : "transparent"
                Text {
                    anchors.verticalCenter: parent.verticalCenter; x: 8
                    text: "Stand By (Slaapstand)"
                    color: p1Mouse.containsMouse ? "white" : "black"
                    font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                }
                MouseArea {
                    id: p1Mouse; anchors.fill: parent; hoverEnabled: true
                    onClicked: { powerPopup.visible = false; sessionManagement.suspend() }
                }
            }
            Rectangle {
                width: parent.width; height: 26; radius: 2
                color: p2Mouse.containsMouse ? "#316ac5" : "transparent"
                Text {
                    anchors.verticalCenter: parent.verticalCenter; x: 8
                    text: "Turn Off (Uitschakelen)"
                    color: p2Mouse.containsMouse ? "white" : "black"
                    font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                }
                MouseArea {
                    id: p2Mouse; anchors.fill: parent; hoverEnabled: true
                    onClicked: { powerPopup.visible = false; sessionManagement.requestShutdown() }
                }
            }
            Rectangle {
                width: parent.width; height: 26; radius: 2
                color: p3Mouse.containsMouse ? "#316ac5" : "transparent"
                Text {
                    anchors.verticalCenter: parent.verticalCenter; x: 8
                    text: "Restart (Opnieuw opstarten)"
                    color: p3Mouse.containsMouse ? "white" : "black"
                    font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                }
                MouseArea {
                    id: p3Mouse; anchors.fill: parent; hoverEnabled: true
                    onClicked: { powerPopup.visible = false; sessionManagement.requestReboot() }
                }
            }
        }
    }
}
