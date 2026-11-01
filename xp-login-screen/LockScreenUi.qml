import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.kscreenlocker as ScreenLocker
import org.kde.plasma.private.sessions
import "xpConfig.js" as XpConfig

Item {
    id: lockScreenUi

    property bool classicLogon: (XpConfig.logonStyle === "classic")
    property bool classicShowOptions: false
    property bool selectedTile: true
    property bool showHintBalloon: false
    property string balloonTitle: "Password Hint:"
    property string balloonText: "Type your user password and press Enter."
    property bool welcomeMode: false
    property bool pendingSubmit: false

    readonly property string displayUserName: (typeof kscreenlocker_userName !== "undefined" && kscreenlocker_userName !== "")
        ? kscreenlocker_userName
        : "King Geoffrey"

    readonly property string displayUserAvatar: Qt.resolvedUrl("images/xp-avatar.png")

    SessionManagement {
        id: sessionManagement
    }

    function activePasswordText() {
        return classicLogon ? classicPwdInput.text : pwdInput.text
    }

    function focusActivePassword() {
        if (classicLogon) {
            classicPwdInput.forceActiveFocus()
        } else if (selectedTile) {
            pwdInput.forceActiveFocus()
        }
    }

    function submitPassword() {
        showHintBalloon = false
        pendingSubmit = true
        authenticator.startAuthenticating()
        authenticator.respond(activePasswordText())
    }

    Connections {
        target: authenticator

        function onFailed(kind) {
            if (kind !== 0) return
            pendingSubmit = false
            pwdInput.text = ""
            classicPwdInput.text = ""
            balloonTitle = "Logon Message"
            balloonText = "The system could not log you on. Make sure your User name and domain are correct, then type your password again."
            showHintBalloon = true
            authenticator.startAuthenticating()
            focusActivePassword()
        }

        function onSucceeded() {
            pendingSubmit = false
            welcomeMode = true
            unlockTimer.start()
        }

        function onPromptForSecretChanged(msg) {
            if (pendingSubmit) {
                pendingSubmit = false
                authenticator.respond(activePasswordText())
            } else {
                focusActivePassword()
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
        focusActivePassword()
    }

    // =========================================================================
    // MODUS 1: STANDAARD WINDOWS XP WELKOMSTSCHERM ("welcome" / Gebruikerstegels)
    // =========================================================================
    Item {
        id: welcomeStyleRoot
        anchors.fill: parent
        visible: !lockScreenUi.classicLogon

        // Hoofdcanvas (#5a7edc met linksboven radiale gloed)
        Rectangle {
            anchors.fill: parent
            color: "#5a7edc"

            Image {
                x: -parent.width * 0.08
                y: topBar.height - parent.height * 0.14
                width: Math.round(parent.width * 0.56)
                height: Math.round(parent.width * 0.56)
                source: Qt.resolvedUrl("images/xp-radial-glow.svg")
                smooth: true
            }

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

        Item {
            id: bgKeyCatcher
            focus: !lockScreenUi.classicLogon && !lockScreenUi.selectedTile
            Keys.onPressed: event => {
                if (!lockScreenUi.selectedTile && !lockScreenUi.welcomeMode) {
                    lockScreenUi.selectedTile = true
                    pwdInput.forceActiveFocus()
                }
            }
        }

        // Bovenbalk (#00309c met witte glanslijn onderaan)
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

        // Onderbalk (Donkerblauw met iconische oranje glanslijn bovenaan)
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

            Row {
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

        // Hoofdscherm inhoud
        Item {
            visible: !lockScreenUi.welcomeMode
            anchors.top: topBar.bottom
            anchors.bottom: bottomBar.top
            anchors.left: parent.left
            anchors.right: parent.right

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

            // Linkerhelft: Echte Microsoft Windows XP Logo + "To begin, click your user name"
            Column {
                anchors.right: centerDivider.left
                anchors.rightMargin: 42
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -18
                spacing: 20

                Image {
                    anchors.right: parent.right
                    width: 235
                    height: 142
                    source: Qt.resolvedUrl("images/xp-login-logo.png")
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    mipmap: true
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

            // Rechterhelft: Gebruikerstegel met Avatar + Wachtwoordveld
            Column {
                anchors.left: centerDivider.right
                anchors.leftMargin: 36
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -10
                spacing: 18

                Item {
                    id: userTileBox
                    width: 410
                    height: lockScreenUi.selectedTile ? 92 : 74

                    Rectangle {
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

                    Rectangle {
                        visible: lockScreenUi.selectedTile
                        anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0.0; color: "#a8c6ff" }
                            GradientStop { position: 0.7; color: "#7da3eb" }
                            GradientStop { position: 1.0; color: "transparent" }
                        }
                    }
                    Rectangle {
                        visible: lockScreenUi.selectedTile
                        anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0.0; color: "#a8c6ff" }
                            GradientStop { position: 0.7; color: "#7da3eb" }
                            GradientStop { position: 1.0; color: "transparent" }
                        }
                    }
                    Rectangle {
                        visible: lockScreenUi.selectedTile
                        anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.topMargin: 3; anchors.bottomMargin: 3; width: 1
                        color: "#a8c6ff"
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            lockScreenUi.selectedTile = true
                            pwdInput.forceActiveFocus()
                        }
                    }

                    Rectangle {
                        id: avatarBorder
                        x: 12; y: 10; width: 58; height: 58; radius: 4
                        color: "#1b439c"
                        border.width: 2
                        border.color: lockScreenUi.selectedTile
                            ? "#ffcc00"
                            : (tileHover.containsMouse ? "#ffe680" : "#e6f0ff")

                        Image {
                            anchors.fill: parent; anchors.margins: 2
                            source: lockScreenUi.displayUserAvatar
                            fillMode: Image.PreserveAspectCrop; smooth: true
                        }

                        MouseArea {
                            id: tileHover
                            anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                lockScreenUi.selectedTile = true
                                pwdInput.forceActiveFocus()
                            }
                        }
                    }

                    Column {
                        anchors.left: avatarBorder.right; anchors.leftMargin: 14
                        anchors.top: avatarBorder.top; anchors.topMargin: -2
                        spacing: 3

                        Text {
                            text: lockScreenUi.displayUserName
                            color: "#ffffff"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 18
                            font.bold: lockScreenUi.selectedTile
                            style: Text.Raised; styleColor: "#0d2e7a"
                        }

                        Text {
                            visible: !lockScreenUi.selectedTile
                            text: "Logged on"
                            color: "#001f66"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 12; font.bold: true
                        }

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

                                Rectangle {
                                    width: 184; height: 25; radius: 2
                                    color: "#ffffff"; border.color: "#10377d"; border.width: 1

                                    TextInput {
                                        id: pwdInput
                                        anchors.fill: parent; anchors.leftMargin: 6; anchors.rightMargin: 6
                                        verticalAlignment: TextInput.AlignVCenter
                                        echoMode: TextInput.Password; passwordCharacter: "●"
                                        color: "#000000"
                                        font.family: "Tahoma, 'Noto Sans', sans-serif"; font.pixelSize: 13
                                        selectByMouse: true; selectionColor: "#316ac5"; selectedTextColor: "#ffffff"
                                        clip: true; focus: !lockScreenUi.classicLogon

                                        onAccepted: lockScreenUi.submitPassword()
                                        onTextChanged: {
                                            if (text.length > 0) lockScreenUi.showHintBalloon = false
                                        }
                                        Keys.onEscapePressed: {
                                            lockScreenUi.showHintBalloon = false
                                            lockScreenUi.selectedTile = false
                                        }
                                    }
                                }

                                Image {
                                    width: 25; height: 25
                                    source: Qt.resolvedUrl("images/btn-go.svg")
                                    sourceSize.width: 50; sourceSize.height: 50; smooth: true
                                    scale: goBtnMouse.pressed ? 0.92 : 1.0
                                    MouseArea {
                                        id: goBtnMouse
                                        anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                                        onClicked: lockScreenUi.submitPassword()
                                    }
                                }

                                Image {
                                    width: 25; height: 25
                                    source: Qt.resolvedUrl("images/btn-help.svg")
                                    sourceSize.width: 50; sourceSize.height: 50; smooth: true
                                    scale: helpBtnMouse.pressed ? 0.92 : 1.0
                                    MouseArea {
                                        id: helpBtnMouse
                                        anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
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

                    Rectangle {
                        visible: lockScreenUi.showHintBalloon && lockScreenUi.selectedTile
                        x: 84; y: 96; width: 280; height: balloonCol.implicitHeight + 16; radius: 6
                        color: "#ffffe1"; border.color: "#000000"; border.width: 1; z: 50

                        Column {
                            id: balloonCol
                            anchors.fill: parent; anchors.margins: 8; spacing: 4
                            Text {
                                text: lockScreenUi.balloonTitle; color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11; font.bold: true
                            }
                            Text {
                                width: parent.width; text: lockScreenUi.balloonText; color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11; wrapMode: Text.WordWrap
                            }
                        }
                    }
                }
            }
        }

        // "welcome" scherm bij ontgrendelen
        Item {
            visible: lockScreenUi.welcomeMode
            anchors.top: topBar.bottom; anchors.bottom: bottomBar.top; anchors.left: parent.left; anchors.right: parent.right

            Text {
                anchors.centerIn: parent; anchors.horizontalCenterOffset: 43; anchors.verticalCenterOffset: -3
                text: "welcome"; color: "#2b4ea2"
                font.family: "Arial, Tahoma, sans-serif"; font.pixelSize: 48; font.bold: true; font.italic: true
            }
            Text {
                anchors.centerIn: parent; anchors.horizontalCenterOffset: 40; anchors.verticalCenterOffset: -6
                text: "welcome"; color: "#ffffff"
                font.family: "Arial, Tahoma, sans-serif"; font.pixelSize: 48; font.bold: true; font.italic: true
            }
        }
    }

    // =========================================================================
    // MODUS 2: KLASSIEK WINDOWS XP AANMELDSCHERM ("Log On to Windows" dialoog!)
    // Exact zoals media_1793528129582_59edf32c.png
    // =========================================================================
    Rectangle {
        id: classicStyleRoot
        anchors.fill: parent
        visible: lockScreenUi.classicLogon
        color: "#004e98"

        MouseArea {
            anchors.fill: parent
            onClicked: {
                powerPopup.visible = false
                classicPwdInput.forceActiveFocus()
            }
        }

        // Het gecentreerde "Log On to Windows" venster met Luna blauwe titelbalk
        Item {
            id: logonBox
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -24
            width: 448
            height: lockScreenUi.welcomeMode ? 195 : (lockScreenUi.classicShowOptions ? 326 : 284)

            // Buitenste Luna blauwe vensterrand
            Rectangle {
                anchors.fill: parent
                topLeftRadius: 7
                topRightRadius: 7
                color: "#00359c"
                border.color: "#00195c"
                border.width: 1
            }

            // 1. Luna Blauwe Titelbalk ("Log On to Windows")
            Rectangle {
                id: classicTitleBar
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 2
                height: 27
                topLeftRadius: 5
                topRightRadius: 5
                gradient: Gradient {
                    GradientStop { position: 0.00; color: "#3d95ff" }
                    GradientStop { position: 0.12; color: "#0058e6" }
                    GradientStop { position: 0.50; color: "#0054e3" }
                    GradientStop { position: 0.88; color: "#0047c4" }
                    GradientStop { position: 1.00; color: "#00369c" }
                }

                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Log On to Windows"
                    color: "#ffffff"
                    font.family: "Tahoma, 'Noto Sans', sans-serif"
                    font.pixelSize: 13
                    font.bold: true
                    style: Text.Raised
                    styleColor: "#062978"
                }
            }

            // 2. Blauwe Windows XP Professional Banner met het echte logo + oranje streep
            Rectangle {
                id: classicBanner
                anchors.top: classicTitleBar.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 3
                anchors.rightMargin: 3
                height: 102
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.00; color: "#4174dc" }
                    GradientStop { position: 0.45; color: "#6092ec" }
                    GradientStop { position: 0.85; color: "#5083e3" }
                    GradientStop { position: 1.00; color: "#3b6ed6" }
                }

                // Het echte Microsoft Windows XP logo gecentreerd in de banner
                Image {
                    id: classicBannerLogo
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.horizontalCenterOffset: 8
                    y: 6
                    width: 155
                    height: 92
                    source: Qt.resolvedUrl("images/xp-login-logo.png")
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    mipmap: true
                }

                Text {
                    anchors.left: classicBannerLogo.left
                    anchors.leftMargin: 30
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 6
                    text: "Professional x64 Edition"
                    color: "#ffffff"
                    font.family: "Tahoma, 'Noto Sans', sans-serif"
                    font.pixelSize: 13
                    letterSpacing: 0.3
                }

                // Linksonder in de banner: Copyright
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 7
                    text: "Copyright © 1985-2005\nMicrosoft Corporation"
                    color: "#e6f0ff"
                    font.family: "Tahoma, 'Noto Sans', sans-serif"
                    font.pixelSize: 9
                    lineHeight: 1.05
                }

                // Rechtsonder in de banner: Microsoft cursief
                Text {
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 7
                    text: "Microsoft"
                    color: "#ffffff"
                    font.family: "Tahoma, Arial, sans-serif"
                    font.pixelSize: 12
                    font.bold: true
                    font.italic: true
                }

                // Iconische oranje gloedlijn onderaan de banner
                Rectangle {
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 3
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.00; color: "#3b6ed6" }
                        GradientStop { position: 0.22; color: "#c97a3e" }
                        GradientStop { position: 0.45; color: "#ff8c1a" }
                        GradientStop { position: 0.65; color: "#e87e25" }
                        GradientStop { position: 1.00; color: "#3b6ed6" }
                    }
                }
            }

            // 3. Beige XP Formulier-gedeelte (#ece9d8)
            Rectangle {
                anchors.top: classicBanner.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 3
                anchors.rightMargin: 3
                anchors.bottomMargin: 3
                color: "#ece9d8"

                // Tijdens ontgrendelen: "Loading your personal settings..."
                Column {
                    visible: lockScreenUi.welcomeMode
                    anchors.left: parent.left
                    anchors.leftMargin: 22
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 6

                    Text {
                        text: "Loading your personal settings..."
                        color: "#000000"
                        font.family: "Tahoma, sans-serif"
                        font.pixelSize: 12
                        font.bold: true
                    }
                }

                // Normaal aanmeldformulier (User name, Password, OK/Cancel/Shut Down/Options)
                Item {
                    visible: !lockScreenUi.welcomeMode
                    anchors.fill: parent

                    // Rij 1: User name:
                    Text {
                        x: 16
                        y: 19
                        text: "User name:"
                        color: "#000000"
                        font.family: "Tahoma, 'Noto Sans', sans-serif"
                        font.pixelSize: 11
                    }

                    Rectangle {
                        x: 106
                        y: 15
                        width: 266
                        height: 22
                        color: "#ffffff"
                        border.color: "#7f9db9"
                        border.width: 1

                        TextInput {
                            id: classicUserInput
                            anchors.fill: parent
                            anchors.leftMargin: 5
                            anchors.rightMargin: 5
                            verticalAlignment: TextInput.AlignVCenter
                            text: lockScreenUi.displayUserName
                            color: "#000000"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 11
                            selectByMouse: true
                            selectionColor: "#316ac5"
                            selectedTextColor: "#ffffff"
                            clip: true
                            KeyNavigation.tab: classicPwdInput
                        }
                    }

                    // Rij 2: Password:
                    Text {
                        x: 16
                        y: 49
                        text: "Password:"
                        color: "#000000"
                        font.family: "Tahoma, 'Noto Sans', sans-serif"
                        font.pixelSize: 11
                    }

                    Rectangle {
                        x: 106
                        y: 45
                        width: 266
                        height: 22
                        color: "#ffffff"
                        border.color: "#7f9db9"
                        border.width: 1

                        TextInput {
                            id: classicPwdInput
                            anchors.fill: parent
                            anchors.leftMargin: 5
                            anchors.rightMargin: 5
                            verticalAlignment: TextInput.AlignVCenter
                            echoMode: TextInput.Password
                            passwordCharacter: "●"
                            color: "#000000"
                            font.family: "Tahoma, 'Noto Sans', sans-serif"
                            font.pixelSize: 12
                            selectByMouse: true
                            selectionColor: "#316ac5"
                            selectedTextColor: "#ffffff"
                            clip: true
                            focus: lockScreenUi.classicLogon
                            onAccepted: lockScreenUi.submitPassword()
                        }
                    }

                    // Rij 3 (indien Options << is uitgeklapt): Log on to:
                    Item {
                        visible: lockScreenUi.classicShowOptions
                        x: 0
                        y: 75
                        width: parent.width
                        height: 26

                        Text {
                            x: 16
                            y: 4
                            text: "Log on to:"
                            color: "#000000"
                            font.family: "Tahoma, sans-serif"
                            font.pixelSize: 11
                        }

                        Rectangle {
                            x: 106
                            y: 0
                            width: 266
                            height: 22
                            color: "#ffffff"
                            border.color: "#7f9db9"
                            border.width: 1

                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                x: 5
                                text: "BAZZITE-XP (This computer)"
                                color: "#000000"
                                font.family: "Tahoma, sans-serif"
                                font.pixelSize: 11
                            }

                            Rectangle {
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.bottom: parent.bottom
                                anchors.margins: 1
                                width: 17
                                radius: 1
                                color: "#d6e3f7"
                                border.color: "#7f9db9"
                                Text {
                                    anchors.centerIn: parent
                                    text: "▾"
                                    color: "#1d3f7a"
                                    font.pixelSize: 10
                                }
                            }
                        }
                    }

                    // Foutmelding indien wachtwoord onjuist
                    Text {
                        visible: lockScreenUi.showHintBalloon
                        x: 106
                        y: lockScreenUi.classicShowOptions ? 102 : 70
                        width: 320
                        text: "Het opgegeven wachtwoord is onjuist. Probeer het opnieuw."
                        color: "#b81d00"
                        font.family: "Tahoma, sans-serif"
                        font.pixelSize: 10
                    }

                    // Onderste rij met de 4 authentieke Windows XP knoppen: [ OK ] [ Cancel ] [ Shut Down... ] [ Options << ]
                    Row {
                        anchors.right: parent.right
                        anchors.rightMargin: 12
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 14
                        spacing: 8

                        // 1. [ OK ] (Default XP knop met blauwe binnenrand)
                        Rectangle {
                            width: 82; height: 24; radius: 3
                            border.color: "#003c74"; border.width: 1
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: okM.pressed ? "#e5e4da" : "#ffffff" }
                                GradientStop { position: 0.85; color: okM.pressed ? "#d5d2c6" : "#f0efe6" }
                                GradientStop { position: 1.0; color: "#d6d2c4" }
                            }
                            Rectangle {
                                anchors.fill: parent; anchors.margins: 1; radius: 2
                                color: "transparent"
                                border.color: okM.containsMouse ? "#f5b242" : "#699be3"
                                border.width: 1.5
                            }
                            Text {
                                anchors.centerIn: parent
                                text: "OK"
                                color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                            }
                            MouseArea {
                                id: okM; anchors.fill: parent; hoverEnabled: true
                                onClicked: lockScreenUi.submitPassword()
                            }
                        }

                        // 2. [ Cancel ]
                        Rectangle {
                            width: 82; height: 24; radius: 3
                            border.color: "#003c74"; border.width: 1
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: canM.pressed ? "#e5e4da" : "#ffffff" }
                                GradientStop { position: 0.85; color: canM.pressed ? "#d5d2c6" : "#f0efe6" }
                                GradientStop { position: 1.0; color: "#d6d2c4" }
                            }
                            Rectangle {
                                visible: canM.containsMouse
                                anchors.fill: parent; anchors.margins: 1; radius: 2
                                color: "transparent"; border.color: "#f5b242"; border.width: 1.5
                            }
                            Text {
                                anchors.centerIn: parent
                                text: "Cancel"
                                color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                            }
                            MouseArea {
                                id: canM; anchors.fill: parent; hoverEnabled: true
                                onClicked: {
                                    classicPwdInput.text = ""
                                    lockScreenUi.showHintBalloon = false
                                    classicPwdInput.forceActiveFocus()
                                }
                            }
                        }

                        // 3. [ Shut Down... ]
                        Rectangle {
                            width: 88; height: 24; radius: 3
                            border.color: "#003c74"; border.width: 1
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: sdM.pressed ? "#e5e4da" : "#ffffff" }
                                GradientStop { position: 0.85; color: sdM.pressed ? "#d5d2c6" : "#f0efe6" }
                                GradientStop { position: 1.0; color: "#d6d2c4" }
                            }
                            Rectangle {
                                visible: sdM.containsMouse
                                anchors.fill: parent; anchors.margins: 1; radius: 2
                                color: "transparent"; border.color: "#f5b242"; border.width: 1.5
                            }
                            Text {
                                anchors.centerIn: parent
                                text: "Shut Down..."
                                color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                            }
                            MouseArea {
                                id: sdM; anchors.fill: parent; hoverEnabled: true
                                onClicked: powerPopup.visible = !powerPopup.visible
                            }
                        }

                        // 4. [ Options << ]
                        Rectangle {
                            width: 86; height: 24; radius: 3
                            border.color: "#003c74"; border.width: 1
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: optM.pressed ? "#e5e4da" : "#ffffff" }
                                GradientStop { position: 0.85; color: optM.pressed ? "#d5d2c6" : "#f0efe6" }
                                GradientStop { position: 1.0; color: "#d6d2c4" }
                            }
                            Rectangle {
                                visible: optM.containsMouse
                                anchors.fill: parent; anchors.margins: 1; radius: 2
                                color: "transparent"; border.color: "#f5b242"; border.width: 1.5
                            }
                            Text {
                                anchors.centerIn: parent
                                text: lockScreenUi.classicShowOptions ? "Options <<" : "Options >>"
                                color: "#000000"
                                font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                            }
                            MouseArea {
                                id: optM; anchors.fill: parent; hoverEnabled: true
                                onClicked: lockScreenUi.classicShowOptions = !lockScreenUi.classicShowOptions
                            }
                        }
                    }
                }
            }
        }
    }

    // === KLEIN XP MENU VOOR "Turn off computer" / "Shut Down..." ===
    Rectangle {
        id: powerPopup
        visible: false
        x: lockScreenUi.classicLogon ? Math.round(parent.width / 2 - 95) : 32
        y: lockScreenUi.classicLogon ? Math.round(parent.height / 2 + 120) : (parent.height - bottomBar.height - height - 6)
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
