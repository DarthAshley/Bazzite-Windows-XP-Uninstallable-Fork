import QtCore
import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasma5support as P5Support
import "xpConfig.js" as XpConfig

PlasmoidItem {
    id: root

    property bool expanded: false
    property bool muted: false
    property string timeString: "00:00"
    property string dateString: ""

    readonly property bool isClassicTaskbar: (XpConfig.taskbarStyle || "xp") === "classic"
    readonly property bool showClockSetting: XpConfig.showClock !== false

    readonly property string xpScript: (StandardPaths.writableLocation(StandardPaths.GenericDataLocation) + "/xp-startknop/xp-verkenner.py").replace(/^file:\/\//, "")
    readonly property string sniListCmd: "python3 \"" + xpScript + "\" sni-list"
    property int _pollSeq: 0

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
        root._pollSeq = (root._pollSeq + 1) % 1000000
        sniSource.connectSource(root.sniListCmd + " #" + root._pollSeq)
    }

    function runCmd(cmd) {
        execSource.connectSource(cmd)
    }

    Component.onCompleted: {
        updateClock()
        refreshSni()
    }

    Timer {
        interval: 2000
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
            disconnectSource(source)
            let out = (data["stdout"] || "").trim()
            if (out === "") return
            try {
                let parsed = JSON.parse(out)
                let same = (parsed.length === sniAppsModel.count)
                if (same) {
                    for (let k = 0; k < parsed.length; ++k) {
                        let cur = sniAppsModel.get(k)
                        if (cur.sniService !== parsed[k].service || cur.sniIcon !== parsed[k].icon || cur.sniId !== parsed[k].id) {
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
            text: "Adjust Date/Time"
            icon.name: "preferences-system-time"
            onTriggered: root.runCmd("kcmshell6 kcm_clock")
        },
        PlasmaCore.Action {
            text: "Customize Notifications..."
            icon.name: "preferences-desktop-notification"
            onTriggered: root.runCmd("kcmshell6 kcm_notifications")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Show the Desktop"
            icon.name: "user-desktop"
            onTriggered: root.runCmd("if [ \"$(qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showingDesktop)\" = \"true\" ]; then qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop false; else qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop true; fi")
        },
        PlasmaCore.Action {
            text: "Task Manager"
            icon.name: "utilities-system-monitor"
            onTriggered: root.runCmd("python3 \"$HOME/.local/share/xp-startknop/xp-verkenner.py\" taakbeheer")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Properties (Taskbar, Start Menu & Logon)"
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

        readonly property int iconSz: Math.max(16, Math.min(22, Math.round(height * 0.53)))
        readonly property int contentWidth: Math.max(120, trayRow.implicitWidth + 24)

        Layout.minimumWidth: contentWidth
        Layout.preferredWidth: contentWidth
        Layout.maximumWidth: contentWidth
        Layout.fillHeight: true

        // Het Systeemvak (Notification Area): Lichtblauw XP Luna OF Klassiek Grijs 3D verzonken
        Rectangle {
            anchors.fill: parent
            y: root.isClassicTaskbar ? 3 : 0
            height: root.isClassicTaskbar ? (parent.height - 5) : parent.height
            color: root.isClassicTaskbar ? "#d4d0c8" : "#0f85e4"

            // Alleen in XP Luna-modus: de blauwe glans-gradient
            Rectangle {
                anchors.fill: parent
                visible: !root.isClassicTaskbar
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#1aa9f8" }
                    GradientStop { position: 0.08; color: "#0d84e3" }
                    GradientStop { position: 0.22; color: "#1597ef" }
                    GradientStop { position: 0.82; color: "#0f85e4" }
                    GradientStop { position: 1.0; color: "#0a69c2" }
                }
            }

            // Klassieke 3D verzonken randen wanneer Classic-modus actief is
            Rectangle {
                visible: root.isClassicTaskbar
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
                height: 1; color: "#808080"
            }
            Rectangle {
                visible: root.isClassicTaskbar
                anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left
                width: 1; color: "#808080"
            }
            Rectangle {
                visible: root.isClassicTaskbar
                anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right
                height: 1; color: "#ffffff"
            }
            Rectangle {
                visible: root.isClassicTaskbar
                anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.right: parent.right
                width: 1; color: "#ffffff"
            }

            // Lichtblauwe bovenste highlight-lijn (XP Luna)
            Rectangle {
                visible: !root.isClassicTaskbar
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: 2
                color: "#38b6ff"
                opacity: 0.85
            }

            // Linker 3D scheidingsrand tussen donkerblauwe taakbalk en lichtblauw systeemvak (XP Luna)
            Rectangle {
                visible: !root.isClassicTaskbar
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
                visible: !root.isClassicTaskbar
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
                radius: root.isClassicTaskbar ? 2 : 9
                border.color: root.isClassicTaskbar ? "#404040" : "#093c8c"
                border.width: 1
                color: root.isClassicTaskbar ? "#d4d0c8" : "#1682e8"

                Rectangle {
                    anchors.fill: parent
                    radius: parent.radius
                    visible: !root.isClassicTaskbar
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: chevronMouse.containsMouse ? "#7cd2ff" : "#5cbcff" }
                        GradientStop { position: 0.5; color: chevronMouse.containsMouse ? "#2894f4" : "#1682e8" }
                        GradientStop { position: 1.0; color: "#0a58b8" }
                    }
                }

                Text {
                    anchors.centerIn: parent
                    text: root.expanded ? "›" : "‹"
                    color: root.isClassicTaskbar ? "#000000" : "white"
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

                    Item {
                        width: trayItem.iconSz; height: trayItem.iconSz
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

                    Item {
                        width: trayItem.iconSz; height: trayItem.iconSz
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

                    Item {
                        width: trayItem.iconSz; height: trayItem.iconSz
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

                        width: trayItem.iconSz
                        height: trayItem.iconSz
                        anchors.verticalCenter: parent.verticalCenter

                        Image {
                            anchors.fill: parent
                            visible: sniIcon.startsWith("file://")
                            source: sniIcon.startsWith("file://") ? sniIcon : ""
                            sourceSize.width: 32
                            sourceSize.height: 32
                            smooth: true
                            cache: false
                        }

                        Kirigami.Icon {
                            anchors.fill: parent
                            visible: !sniIcon.startsWith("file://")
                            source: !sniIcon.startsWith("file://") ? sniIcon : ""
                            fallback: "application-x-executable"
                        }

                        PlasmaCore.ToolTipArea {
                            anchors.fill: parent
                            mainText: sniTitle
                            subText: "Click to open, right-click for options"
                        }

                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton | Qt.RightButton
                            onClicked: mouse => {
                                if (mouse.button === Qt.RightButton) {
                                    root.runCmd("env GDK_BACKEND=x11 python3 '" + root.xpScript + "' sni-menu '" + sniService + "' '" + sniPath + "' '" + sniMenu + "'")
                                } else {
                                    root.runCmd("python3 '" + root.xpScript + "' sni-activate '" + sniService + "' '" + sniPath + "' '" + sniMenu + "'")
                                }
                            }
                        }
                    }
                }

                // 1. Netwerkverbinding
                Item {
                    width: trayItem.iconSz; height: trayItem.iconSz
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/tray-net.svg")
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "Local Area Connection"
                        subText: "Connected"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.runCmd("kcmshell6 kcm_networkmanagement")
                    }
                }

                // 2. Windows XP Beveiligingscentrum Schildje
                Item {
                    width: trayItem.iconSz; height: trayItem.iconSz
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/xp-shield.svg")
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "Windows XP Security Center"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: root.runCmd("python3 '" + root.xpScript + "' configuratiescherm")
                    }
                }

                // 3. Volume / Geluid
                Item {
                    width: trayItem.iconSz; height: trayItem.iconSz
                    anchors.verticalCenter: parent.verticalCenter
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/" + (root.muted ? "tray-muted.svg" : "tray-audio.svg"))
                        sourceSize.width: 32; sourceSize.height: 32
                    }
                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: "Volume"
                        subText: "Scroll to adjust volume"
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

                // 4. Klok (indien ingeschakeld in XP Eigenschappen)
                Item {
                    visible: root.showClockSetting
                    width: clockText.implicitWidth + 8
                    height: 22
                    anchors.verticalCenter: parent.verticalCenter

                    Text {
                        id: clockText
                        anchors.centerIn: parent
                        text: root.timeString
                        color: root.isClassicTaskbar ? "#000000" : "white"
                        renderType: Text.NativeRendering
                        font.family: "Tahoma"
                        font.pixelSize: Math.max(12, Math.min(14, Math.round(trayItem.height * 0.38)))
                    }

                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: root.dateString
                        subText: "Click to open Date and Time Properties"
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
