import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.private.kicker as Kicker
import org.kde.plasma.plasma5support as P5Support
import "xpConfig.js" as XpConfig

PlasmoidItem {
    id: root

    property double lastHidden: 0
    readonly property string toggleDesktopCmd: "if [ \"$(qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showingDesktop)\" = \"true\" ]; then qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop false; else qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDesktop true; fi"

    function toggleMenu() {
        if (startMenu.visible) {
            startMenu.visible = false
        } else if (Date.now() - lastHidden > 250) {
            startMenu.visible = true
            startMenu.requestActivate()
        }
    }

    function runCmd(cmd) {
        extLauncher.connectSource(cmd)
    }

    function triggerQuickLaunchApp(appName) {
        let favModel = kickerModel.favoritesModel
        if (favModel) {
            for (let i = 0; i < favModel.count; ++i) {
                let idx = favModel.index(i, 0)
                let nm = (favModel.data(idx, Qt.DisplayRole) || "").toString().trim()
                if (nm === appName) {
                    favModel.trigger(i, "", null)
                    return
                }
            }
        }
        for (let j = 0; j < kickerUsage.count; ++j) {
            let idx2 = kickerUsage.index(j, 0)
            let nm2 = (kickerUsage.data(idx2, Qt.DisplayRole) || "").toString().trim()
            if (nm2 === appName) {
                kickerUsage.trigger(j, "", null)
                return
            }
        }
        root.runCmd("kioclient6 exec $(grep -ril 'Name=" + appName + "' \"$HOME/.local/share/applications\" /usr/share/applications /var/lib/flatpak/exports/share/applications 2>/dev/null | head -n1)")
    }

    function removeExtraQuickLaunch(idx) {
        let cur = Plasmoid.configuration.quickLaunchExtra || []
        let next = []
        for (let i = 0; i < cur.length; ++i) {
            if (i !== idx) next.push(cur[i])
        }
        Plasmoid.configuration.quickLaunchExtra = next
    }

    P5Support.DataSource {
        id: extLauncher
        engine: "executable"
        onNewData: source => disconnectSource(source)
    }

    Plasmoid.contextualActions: [
        PlasmaCore.Action {
            text: "Explore (My Computer)"
            icon.name: "computer"
            onTriggered: root.runCmd("python3 \"$HOME/.local/share/xp-startknop/xp-verkenner.py\" computer")
        },
        PlasmaCore.Action {
            text: "Search..."
            icon.name: "edit-find"
            onTriggered: root.runCmd("krunner")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Show the Desktop"
            icon.name: "user-desktop"
            onTriggered: root.runCmd(root.toggleDesktopCmd)
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
    Plasmoid.status: startMenu.visible ? PlasmaCore.Types.RequiresAttentionStatus : PlasmaCore.Types.PassiveStatus
    Plasmoid.onActivated: toggleMenu()

    Kicker.RootModel {
        id: kickerModel
        appletInterface: root
        autoPopulate: false
        appNameFormat: 0
        flat: true
        sorted: true
        showSeparators: false
        showAllApps: true
        showAllAppsCategorized: false
        showRecentApps: false
        showRecentDocs: false
        showPowerSession: false
        showFavoritesPlaceholder: false

        Component.onCompleted: {
            favoritesModel.initForClient("org.kde.plasma.kickoff.favorites.instance-445")
            refresh()
        }
    }

    Kicker.RootModel {
        id: kickerCatModel
        appletInterface: root
        autoPopulate: false
        appNameFormat: 0
        flat: true
        sorted: true
        showSeparators: false
        showAllApps: false
        showAllAppsCategorized: false
        showRecentApps: false
        showRecentDocs: false
        showPowerSession: false
        showFavoritesPlaceholder: false

        Component.onCompleted: {
            refresh()
        }
    }

    Kicker.RecentUsageModel {
        id: kickerUsage
        ordering: Kicker.RecentUsageModel.Popular
        shownItems: Kicker.RecentUsageModel.OnlyApps
    }

    Kicker.RecentUsageModel {
        id: kickerRecentDocs
        ordering: Kicker.RecentUsageModel.Recent
        shownItems: Kicker.RecentUsageModel.OnlyDocs
    }

    compactRepresentation: null

    fullRepresentation: Item {
        id: button

        readonly property int frame: mouse.pressed || startMenu.visible ? 2 : (mouse.containsMouse ? 1 : 0)
        readonly property string effectiveTaskbarStyle: (Plasmoid.configuration.taskbarStyle && Plasmoid.configuration.taskbarStyle !== "")
            ? Plasmoid.configuration.taskbarStyle
            : (XpConfig.taskbarStyle || "xp")
        readonly property bool isClassicTaskbar: effectiveTaskbarStyle === "classic"

        // De paneelachtergrond houdt links 9 pixels vrij; de knop moet in de hoek zitten
        readonly property int panelMargin: 9
        readonly property int startBtnWidth: isClassicTaskbar
            ? Math.max(62, Math.round(height * 2.35)) - panelMargin
            : Math.round(height * 97 / 30) - panelMargin
        readonly property bool showQL: (Plasmoid.configuration.showQuickLaunch !== false) && (XpConfig.showQuickLaunch !== false)
        readonly property int qlBtnSize: Math.max(23, Math.min(36, height - 7))
        readonly property int qlIconSize: Math.max(17, Math.min(28, height - 13))
        readonly property int qlWidth: showQL ? (quickLaunchRow.implicitWidth + 10) : 0

        Layout.minimumWidth: startBtnWidth + qlWidth
        Layout.preferredWidth: startBtnWidth + qlWidth
        Layout.maximumWidth: startBtnWidth + qlWidth
        Layout.fillHeight: true

        Component.onCompleted: startMenu.visualParent = button

        // Als Classic Taakbalk-modus actief is: teken ook het klassieke #d4d0c8 paneelvlak achter Start & Snel starten
        Rectangle {
            visible: button.isClassicTaskbar
            x: -button.panelMargin
            y: 0
            width: button.width + button.panelMargin + 2000
            height: button.height
            color: "#d4d0c8"
            z: -2

            Rectangle {
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
                height: 1; color: "#ffffff"
            }
            Rectangle {
                anchors.top: parent.top; anchors.topMargin: 1; anchors.left: parent.left; anchors.right: parent.right
                height: 1; color: "#dfdfdf"
            }
        }

        // De Start-knop helemaal links in de hoek (Windows XP Groen OF Klassiek Grijs 3D)
        Item {
            id: startBtnBox
            x: -button.panelMargin
            width: button.startBtnWidth + button.panelMargin
            height: button.height

            // 1. Windows XP Luna Groene Startknop
            Item {
                anchors.fill: parent
                visible: !button.isClassicTaskbar

                Repeater {
                    model: ["start-normaal.png", "start-zweven.png", "start-ingedrukt.png"]
                    Image {
                        anchors.fill: parent
                        source: Qt.resolvedUrl("../images/" + modelData)
                        smooth: true
                        visible: button.frame === index
                    }
                }
            }

            // 2. Klassieke Windows Startknop (3D grijs #d4d0c8 met 4-kleuren vlaggetje en vette "Start")
            Rectangle {
                anchors.fill: parent
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.topMargin: 3
                anchors.bottomMargin: 3
                visible: button.isClassicTaskbar
                color: "#d4d0c8"

                readonly property bool sunken: button.frame === 2

                // Buitenste 3D rand
                Rectangle {
                    anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
                    height: 1; color: parent.sunken ? "#404040" : "#ffffff"
                }
                Rectangle {
                    anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left
                    width: 1; color: parent.sunken ? "#404040" : "#ffffff"
                }
                Rectangle {
                    anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right
                    height: 1; color: parent.sunken ? "#ffffff" : "#404040"
                }
                Rectangle {
                    anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.right: parent.right
                    width: 1; color: parent.sunken ? "#ffffff" : "#404040"
                }

                // Binnenste 3D rand
                Rectangle {
                    anchors.top: parent.top; anchors.topMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1
                    height: 1; color: parent.sunken ? "#808080" : "#dfdfdf"
                }
                Rectangle {
                    anchors.top: parent.top; anchors.topMargin: 1; anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1
                    width: 1; color: parent.sunken ? "#808080" : "#dfdfdf"
                }
                Rectangle {
                    anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1
                    height: 1; color: parent.sunken ? "#dfdfdf" : "#808080"
                }
                Rectangle {
                    anchors.top: parent.top; anchors.topMargin: 1; anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1
                    width: 1; color: parent.sunken ? "#dfdfdf" : "#808080"
                }

                Row {
                    anchors.centerIn: parent
                    anchors.horizontalCenterOffset: parent.sunken ? 1 : 0
                    anchors.verticalCenterOffset: parent.sunken ? 1 : 0
                    spacing: 4

                    // Klassiek 4-kleuren Windows-icoontje
                    Grid {
                        anchors.verticalCenter: parent.verticalCenter
                        columns: 2
                        spacing: 1
                        Rectangle { width: Math.max(6, Math.round(button.height * 0.20)); height: width; color: "#ff3300"; border.color: "#801800"; border.width: 1 }
                        Rectangle { width: Math.max(6, Math.round(button.height * 0.20)); height: width; color: "#33cc33"; border.color: "#146614"; border.width: 1 }
                        Rectangle { width: Math.max(6, Math.round(button.height * 0.20)); height: width; color: "#0066ff"; border.color: "#002b80"; border.width: 1 }
                        Rectangle { width: Math.max(6, Math.round(button.height * 0.20)); height: width; color: "#ffcc00"; border.color: "#806600"; border.width: 1 }
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Start"
                        color: "#000000"
                        font.family: "Tahoma"
                        font.pixelSize: Math.max(11, Math.min(16, Math.round(button.height * 0.40)))
                        font.bold: true
                        renderType: Text.NativeRendering
                    }
                }
            }

            MouseArea {
                id: mouse
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.LeftButton
                onClicked: root.toggleMenu()
            }
        }

        // === WINDOWS XP WERKBALK SNEL STARTEN (Quick Launch) RECHTS NAAST DE START-KNOP ===
        Row {
            id: quickLaunchRow
            visible: button.showQL
            x: button.startBtnWidth + 4
            anchors.verticalCenter: parent.verticalCenter
            spacing: 2

            // 1. Bureaublad weergeven (Show Desktop)
            Rectangle {
                width: button.qlBtnSize
                height: button.qlBtnSize
                radius: button.isClassicTaskbar ? 0 : 2
                anchors.verticalCenter: parent.verticalCenter
                color: button.isClassicTaskbar
                    ? (sdMouse.pressed ? "#c6c2ba" : "transparent")
                    : (sdMouse.pressed ? "#184ea8" : (sdMouse.containsMouse ? "#3880eb" : "transparent"))
                border.color: button.isClassicTaskbar
                    ? (sdMouse.containsMouse || sdMouse.pressed ? "#808080" : "transparent")
                    : (sdMouse.pressed ? "#0c3278" : (sdMouse.containsMouse ? "#72b2ff" : "transparent"))
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: button.qlIconSize
                    height: button.qlIconSize
                    source: Qt.resolvedUrl("../images/icons/show-desktop.svg")
                    sourceSize.width: button.qlIconSize * 2
                    sourceSize.height: button.qlIconSize * 2
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Show Desktop"
                    subText: "Minimize or restore all open windows"
                }

                MouseArea {
                    id: sdMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.runCmd(root.toggleDesktopCmd)
                }
            }

            // 2. Snelkoppeling: Mozilla Firefox
            Rectangle {
                width: button.qlBtnSize
                height: button.qlBtnSize
                radius: button.isClassicTaskbar ? 0 : 2
                anchors.verticalCenter: parent.verticalCenter
                color: button.isClassicTaskbar
                    ? (ffMouse.pressed ? "#c6c2ba" : "transparent")
                    : (ffMouse.pressed ? "#184ea8" : (ffMouse.containsMouse ? "#3880eb" : "transparent"))
                border.color: button.isClassicTaskbar
                    ? (ffMouse.containsMouse || ffMouse.pressed ? "#808080" : "transparent")
                    : (ffMouse.pressed ? "#0c3278" : (ffMouse.containsMouse ? "#72b2ff" : "transparent"))
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: button.qlIconSize
                    height: button.qlIconSize
                    source: Qt.resolvedUrl("../images/icons/firefox.svg")
                    sourceSize.width: button.qlIconSize * 2
                    sourceSize.height: button.qlIconSize * 2
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Mozilla Firefox"
                    subText: "Browse the Internet"
                }

                MouseArea {
                    id: ffMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.runCmd("firefox || xdg-open https://www.google.com")
                }
            }

            // 3. Snelkoppeling: Windows Verkenner (Dolphin)
            Rectangle {
                width: button.qlBtnSize
                height: button.qlBtnSize
                radius: button.isClassicTaskbar ? 0 : 2
                anchors.verticalCenter: parent.verticalCenter
                color: button.isClassicTaskbar
                    ? (exMouse.pressed ? "#c6c2ba" : "transparent")
                    : (exMouse.pressed ? "#184ea8" : (exMouse.containsMouse ? "#3880eb" : "transparent"))
                border.color: button.isClassicTaskbar
                    ? (exMouse.containsMouse || exMouse.pressed ? "#808080" : "transparent")
                    : (exMouse.pressed ? "#0c3278" : (exMouse.containsMouse ? "#72b2ff" : "transparent"))
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: button.qlIconSize
                    height: button.qlIconSize
                    source: Qt.resolvedUrl("../images/icons/folder.svg")
                    sourceSize.width: button.qlIconSize * 2
                    sourceSize.height: button.qlIconSize * 2
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Windows Explorer (Dolphin)"
                    subText: "Display the files and folders on your computer"
                }

                MouseArea {
                    id: exMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.runCmd("dolphin \"$HOME\"")
                }
            }

            // Extra door de gebruiker toegevoegde Snel starten-snelkoppelingen (via rechtermuisknop in Startmenu)
            Repeater {
                model: Plasmoid.configuration.quickLaunchExtra || []
                delegate: Rectangle {
                    required property int index
                    required property string modelData

                    readonly property var parts: modelData.split("|")
                    readonly property string itemTitle: parts.length > 0 ? parts[0] : ""
                    readonly property string itemIcon: parts.length > 1 ? parts[1] : "application-x-executable"

                    width: button.qlBtnSize
                    height: button.qlBtnSize
                    radius: button.isClassicTaskbar ? 0 : 2
                    anchors.verticalCenter: parent.verticalCenter
                    color: button.isClassicTaskbar
                        ? (qlItemMouse.pressed ? "#c6c2ba" : "transparent")
                        : (qlItemMouse.pressed ? "#184ea8" : (qlItemMouse.containsMouse ? "#3880eb" : "transparent"))
                    border.color: button.isClassicTaskbar
                        ? (qlItemMouse.containsMouse || qlItemMouse.pressed ? "#808080" : "transparent")
                        : (qlItemMouse.pressed ? "#0c3278" : (qlItemMouse.containsMouse ? "#72b2ff" : "transparent"))
                    border.width: 1

                    Kirigami.Icon {
                        anchors.centerIn: parent
                        width: button.qlIconSize
                        height: button.qlIconSize
                        source: itemIcon
                    }

                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: itemTitle
                        subText: "Click to launch, middle-click to remove from Quick Launch"
                    }

                    MouseArea {
                        id: qlItemMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.LeftButton | Qt.MiddleButton
                        onClicked: mouse => {
                            if (mouse.button === Qt.MiddleButton) {
                                root.removeExtraQuickLaunch(index)
                            } else {
                                root.triggerQuickLaunchApp(itemTitle)
                            }
                        }
                    }
                }
            }

            // Authentieke 3D verticale Windows XP / Classic scheidingslijn achter Snel starten
            Item {
                width: 6
                height: Math.max(20, button.height - 8)
                anchors.verticalCenter: parent.verticalCenter

                Rectangle {
                    x: 2
                    y: 1
                    width: 1
                    height: parent.height - 2
                    color: button.isClassicTaskbar ? "#808080" : "#103f91"
                }
                Rectangle {
                    x: 3
                    y: 1
                    width: 1
                    height: parent.height - 2
                    color: button.isClassicTaskbar ? "#ffffff" : "#4a90f0"
                    opacity: 0.85
                }
            }
        }
    }

    PlasmaCore.Dialog {
        id: startMenu

        flags: Qt.WindowStaysOnTopHint
        location: Plasmoid.location
        hideOnWindowDeactivate: true
        backgroundHints: PlasmaCore.Dialog.NoBackground

        onVisibleChanged: {
            if (visible) {
                menuView.reset()
            } else {
                root.lastHidden = Date.now()
            }
        }

        mainItem: StartMenu {
            id: menuView
            rootModel: kickerModel
            catRootModel: kickerCatModel
            usageModel: kickerUsage
            recentDocsModel: kickerRecentDocs
            onCloseRequested: startMenu.visible = false
            Keys.onEscapePressed: startMenu.visible = false
        }
    }
}
