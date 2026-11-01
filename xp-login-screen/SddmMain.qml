import QtQuick
import QtQuick.Controls
import SddmComponents 2.0
import "xpConfig.js" as XpConfig

Rectangle {
    id: container
    width: 1920
    height: 1080
    color: logonStyle === "classic" ? "#004e98" : "#5a7edc"

    property string logonStyle: XpConfig.logonStyle || "welcome"
    property int sessionIndex: (typeof sessionModel !== "undefined" && sessionModel.lastIndex >= 0) ? sessionModel.lastIndex : 0
    property string currentUserName: (typeof userModel !== "undefined" && userModel.lastUser) ? userModel.lastUser : "king"
    property bool selectedTile: true
    property bool showHintBalloon: false
    property string balloonTitle: "Password Hint:"
    property string balloonText: "Voer je Bazzite gebruikerswachtwoord in en druk op Enter."
    property bool welcomeMode: false

    TextConstants { id: textConstants }

    Connections {
        target: sddm
        function onLoginSucceeded() {
            welcomeMode = true
        }
        function onLoginFailed() {
            welcomeMode = false
            pwdInput.text = ""
            classicPassInput.text = ""
            balloonTitle = "Did you forget your password?"
            balloonText = "Please type your password again.\nBe sure to use the correct uppercase and lowercase letters."
            showHintBalloon = true
            if (container.logonStyle === "classic") {
                classicPassInput.forceActiveFocus()
            } else {
                pwdInput.forceActiveFocus()
            }
        }
    }

    function doLogin() {
        showHintBalloon = false
        let pw = (container.logonStyle === "classic") ? classicPassInput.text : pwdInput.text
        sddm.login(currentUserName, pw, sessionIndex)
    }

    // === MODUS A: STANDAARD WINDOWS XP WELKOMSTSCHERM ("welcome") ===
    Item {
        anchors.fill: parent
        visible: container.logonStyle !== "classic"

        Image {
            x: -parent.width * 0.08
            y: topBar.height - parent.height * 0.14
            width: Math.round(parent.width * 0.56)
            height: Math.round(parent.width * 0.56)
            source: Qt.resolvedUrl("assets/xp-radial-glow.svg")
            smooth: true
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                container.showHintBalloon = false
                powerPopup.visible = false
                container.selectedTile = false
            }
        }

        Rectangle {
            id: topBar
            anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
            height: Math.max(76, Math.round(parent.height * 0.118))
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#002b8f" }
                GradientStop { position: 1.0; color: "#003399" }
            }
            Rectangle {
                anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; height: 2
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

        Rectangle {
            id: bottomBar
            anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right
            height: Math.max(72, Math.round(parent.height * 0.112))
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "#283894" }
                GradientStop { position: 0.4; color: "#143091" }
                GradientStop { position: 1.0; color: "#002987" }
            }
            Rectangle {
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; height: 2
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
                visible: !container.welcomeMode
                anchors.left: parent.left; anchors.leftMargin: 32; anchors.verticalCenter: parent.verticalCenter
                spacing: 10
                Image {
                    width: 28; height: 28; anchors.verticalCenter: parent.verticalCenter
                    source: Qt.resolvedUrl("assets/btn-power.svg")
                    sourceSize.width: 56; sourceSize.height: 56; smooth: true
                    MouseArea {
                        anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: powerPopup.visible = !powerPopup.visible
                    }
                }
                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Turn off computer"
                    color: "#ffffff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 15
                    MouseArea {
                        anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: powerPopup.visible = !powerPopup.visible
                    }
                }
            }

            Column {
                visible: !container.welcomeMode
                anchors.right: parent.right; anchors.rightMargin: 32; anchors.verticalCenter: parent.verticalCenter
                spacing: 2
                Text {
                    anchors.right: parent.right
                    text: "After you log on, you can add or change accounts."
                    color: "#dce8ff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                }
                Text {
                    anchors.right: parent.right
                    text: "Just go to your Control Panel and click User Accounts."
                    color: "#dce8ff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                }
            }
        }

        Item {
            visible: !container.welcomeMode
            anchors.top: topBar.bottom; anchors.bottom: bottomBar.top; anchors.left: parent.left; anchors.right: parent.right

            Rectangle {
                id: centerDivider
                x: Math.round(parent.width * 0.49)
                y: Math.round(parent.height * 0.08)
                width: 1; height: Math.round(parent.height * 0.84)
                gradient: Gradient {
                    GradientStop { position: 0.00; color: "transparent" }
                    GradientStop { position: 0.20; color: "#8cb0f2" }
                    GradientStop { position: 0.50; color: "#c2daff" }
                    GradientStop { position: 0.80; color: "#8cb0f2" }
                    GradientStop { position: 1.00; color: "transparent" }
                }
            }

            Column {
                anchors.right: centerDivider.left; anchors.rightMargin: 42
                anchors.verticalCenter: parent.verticalCenter; anchors.verticalCenterOffset: -18
                spacing: 20

                Image {
                    anchors.right: parent.right; width: 235; height: 142
                    source: Qt.resolvedUrl("assets/xp-login-logo.png")
                    fillMode: Image.PreserveAspectFit; smooth: true; mipmap: true
                }
                Text {
                    anchors.right: parent.right
                    text: "To begin, click your user name"
                    color: "#ffffff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 19
                    style: Text.Raised; styleColor: "#3052a6"
                }
            }

            Item {
                anchors.left: centerDivider.right; anchors.leftMargin: 36
                anchors.verticalCenter: parent.verticalCenter; anchors.verticalCenterOffset: -10
                width: 410; height: container.selectedTile ? 92 : 74

                Rectangle {
                    anchors.fill: parent; radius: 6
                    visible: container.selectedTile
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.00; color: "#1140aa" }
                        GradientStop { position: 0.52; color: "#2153bf" }
                        GradientStop { position: 0.88; color: "#4b72d4" }
                        GradientStop { position: 1.00; color: "#5a7edc" }
                    }
                }
                Rectangle {
                    visible: container.selectedTile
                    anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "#a8c6ff" }
                        GradientStop { position: 0.7; color: "#7da3eb" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
                Rectangle {
                    visible: container.selectedTile
                    anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "#a8c6ff" }
                        GradientStop { position: 0.7; color: "#7da3eb" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
                Rectangle {
                    visible: container.selectedTile
                    anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.topMargin: 3; anchors.bottomMargin: 3; width: 1
                    color: "#a8c6ff"
                }

                MouseArea {
                    anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                    onClicked: { container.selectedTile = true; pwdInput.forceActiveFocus() }
                }

                Rectangle {
                    id: avatarBorder
                    x: 12; y: 10; width: 58; height: 58; radius: 4
                    color: "#1b439c"; border.width: 2
                    border.color: container.selectedTile ? "#ffcc00" : "#e6f0ff"
                    Image {
                        anchors.fill: parent; anchors.margins: 2
                        source: Qt.resolvedUrl("assets/xp-avatar.png")
                        fillMode: Image.PreserveAspectCrop; smooth: true
                    }
                }

                Column {
                    anchors.left: avatarBorder.right; anchors.leftMargin: 14
                    anchors.top: avatarBorder.top; anchors.topMargin: -2
                    spacing: 3

                    Text {
                        text: "King Geoffrey"
                        color: "#ffffff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 18
                        font.bold: container.selectedTile; style: Text.Raised; styleColor: "#0d2e7a"
                    }

                    Column {
                        visible: container.selectedTile
                        spacing: 3
                        Text {
                            text: "Type your password"
                            color: "#ffffff"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11
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
                                    color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 13
                                    clip: true; focus: container.logonStyle !== "classic"
                                    onAccepted: container.doLogin()
                                }
                            }
                            Image {
                                width: 25; height: 25
                                source: Qt.resolvedUrl("assets/btn-go.svg")
                                sourceSize.width: 50; sourceSize.height: 50; smooth: true
                                MouseArea {
                                    anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                    onClicked: container.doLogin()
                                }
                            }
                            Image {
                                width: 25; height: 25
                                source: Qt.resolvedUrl("assets/btn-help.svg")
                                sourceSize.width: 50; sourceSize.height: 50; smooth: true
                                MouseArea {
                                    anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                    onClicked: container.showHintBalloon = !container.showHintBalloon
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    visible: container.showHintBalloon && container.selectedTile
                    x: 84; y: 96; width: 280; height: bCol.implicitHeight + 16; radius: 6
                    color: "#ffffe1"; border.color: "#000000"; border.width: 1; z: 50
                    Column {
                        id: bCol; anchors.fill: parent; anchors.margins: 8; spacing: 4
                        Text { text: container.balloonTitle; font.family: "Tahoma, sans-serif"; font.pixelSize: 11; font.bold: true }
                        Text { width: parent.width; text: container.balloonText; font.family: "Tahoma, sans-serif"; font.pixelSize: 11; wrapMode: Text.WordWrap }
                    }
                }
            }
        }

        Item {
            visible: container.welcomeMode
            anchors.top: topBar.bottom; anchors.bottom: bottomBar.top; anchors.left: parent.left; anchors.right: parent.right
            Text {
                anchors.centerIn: parent; anchors.horizontalCenterOffset: 43; anchors.verticalCenterOffset: -3
                text: "welcome"; color: "#2b4ea2"; font.family: "Arial, Tahoma, sans-serif"; font.pixelSize: 48; font.bold: true; font.italic: true
            }
            Text {
                anchors.centerIn: parent; anchors.horizontalCenterOffset: 40; anchors.verticalCenterOffset: -6
                text: "welcome"; color: "#ffffff"; font.family: "Arial, Tahoma, sans-serif"; font.pixelSize: 48; font.bold: true; font.italic: true
            }
        }

        Rectangle {
            id: powerPopup
            visible: false
            anchors.left: parent.left; anchors.leftMargin: 32; anchors.bottom: bottomBar.top; anchors.bottomMargin: 6
            width: 180; height: 58; radius: 3; color: "#ffffff"; border.color: "#00309c"; border.width: 1; z: 100
            Column {
                anchors.fill: parent; anchors.margins: 4; spacing: 2
                Rectangle {
                    width: parent.width; height: 24; color: m1.containsMouse ? "#316ac5" : "transparent"
                    Text { anchors.verticalCenter: parent.verticalCenter; x: 8; text: "Turn Off"; color: m1.containsMouse ? "white" : "black"; font.pixelSize: 12 }
                    MouseArea { id: m1; anchors.fill: parent; hoverEnabled: true; onClicked: sddm.powerOff() }
                }
                Rectangle {
                    width: parent.width; height: 24; color: m2.containsMouse ? "#316ac5" : "transparent"
                    Text { anchors.verticalCenter: parent.verticalCenter; x: 8; text: "Restart"; color: m2.containsMouse ? "white" : "black"; font.pixelSize: 12 }
                    MouseArea { id: m2; anchors.fill: parent; hoverEnabled: true; onClicked: sddm.reboot() }
                }
            }
        }
    }

    // === MODUS B: KLASSIEK WINDOWS XP AANMELDSCHERM ("Log On to Windows") ===
    Rectangle {
        anchors.fill: parent
        visible: container.logonStyle === "classic"
        color: "#004e98"

        Rectangle {
            width: 436; height: 258
            anchors.centerIn: parent; anchors.verticalCenterOffset: -20
            color: "#ece9d8"
            border.color: "#00195c"; border.width: 1; radius: 5

            Rectangle {
                anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left; width: 3; color: "#0046d5"
            }
            Rectangle {
                anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.right: parent.right; width: 3; color: "#0035a8"
            }
            Rectangle {
                anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; height: 3; color: "#0035a8"
            }

            Rectangle {
                id: sddmClTitle
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
                height: 28; topLeftRadius: 5; topRightRadius: 5
                gradient: Gradient {
                    GradientStop { position: 0.00; color: "#3d95ff" }
                    GradientStop { position: 0.12; color: "#0058ee" }
                    GradientStop { position: 0.50; color: "#0054e3" }
                    GradientStop { position: 0.88; color: "#0046c7" }
                    GradientStop { position: 1.00; color: "#026afe" }
                }
                Text {
                    anchors.left: parent.left; anchors.leftMargin: 9; anchors.verticalCenter: parent.verticalCenter
                    text: "Log On to Windows"; color: "#ffffff"
                    font.family: "Trebuchet MS, Tahoma, sans-serif"; font.pixelSize: 13; font.bold: true
                    style: Text.Raised; styleColor: "#0a246a"
                }
            }

            Rectangle {
                id: sddmClBanner
                anchors.top: sddmClTitle.bottom; anchors.left: parent.left; anchors.right: parent.right
                anchors.leftMargin: 3; anchors.rightMargin: 3; height: 88
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.00; color: "#4e71cc" }
                    GradientStop { position: 0.45; color: "#688be0" }
                    GradientStop { position: 1.00; color: "#799ae8" }
                }
                Image {
                    x: 112; y: 4; width: 205; height: 68
                    source: Qt.resolvedUrl("assets/xp-login-logo.png")
                    fillMode: Image.PreserveAspectFit; smooth: true; mipmap: true
                }
                Text {
                    x: 192; y: 58
                    text: "Professional x64 Edition"; color: "#ffffff"
                    font.family: "Tahoma, sans-serif"; font.pixelSize: 14
                }
                Text {
                    anchors.left: parent.left; anchors.leftMargin: 7; anchors.bottom: parent.bottom; anchors.bottomMargin: 6
                    text: "Copyright © 1985-2005\nMicrosoft Corporation"; color: "#ffffff"
                    font.family: "Tahoma, sans-serif"; font.pixelSize: 9; lineHeight: 1.05
                }
                Text {
                    anchors.right: parent.right; anchors.rightMargin: 9; anchors.bottom: parent.bottom; anchors.bottomMargin: 6
                    text: "Microsoft"; color: "#ffffff"
                    font.family: "Arial, Tahoma, sans-serif"; font.pixelSize: 12; font.bold: true; font.italic: true
                }
            }

            Rectangle {
                id: sddmClOrange
                anchors.top: sddmClBanner.bottom; anchors.left: parent.left; anchors.right: parent.right
                anchors.leftMargin: 3; anchors.rightMargin: 3; height: 4
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.00; color: "#d7c9a9" }
                    GradientStop { position: 0.25; color: "#e88b2c" }
                    GradientStop { position: 0.50; color: "#ff8c00" }
                    GradientStop { position: 0.78; color: "#7e9de2" }
                    GradientStop { position: 1.00; color: "#577ad0" }
                }
            }

            Item {
                anchors.top: sddmClOrange.bottom; anchors.bottom: parent.bottom
                anchors.left: parent.left; anchors.right: parent.right; anchors.margins: 3

                Text {
                    x: 10; y: 20
                    text: "User name:"; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                }
                Rectangle {
                    x: 84; y: 16; width: 256; height: 22
                    color: "#ffffff"; border.color: "#7f9db9"; border.width: 1
                    TextInput {
                        anchors.fill: parent; anchors.leftMargin: 5; anchors.rightMargin: 5
                        verticalAlignment: TextInput.AlignVCenter
                        text: "King Geoffrey"; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                        readOnly: true
                    }
                }
                Text {
                    x: 10; y: 50
                    text: "Password:"; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11
                }
                Rectangle {
                    x: 84; y: 46; width: 256; height: 22
                    color: "#ffffff"; border.color: "#7f9db9"; border.width: 1
                    TextInput {
                        id: classicPassInput
                        anchors.fill: parent; anchors.leftMargin: 5; anchors.rightMargin: 5
                        verticalAlignment: TextInput.AlignVCenter
                        echoMode: TextInput.Password; passwordCharacter: "●"
                        color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                        focus: container.logonStyle === "classic"
                        onAccepted: container.doLogin()
                    }
                }

                Row {
                    x: 84; y: 92; spacing: 8
                    Rectangle {
                        width: 76; height: 24; radius: 3; border.color: "#003c74"; border.width: 1
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#ffffff" }
                            GradientStop { position: 0.85; color: "#ecebe3" }
                            GradientStop { position: 1.0; color: "#d6d2c2" }
                        }
                        Rectangle { anchors.fill: parent; anchors.margins: 1; radius: 2; color: "transparent"; border.color: "#72ace8"; border.width: 1 }
                        Text { anchors.centerIn: parent; text: "OK"; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11 }
                        MouseArea { anchors.fill: parent; onClicked: container.doLogin() }
                    }
                    Rectangle {
                        width: 76; height: 24; radius: 3; color: "#f5f4ea"; border.color: "#c9c7ba"; border.width: 1
                        Text { anchors.centerIn: parent; text: "Cancel"; color: "#a19f92"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11 }
                    }
                    Rectangle {
                        width: 78; height: 24; radius: 3; border.color: "#003c74"; border.width: 1
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#ffffff" }
                            GradientStop { position: 0.85; color: "#ecebe3" }
                            GradientStop { position: 1.0; color: "#d6d2c2" }
                        }
                        Text { anchors.centerIn: parent; text: "Shut Down..."; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11 }
                        MouseArea { anchors.fill: parent; onClicked: sddm.powerOff() }
                    }
                    Rectangle {
                        width: 76; height: 24; radius: 3; border.color: "#003c74"; border.width: 1
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#ffffff" }
                            GradientStop { position: 0.85; color: "#ecebe3" }
                            GradientStop { position: 1.0; color: "#d6d2c2" }
                        }
                        Text { anchors.centerIn: parent; text: "Options <<"; color: "#000000"; font.family: "Tahoma, sans-serif"; font.pixelSize: 11 }
                    }
                }
            }
        }
    }
}
