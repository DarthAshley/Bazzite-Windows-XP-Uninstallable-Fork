import QtQuick

Item {
    id: root
    property int stage: 0
    property bool showWelcome: false

    onStageChanged: {
        if (stage >= 3) {
            showWelcome = true
        }
    }

    Timer {
        interval: 1600
        running: true
        repeat: false
        onTriggered: root.showWelcome = true
    }

    // === HOOFDCANVAS (Middenblauw #5a7edc met linksboven radiale gloed) ===
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
            visible: !root.showWelcome
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
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: "Turn off computer"
                color: "#ffffff"
                font.family: "Tahoma, 'Noto Sans', sans-serif"
                font.pixelSize: 15
            }
        }

        // Rechtsonder: Twee regels XP uitlegtekst
        Column {
            visible: !root.showWelcome
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

    // === FASE 1: WINDOWS XP LOGIN SCHERM (Exact zoals screenshot 1!) ===
    Item {
        visible: !root.showWelcome
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

        Item {
            anchors.left: centerDivider.right
            anchors.leftMargin: 36
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -10
            width: 410
            height: 92

            Rectangle {
                anchors.fill: parent
                radius: 6
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.00; color: "#1140aa" }
                    GradientStop { position: 0.52; color: "#2153bf" }
                    GradientStop { position: 0.88; color: "#4b72d4" }
                    GradientStop { position: 1.00; color: "#5a7edc" }
                }
            }

            Rectangle {
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#a8c6ff" }
                    GradientStop { position: 0.7; color: "#7da3eb" }
                    GradientStop { position: 1.0; color: "transparent" }
                }
            }
            Rectangle {
                anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.leftMargin: 4; height: 1
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#a8c6ff" }
                    GradientStop { position: 0.7; color: "#7da3eb" }
                    GradientStop { position: 1.0; color: "transparent" }
                }
            }
            Rectangle {
                anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.topMargin: 3; anchors.bottomMargin: 3; width: 1
                color: "#a8c6ff"
            }

            Rectangle {
                id: splashAvatar
                x: 12; y: 10; width: 58; height: 58; radius: 4
                color: "#1b439c"
                border.width: 2; border.color: "#ffcc00"
                Image {
                    anchors.fill: parent; anchors.margins: 2
                    source: Qt.resolvedUrl("images/xp-avatar.png")
                    fillMode: Image.PreserveAspectCrop; smooth: true
                }
            }

            Column {
                anchors.left: splashAvatar.right; anchors.leftMargin: 14
                anchors.top: splashAvatar.top; anchors.topMargin: -2
                spacing: 3

                Text {
                    text: "King Geoffrey"
                    color: "#ffffff"
                    font.family: "Tahoma, 'Noto Sans', sans-serif"
                    font.pixelSize: 18; font.bold: true
                    style: Text.Raised; styleColor: "#0d2e7a"
                }

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
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            x: 7
                            text: "●●●●●●●●"
                            color: "#000000"
                            font.family: "Tahoma, sans-serif"; font.pixelSize: 12
                        }
                    }

                    Image {
                        width: 25; height: 25
                        source: Qt.resolvedUrl("images/btn-go.svg")
                        sourceSize.width: 50; sourceSize.height: 50; smooth: true
                    }

                    Image {
                        width: 25; height: 25
                        source: Qt.resolvedUrl("images/btn-help.svg")
                        sourceSize.width: 50; sourceSize.height: 50; smooth: true
                    }
                }
            }
        }
    }

    // === FASE 2: "welcome" SCHERM (Exact zoals screenshot 3!) ===
    Item {
        visible: root.showWelcome
        anchors.top: topBar.bottom
        anchors.bottom: bottomBar.top
        anchors.left: parent.left
        anchors.right: parent.right

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
}
