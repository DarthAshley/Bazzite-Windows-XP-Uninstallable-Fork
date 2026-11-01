import QtCore
import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasma5support as P5Support

PlasmoidItem {
    id: root

    property bool expanded: false
    property bool muted: false
    property string timeString: "00:00"
    property string dateString: ""

    readonly property string xpScript: StandardPaths.writableLocation(StandardPaths.GenericDataLocation) + "/xp-startknop/xp-verkenner.py"
    readonly property string sniListCmd: "python3 '" + xpScript + "' sni-list"

    ListModel {
        id: sniAppsModel
    }

    function updateClock() {
        let now = new Date()
        let hh = ("0" + now.getHours()).slice(-2)
        let mm = ("0" + now.getMinutes()).slice(-2)
        root.timeString = hh + ":" + mm
        root.dateString = Qt.formatDate(now, "dddd d MMMM yyyy")
    }

    function refreshSni() {
        sniSource.connectSource(root.sniListCmd)
    }

    function runCmd(cmd) {
        execSource.connectSource(cmd)
    }

    Component.onCompleted: {
        updateClock()
        refreshSni()
    }

    Timer {
        interval: 2500
        running: true
        repeat: true
        onTriggered: {
            root.updateClock()
            root.refreshSni()
        }
    }

    P5Support.DataSource {
        id: execSource
        engine: "executable"
        onNewData: source => disconnectSource(source)
    }

    P5Support.DataSource {
        id: sniSource
        engine: "executable"
        onNewData: (source, data) => {
            let out = (data["stdout"] || "").trim()
            disconnectSource(source)
            if (out === "") return
            try {
                let parsed = JSON.parse(out)
                // Alleen bijwerken als de lijst veranderd is om knipperen te voorkomen
                let same = (parsed.length === sniAppsModel.count)
                if (same) {
                    for (let k = 0; k < parsed.length; ++k) {
                        let cur = sniAppsModel.get(k)
                        if (cur.sniService !== parsed[k].service || cur.sniIcon !== parsed[k].icon) {
                            same = false
                            break
                        }
                    }
                }
                if (!same) {
                    sniAppsModel.clear()
                    for (let i = 0; i < parsed.length; ++i) {
                        sniAppsModel.append({
                            "sniService": parsed[i].service || "",
                            "sniPath": parsed[i].path || "/StatusNotifierItem",
                            "sniId": parsed[i].id || "",
                            "sniTitle": parsed[i].title || "",
                            "sniIcon": parsed[i].icon || "application-x-executable",
                            "sniMenu": parsed[i].menu || "/com/canonical/dbusmenu"
                        })
                    }
                }
            } catch (e) {}
        }
    }

    Plasmoid.contextualActions: [
        PlasmaCore.Action {
            text: "Datum en tijd aanpassen"
            icon.name: "preferences-system-time"
            onTriggered: root.runCmd("kcmshell6 kcm_clock")
        },
        PlasmaCore.Action {
            text: "Meldingen aanpassen..."
            icon.name: "preferences-desktop-notification"
            onTriggered: root.runCmd("kcmshell6 kcm_notifications")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Het bureaublad weergeven"
            icon.name: "user-desktop"
            onTriggered: root.runCmd("if [ \"$(qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showingDesktop)\" = \"true\" ]; then qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop false; else qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop true; fi")
        },
        PlasmaCore.Action {
            text: "Taakbeheer"
            icon.name: "utilities-system-monitor"
            onTriggered: root.runCmd("python3 \"$HOME/.local/share/xp-startknop/xp-verkenner.py\" taakbeheer")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Eigenschappen"
            icon.name: "configure"
            onTriggered: root.runCmd("python3 \"$HOME/.local/share/xp-startknop/xp-verkenner.py\" taakbalk")
        }
    ]

    preferredRepresentation: fullRepresentation
    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    Plasmoid.constraintHints: Plasmoid.CanFillArea

    compactRepresentation: null

    fullRepresentation: Item {
        id: trayItem

        // Paneel heeft rechts 10px marge; we trekken het lichtblauwe XP-systeemvak door tot de rechterrand
        readonly property int panelRightMargin: 10
        readonly property int contentWidth: trayRow.implicitWidth + 24

        Layout.minimumWidth: contentWidth - panelRightMargin
        Layout.preferredWidth: contentWidth - panelRightMargin
        Layout.maximumWidth: contentWidth - panelRightMargin
        Layout.fillHeight: true

        // Het lichtblauwe verzonken Windows XP Systeemvak (Notification Area)
        Rectangle {
            x: 0
            y: 0
            width: trayItem.contentWidth
            height: trayItem.height

            gradient: Gradient {
                GradientStop { position: 0.0; color: "#1aa9f8" }
                GradientStop { position: 0.08; color: "#0d84e3" }
                GradientStop { position: 0.22; color: "#1597ef" }
                GradientStop { position: 0.82; color: "#0f85e4" }
                GradientStop { position: 1.0; color: "#0a69c2" }
            }

            // Lichtblauwe bovenste highlight-lijn
            Rectangle {
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: 2
                color: "#38b6ff"
                opacity: 0.85
            }

            // Linker 3D scheidingsrand tussen donkerblauwe taakbalk en lichtblauw systeemvak
            Rectangle {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                width: 2
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#083d8c" }
                    GradientStop { position: 0.5; color: "#0a4da8" }
                    GradientStop { position: 1.0; color: "#07347a" }
                }
            }
            Rectangle {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                x: 2
                width: 1
                color: "#43b7ff"
                opacity: 0.7
            }

            // Ronde blauwe 3D Windows XP Chevron-knop (< / >) op de linkerrand van het systeemvak
            Rectangle {
                id: chevronBtn
                x: -8
                anchors.verticalCenter: parent.verticalCenter
                width: 18
                height: 18
                radius: 9
                border.color: "#093c8c"
                border.width: 1
                gradient: Gradient {
                    GradientStop { position: 0.0; color: chevronMouse.containsMouse ? "#7cd2ff" : "#5cbcff" }
                    GradientStop { position: 0.5; color: chevronMouse.containsMouse ? "#2894f4" : "#1682e8" }
                    GradientStop { position: 1.0; color: "#0a58b8" }
                }

                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 1
                    radius: 8
                    color: "transparent"
                    border.color: "#b8e6ff"
                    border.width: 1
                    opacity: 0.65
                }

                Text {
                    anchors.centerIn: parent
                    text: root.expanded ? "›" : "‹"
                    color: "white"
                    font.family: "Tahoma"
                    font.pixelSize: 13
                    font.bold: true
                }

                MouseArea {
                    id: chevronMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.expanded = !root.expanded
                }
            }

            Row {
                id: trayRow
                x: 13
                anchors.verticalCenter: parent.verticalCenter
                spacing: 5

                // Verborgen / uitklapbare systeemvak-icoontjes (zichtbaar na klik op <)
                Row {
                    visible: root.expanded
                    spacing: 5
                    anchors.verticalCenter: parent.verticalCenter

                    // Hardware veilig verwijderen / Schijven
                    Item {
                        width: 16; height: 16
                        Image {
                            anchors.fill: parent
                            source: Qt.resolvedUrl("../images/tray-usb.svg")
                            sourceSize.width: 32; sourceSize.height: 32
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: root.runCmd("kcmshell6 kcm_device_automounter")
                        }
                    }

                    // Bluetooth
                    Item {
                        width: 16; height: 16
                        Image {
                            anchors.fill: parent
                            source: Qt.resolvedUrl("../images/tray-bt.svg")
                            sourceSize.width: 32; sourceSize.height: 32
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: root.runCmd("kcmshell6 kcm_bluetooth")
                        }
                    }

                    // Beeldscherminstellingen
                    Item {
                        width: 16; height: 16
                        Image {
                            anchors.fill: parent
                            source: Qt.resolvedUrl("../images/cp-display.svg")
                            sourceSize.width: 32; sourceSize.height: 32
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: root.runCmd("python3 '" + root.xpScript + "' beeldscherm")
                        }
                    }
                }

                // === LIVE ACHTERGROND-APPLICATIES (Discord, Steam, Unity Hub, Easy Effects, etc.) ===
                Repeater {
                    model: sniAppsModel
                    delegate: Item {
                        required property int index
                        required property string sniService
                        required property string sniPath
                        required property string sniId
                        required property string sniTitle
                        required property string sniIcon
                        required property string sniMenu

                        width: 16
                        height: 16
                        anchors.verticalCenter: parent.verticalCenter

                        Image {
                            anchors.fill: parent
                            visible: sniIcon.startsWith("file://")
                            source: sniIcon.startsWith("file://") ? sniIcon : ""
                            sourceSize.width: 32
                            sourceSize.height: 32
                            smooth: true
                        }

                        Kirigami.Icon {
                            anchors.fill: parent
                            visible: !sniIcon.startsWith("file://")
                            source: !sniIcon.startsWith("file://") ? sniIcon : ""
                        }

                        PlasmaCore.ToolTipArea {
                            anchors.fill: parent
                            mainText: sniTitle
                            subText: "Klik om te openen, rechtsklik voor opties"
                        }

                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton | Qt.RightButton
                            onClicked: mouse => {
                                if (mouse.button === Qt.RightButton) {
                                    root.runCmd("python3 '" + root.xpScript + "' sni-menu '" + sniService + "' '" + sniPath + "' '" + sniMenu + "'")
                                } else {
                                    root.runCmd("python3 '" + root.xpScript + "' sni-activate '" + sniService + "' '" + sniPath + "' '" + sniMenu + "'")
                                }
                            }
                        }
                    }
                }

                // 1. Netwerkverbinding (Twee lichtgevende XP-monitortjes)
                Item {
                    width: 16; height: 16
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/tray-net.svg")
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "LAN-verbinding"
                        subText: "Verbonden"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.runCmd("kcmshell6 kcm_networkmanagement")
                    }
                }

                // 2. Windows XP Beveiligingscentrum Schildje
                Item {
                    width: 16; height: 16
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/xp-shield.svg")
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "Windows XP Beveiligingscentrum"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.runCmd("python3 '" + root.xpScript + "' configuratiescherm")
                    }
                }

                // 3. Volume / Geluid (grijs XP-luidsprekertje; scrollen regelt volume!)
                Item {
                    width: 16; height: 16
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/" + (root.muted ? "tray-muted.svg" : "tray-audio.svg"))
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "Volume"
                        subText: "Scroll om volume aan te passen"
                    }
                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.MiddleButton
                        onClicked: mouse => {
                            if (mouse.button === Qt.MiddleButton) {
                                root.muted = !root.muted
                                root.runCmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")
                            } else {
                                root.runCmd("kcmshell6 kcm_pulseaudio")
                            }
                        }
                        onWheel: wheel => {
                            if (wheel.angleDelta.y > 0) {
                                root.runCmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+")
                            } else {
                                root.runCmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")
                            }
                        }
                    }
                }

                // 4. Enkele-regel witte Tahoma Klok (zoals in origineel Windows XP!)
                Item {
                    width: clockText.implicitWidth + 8
                    height: 22
                    anchors.verticalCenter: parent.verticalCenter

                    Text {
                        id: clockText
                        anchors.centerIn: parent
                        text: root.timeString
                        color: "white"
                        renderType: Text.NativeRendering
                        font.family: "Tahoma"
                        font.pixelSize: 12
                    }

                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: root.dateString
                        subText: "Klik om Datum en tijd te openen"
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.runCmd("kcmshell6 kcm_clock")
                    }
                }
            }
        }
    }
}
