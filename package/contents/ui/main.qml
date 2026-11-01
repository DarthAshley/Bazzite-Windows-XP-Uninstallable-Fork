import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.private.kicker as Kicker
import org.kde.plasma.plasma5support as P5Support

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
        // Zoek het programma in favorieten of meest gebruikt en start het
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
            text: "Verkennen (Deze computer)"
            icon.name: "computer"
            onTriggered: root.runCmd("python3 \"$HOME/.local/share/xp-startknop/xp-verkenner.py\" computer")
        },
        PlasmaCore.Action {
            text: "Zoeken..."
            icon.name: "edit-find"
            onTriggered: root.runCmd("krunner")
        },
        PlasmaCore.Action {
            isSeparator: true
        },
        PlasmaCore.Action {
            text: "Het bureaublad weergeven"
            icon.name: "user-desktop"
            onTriggered: root.runCmd(root.toggleDesktopCmd)
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

        // De paneelachtergrond houdt links 9 pixels vrij; de knop moet in de hoek zitten
        readonly property int panelMargin: 9
        readonly property int startBtnWidth: Math.round(height * 97 / 30) - panelMargin
        readonly property bool showQL: Plasmoid.configuration.showQuickLaunch !== false
        readonly property int qlWidth: showQL ? (quickLaunchRow.implicitWidth + 10) : 0

        Layout.minimumWidth: startBtnWidth + qlWidth
        Layout.preferredWidth: startBtnWidth + qlWidth
        Layout.maximumWidth: startBtnWidth + qlWidth
        Layout.fillHeight: true

        Component.onCompleted: startMenu.visualParent = button

        // De groene Windows XP Start-knop helemaal links in de hoek
        Item {
            id: startBtnBox
            x: -button.panelMargin
            width: button.startBtnWidth + button.panelMargin
            height: button.height

            Repeater {
                model: ["start-normaal.png", "start-zweven.png", "start-ingedrukt.png"]
                Image {
                    anchors.fill: parent
                    source: Qt.resolvedUrl("../images/" + modelData)
                    smooth: true
                    visible: button.frame === index
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
                width: 23
                height: 23
                radius: 2
                anchors.verticalCenter: parent.verticalCenter
                color: sdMouse.pressed ? "#184ea8" : (sdMouse.containsMouse ? "#3880eb" : "transparent")
                border.color: sdMouse.pressed ? "#0c3278" : (sdMouse.containsMouse ? "#72b2ff" : "transparent")
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: 17
                    height: 17
                    source: Qt.resolvedUrl("../images/icons/show-desktop.svg")
                    sourceSize.width: 34
                    sourceSize.height: 34
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Bureaublad weergeven"
                    subText: "Alle vensters minimaliseren of herstellen"
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
                width: 23
                height: 23
                radius: 2
                anchors.verticalCenter: parent.verticalCenter
                color: ffMouse.pressed ? "#184ea8" : (ffMouse.containsMouse ? "#3880eb" : "transparent")
                border.color: ffMouse.pressed ? "#0c3278" : (ffMouse.containsMouse ? "#72b2ff" : "transparent")
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: 17
                    height: 17
                    source: Qt.resolvedUrl("../images/icons/firefox.svg")
                    sourceSize.width: 34
                    sourceSize.height: 34
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Mozilla Firefox"
                    subText: "Op het internet surfen"
                }

                MouseArea {
                    id: ffMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.runCmd("firefox || xdg-open https://www.google.nl")
                }
            }

            // 3. Snelkoppeling: Windows Verkenner (Dolphin)
            Rectangle {
                width: 23
                height: 23
                radius: 2
                anchors.verticalCenter: parent.verticalCenter
                color: exMouse.pressed ? "#184ea8" : (exMouse.containsMouse ? "#3880eb" : "transparent")
                border.color: exMouse.pressed ? "#0c3278" : (exMouse.containsMouse ? "#72b2ff" : "transparent")
                border.width: 1

                Image {
                    anchors.centerIn: parent
                    width: 17
                    height: 17
                    source: Qt.resolvedUrl("../images/icons/folder.svg")
                    sourceSize.width: 34
                    sourceSize.height: 34
                    smooth: true
                }

                PlasmaCore.ToolTipArea {
                    anchors.fill: parent
                    mainText: "Windows Verkenner (Dolphin)"
                    subText: "Mappen en bestanden weergeven"
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

                    width: 23
                    height: 23
                    radius: 2
                    anchors.verticalCenter: parent.verticalCenter
                    color: qlItemMouse.pressed ? "#184ea8" : (qlItemMouse.containsMouse ? "#3880eb" : "transparent")
                    border.color: qlItemMouse.pressed ? "#0c3278" : (qlItemMouse.containsMouse ? "#72b2ff" : "transparent")
                    border.width: 1

                    Kirigami.Icon {
                        anchors.centerIn: parent
                        width: 17
                        height: 17
                        source: itemIcon
                    }

                    PlasmaCore.ToolTipArea {
                        anchors.fill: parent
                        mainText: itemTitle
                        subText: "Klik om te starten, middelklik om te verwijderen uit Snel starten"
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

            // Authentieke 3D verticale Windows XP scheidingslijn achter Snel starten
            Item {
                width: 6
                height: 20
                anchors.verticalCenter: parent.verticalCenter

                Rectangle {
                    x: 2
                    y: 1
                    width: 1
                    height: 18
                    color: "#103f91"
                }
                Rectangle {
                    x: 3
                    y: 1
                    width: 1
                    height: 18
                    color: "#4a90f0"
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
