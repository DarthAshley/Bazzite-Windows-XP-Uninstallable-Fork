import QtCore
import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts
import org.kde.coreaddons as KCoreAddons
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.plasma5support as P5Support
import org.kde.plasma.private.sessions as Sessions
import "xpConfig.js" as XpConfig

Item {
    id: menu

    required property var rootModel
    required property var catRootModel
    required property var usageModel
    required property var recentDocsModel

    readonly property string effectiveStartStyle: (Plasmoid.configuration.startMenuStyle && Plasmoid.configuration.startMenuStyle !== "")
        ? Plasmoid.configuration.startMenuStyle
        : (XpConfig.startMenuStyle || "xp")
    readonly property bool isClassicStart: effectiveStartStyle === "classic"

    readonly property string effectiveIconSize: (Plasmoid.configuration.startIconSize && Plasmoid.configuration.startIconSize !== "")
        ? Plasmoid.configuration.startIconSize
        : (XpConfig.startIconSize || "large")
    readonly property bool isSmallIcons: effectiveIconSize === "small"

    readonly property string effectiveItemsMode: (Plasmoid.configuration.startItemsMode && Plasmoid.configuration.startItemsMode !== "")
        ? Plasmoid.configuration.startItemsMode
        : (XpConfig.startItemsMode || "both")

    readonly property int effectiveItemsCount: (Plasmoid.configuration.startItemsCount > 0)
        ? Plasmoid.configuration.startItemsCount
        : (XpConfig.startItemsCount || 0)

    property int menuWidth: Plasmoid.configuration.menuWidth > 390 ? Plasmoid.configuration.menuWidth : 430
    property int menuHeight: Plasmoid.configuration.menuHeight > 400 ? Plasmoid.configuration.menuHeight : 535

    property bool allPrograms: false
    property bool showRecentDocs: false
    property int activeCategoryIndex: -1
    property string activeBuiltinFolder: ""
    property string activeSubFolder: ""
    property real col2TargetY: 160
    property real col3TargetY: 160
    property double allProgramsOpenedAt: 0

    // Timers zodat Alle programma's en submenu's NOOIT per ongeluk sluiten tijdens muisbewegingen
    Timer {
        id: closeAllProgsTimer
        interval: 500
        repeat: false
        onTriggered: {
            if (!allHover.containsMouse && !col1Blocker.containsMouse && !col2Blocker.containsMouse && !col3Blocker.containsMouse) {
                menu.allPrograms = false
                menu.activeCategoryIndex = -1
                menu.activeBuiltinFolder = ""
                menu.activeSubFolder = ""
            }
        }
    }

    Timer {
        id: col2SwitchTimer
        interval: 220
        repeat: false
        property int nextCatIndex: -1
        property string nextBuiltin: ""
        property real nextY: 160
        onTriggered: {
            if (!col2Blocker.containsMouse && !col3Blocker.containsMouse) {
                menu.col2TargetY = nextY
                menu.activeCategoryIndex = nextCatIndex
                menu.activeBuiltinFolder = nextBuiltin
                menu.activeSubFolder = ""
            }
        }
    }

    function requestCol2Change(catIdx, builtinName, targetY) {
        closeAllProgsTimer.stop()
        // Als er nog geen submenu open staat, open direct zonder vertraging
        if (menu.activeCategoryIndex === -1 && menu.activeBuiltinFolder === "") {
            menu.col2TargetY = targetY
            menu.activeCategoryIndex = catIdx
            menu.activeBuiltinFolder = builtinName
            menu.activeSubFolder = ""
            col2SwitchTimer.stop()
        } else {
            col2SwitchTimer.nextCatIndex = catIdx
            col2SwitchTimer.nextBuiltin = builtinName
            col2SwitchTimer.nextY = targetY
            col2SwitchTimer.restart()
        }
    }

    function scheduleCloseAllPrograms() {
        if (menu.allPrograms) {
            closeAllProgsTimer.restart()
        }
    }

    property var removedList: Plasmoid.configuration.removedItems || []
    property var pinnedList: Plasmoid.configuration.pinnedItems || []

    readonly property var allAppsModel: rootModel.count > 0 ? rootModel.modelForRow(0) : null
    readonly property string xpScript: (StandardPaths.writableLocation(StandardPaths.GenericDataLocation) + "/xp-startknop/xp-verkenner.py").replace(/^file:\/\//, "")

    signal closeRequested()

    function reset() {
        closeAllProgsTimer.stop()
        col2SwitchTimer.stop()
        allPrograms = false
        showRecentDocs = false
        activeCategoryIndex = -1
        activeBuiltinFolder = ""
        activeSubFolder = ""
        ctxMenu.visible = false
        usageModel.refresh()
        recentDocsModel.refresh()
        removedList = Plasmoid.configuration.removedItems || []
        pinnedList = Plasmoid.configuration.pinnedItems || []
        rebuildLeftItems()
        forceActiveFocus()
    }

    function openFolder(location) {
        Qt.openUrlExternally(location)
        closeRequested()
    }

    function run(command) {
        launcher.connectSource(command)
        closeRequested()
    }

    function runXpMode(mode) {
        run("python3 '" + xpScript + "' " + mode)
    }

    function isRemoved(name) {
        if (!name) return false
        for (let i = 0; i < removedList.length; ++i) {
            if (removedList[i] === name) return true
        }
        return false
    }

    function isPinned(name) {
        if (!name) return false
        for (let i = 0; i < pinnedList.length; ++i) {
            if (pinnedList[i] === name) return true
        }
        return false
    }

    function removeItemFromList(name) {
        if (!name) return
        let arr = []
        for (let i = 0; i < removedList.length; ++i) {
            if (removedList[i] !== name) arr.push(removedList[i])
        }
        arr.push(name)
        removedList = arr
        Plasmoid.configuration.removedItems = arr
        rebuildLeftItems()
    }

    function togglePinItem(name) {
        if (!name) return
        let arr = []
        let found = false
        for (let i = 0; i < pinnedList.length; ++i) {
            if (pinnedList[i] === name) {
                found = true
            } else {
                arr.push(pinnedList[i])
            }
        }
        if (!found) arr.push(name)
        pinnedList = arr
        Plasmoid.configuration.pinnedItems = arr
        rebuildLeftItems()
    }

    function restoreRemovedItems() {
        removedList = []
        Plasmoid.configuration.removedItems = []
        rebuildLeftItems()
    }

    function isInQuickLaunch(name) {
        if (!name) return false
        let ql = Plasmoid.configuration.quickLaunchExtra || []
        for (let i = 0; i < ql.length; ++i) {
            if (ql[i].split("|")[0] === name) return true
        }
        return false
    }

    function toggleQuickLaunch(name) {
        if (!name) return
        let ql = Plasmoid.configuration.quickLaunchExtra || []
        let next = []
        let found = false
        for (let i = 0; i < ql.length; ++i) {
            if (ql[i].split("|")[0] === name) {
                found = true
            } else {
                next.push(ql[i])
            }
        }
        if (!found) {
            let ic = "application-x-executable"
            for (let k = 0; k < leftAppsModel.count; ++k) {
                let it = leftAppsModel.get(k)
                if (it.appTitle === name) {
                    ic = it.iconName
                    break
                }
            }
            next.push(name + "|" + ic)
        }
        Plasmoid.configuration.quickLaunchExtra = next
    }

    function resetMenuSize() {
        menuWidth = 430
        menuHeight = 535
        Plasmoid.configuration.menuWidth = 430
        Plasmoid.configuration.menuHeight = 535
        rebuildLeftItems()
    }

    Connections {
        target: menu.usageModel
        function onCountChanged() {
            menu.rebuildLeftItems()
        }
    }

    ListModel {
        id: leftAppsModel
    }

    function rebuildLeftItems() {
        leftAppsModel.clear()
        let rowH = menu.isSmallIcons ? 26 : 38
        let availHeight = menu.menuHeight - 60 - 2 - 42 - 96 - 16 - 36
        let autoSlots = Math.max(4, Math.floor(availHeight / rowH))
        let maxSlots = (menu.effectiveItemsCount > 0) ? Math.min(autoSlots, menu.effectiveItemsCount) : autoSlots
        let seen = {}
        let mode = menu.effectiveItemsMode

        // Modus: Vaste eigen lijst ("custom")
        if (mode === "custom") {
            let customArr = (Plasmoid.configuration.customItemsList && Plasmoid.configuration.customItemsList.length > 0)
                ? Plasmoid.configuration.customItemsList
                : (XpConfig.customItems || [])
            for (let c = 0; c < customArr.length && leftAppsModel.count < maxSlots; ++c) {
                let parts = (customArr[c] || "").split("|")
                let cTitle = (parts[0] || "").trim()
                let cIcon = (parts[1] || "application-x-executable").trim()
                let cCmd = (parts[2] || cTitle.toLowerCase()).trim()
                if (cTitle !== "" && !isRemoved(cTitle)) {
                    leftAppsModel.append({
                        "appTitle": cTitle,
                        "iconName": cIcon,
                        "sourceType": "custom:" + cCmd,
                        "sourceIndex": c
                    })
                }
            }
            return
        }

        // 1. Eerst door de gebruiker vastgemaakte items + favorieten (indien mode === "both" of "favorites")
        let favModel = menu.rootModel ? menu.rootModel.favoritesModel : null
        if (favModel && (mode === "both" || mode === "favorites")) {
            for (let i = 0; i < favModel.count && leftAppsModel.count < maxSlots; ++i) {
                let idx = favModel.index(i, 0)
                let name = (favModel.data(idx, Qt.DisplayRole) || "").toString().trim()
                let iconVal = favModel.data(idx, Qt.DecorationRole) || "application-x-executable"
                let iconStr = iconVal.toString()
                let nameKey = name.toLowerCase()
                if (name !== "" && !seen[nameKey] && !seen[iconStr] && !isRemoved(name)) {
                    seen[nameKey] = true
                    seen[iconStr] = true
                    leftAppsModel.append({
                        "appTitle": name,
                        "iconName": iconStr,
                        "sourceType": "fav",
                        "sourceIndex": i
                    })
                }
            }
        }

        // 2. Aanvullen met meest gebruikte programma's (indien mode === "both" of "recent")
        if (menu.usageModel && (mode === "both" || mode === "recent")) {
            for (let j = 0; j < menu.usageModel.count && leftAppsModel.count < maxSlots; ++j) {
                let idx2 = menu.usageModel.index(j, 0)
                let name2 = (menu.usageModel.data(idx2, Qt.DisplayRole) || "").toString().trim()
                let iconVal2 = menu.usageModel.data(idx2, Qt.DecorationRole) || "application-x-executable"
                let iconStr2 = iconVal2.toString()
                let nameKey2 = name2.toLowerCase()
                if (name2 !== "" && !seen[nameKey2] && !seen[iconStr2] && !isRemoved(name2)) {
                    seen[nameKey2] = true
                    seen[iconStr2] = true
                    leftAppsModel.append({
                        "appTitle": name2,
                        "iconName": iconStr2,
                        "sourceType": "usage",
                        "sourceIndex": j
                    })
                }
            }
        }
    }

    function triggerLeftItem(sourceType, sourceIndex) {
        if (sourceType && sourceType.startsWith("custom:")) {
            let cmd = sourceType.substring(7)
            menu.run(cmd)
        } else if (sourceType === "fav" && menu.rootModel && menu.rootModel.favoritesModel) {
            menu.rootModel.favoritesModel.trigger(sourceIndex, "", null)
            menu.closeRequested()
        } else if (sourceType === "usage" && menu.usageModel) {
            menu.usageModel.trigger(sourceIndex, "", null)
            menu.closeRequested()
        }
    }

    // Vaste canvasbreedte voor uitklapmenu's zodat Wayland het dialoogvenster NOOIT hoeft te resizen (voorkomt focusverlies!)
    readonly property int extraPopupWidth: 640

    width: menuWidth + extraPopupWidth
    height: Math.max(menuHeight, 560)
    implicitWidth: width
    implicitHeight: height
    Layout.minimumWidth: width
    Layout.minimumHeight: height
    Layout.maximumWidth: width
    Layout.maximumHeight: height

    KCoreAddons.KUser { id: user }
    Sessions.SessionManagement { id: session }

    P5Support.DataSource {
        id: launcher
        engine: "executable"
        onNewData: source => disconnectSource(source)
    }

    // Klik in de transparante ruimte rechts/boven het Startmenu sluit eerst open sub-popups of anders het Startmenu zelf
    MouseArea {
        anchors.fill: parent
        onClicked: {
            if (ctxMenu.visible) {
                ctxMenu.visible = false
            } else if (menu.allPrograms || menu.showRecentDocs) {
                menu.allPrograms = false
                menu.showRecentDocs = false
                menu.activeCategoryIndex = -1
                menu.activeBuiltinFolder = ""
                menu.activeSubFolder = ""
            } else {
                menu.closeRequested()
            }
        }
    }

    // Het daadwerkelijke Windows XP Startmenu linksonder (XP Luna modus)
    Item {
        id: startBox
        visible: !menu.isClassicStart
        x: 0
        anchors.bottom: parent.bottom
        width: menu.menuWidth
        height: menu.menuHeight

        // Vang kliks binnen startBox op zodat ze niet doorlekken naar het transparante buitenveld
        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (ctxMenu.visible) ctxMenu.visible = false
            }
        }

        // Blauwe Luna buitenrand
        Rectangle {
            anchors.fill: parent
            topLeftRadius: 7
            topRightRadius: 7
            color: "#1c5ad1"
            border.color: "#0b358c"
            border.width: 1
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 2
            anchors.bottomMargin: 0
            spacing: 0

            // Kop met gebruiker
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                topLeftRadius: 6
                topRightRadius: 6
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#559cf6" }
                    GradientStop { position: 0.05; color: "#1868ce" }
                    GradientStop { position: 0.14; color: "#0e60cb" }
                    GradientStop { position: 0.25; color: "#3a8cf0" }
                    GradientStop { position: 0.78; color: "#2675e0" }
                    GradientStop { position: 1.0; color: "#1b5fce" }
                }

                // Subtiele witte glanslijn bovenaan de kopbalk
                Rectangle {
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 5
                    anchors.rightMargin: 5
                    anchors.topMargin: 1
                    height: 1
                    color: "#8abaf8"
                    opacity: 0.75
                }

                Rectangle {
                    id: avatarFrame
                    x: 8
                    anchors.verticalCenter: parent.verticalCenter
                    width: 48
                    height: 48
                    radius: 3
                    color: "#dfe9f8"
                    border.color: "#f4f7fc"
                    border.width: 2

                    Image {
                        anchors.fill: parent
                        anchors.margins: 2
                        source: user.faceIconUrl
                        visible: status === Image.Ready
                    }
                    Kirigami.Icon {
                        anchors.fill: parent
                        anchors.margins: 4
                        source: "user-identity"
                        visible: user.faceIconUrl.toString() === ""
                    }
                }

                XpText {
                    anchors.left: avatarFrame.right
                    anchors.leftMargin: 10
                    anchors.verticalCenter: parent.verticalCenter
                    text: user.fullName || "King Geoffrey"
                    color: "white"
                    style: Text.Raised
                    styleColor: "#0f3a8c"
                    heavy: true
                    font.pixelSize: 17
                }
            }

            // Oranje gloedlijn onder de kop
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 2
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#2675e0" }
                    GradientStop { position: 0.5; color: "#f59c2f" }
                    GradientStop { position: 1.0; color: "#2675e0" }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 0

                // Linkerkolom (Wit): Vastgepind (Internet + E-mail), Meest gebruikt, Alle programma's
                Rectangle {
                    Layout.preferredWidth: Math.round(menu.menuWidth * 0.485)
                    Layout.fillHeight: true
                    color: "white"

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 0

                        // Vastgepind: Internet & E-mail (zoals in origineel Windows XP)
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 5
                        }

                        AppEntry {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 44
                            visible: !menu.isRemoved("Internet")
                            label: "Internet"
                            subtitle: "Internet Explorer"
                            iconFile: "ie6.svg"
                            iconSize: 32
                            bold: true
                            onHovered: {
                                menu.showRecentDocs = false
                            }
                            onActivated: menu.run("xdg-open https://www.google.nl")
                            onRightClicked: (gx, gy) => {
                                let p = mapToItem(menu, gx, gy)
                                ctxMenu.openForItem(p.x, p.y, "Internet", "cmd", "xdg-open https://www.google.nl", -1)
                            }
                        }

                        AppEntry {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 44
                            visible: !menu.isRemoved("E-mail")
                            label: "E-mail"
                            subtitle: "Outlook Express"
                            iconFile: "outlook.svg"
                            iconSize: 32
                            bold: true
                            onHovered: {
                                menu.showRecentDocs = false
                            }
                            onActivated: menu.run("xdg-open https://mail.steelhullstudio.nl")
                            onRightClicked: (gx, gy) => {
                                let p = mapToItem(menu, gx, gy)
                                ctxMenu.openForItem(p.x, p.y, "E-mail", "cmd", "xdg-open https://mail.steelhullstudio.nl", -1)
                            }
                        }

                        Separator {
                            Layout.fillWidth: true
                            lineColor: "#c8c6c0"
                        }

                        // 6+ Meest gebruikte / favoriete programma's (enkele regel, gewone Tahoma)
                        ListView {
                            id: leftListView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            interactive: false
                            model: leftAppsModel

                            delegate: AppEntry {
                                required property int index
                                required property string appTitle
                                required property string iconName
                                required property string sourceType
                                required property int sourceIndex

                                width: ListView.view.width
                                height: menu.isSmallIcons ? 26 : 38
                                label: appTitle
                                icon: iconName
                                iconSize: menu.isSmallIcons ? 20 : 30
                                bold: menu.isPinned(appTitle)
                                onHovered: {
                                    menu.showRecentDocs = false
                                }
                                onActivated: menu.triggerLeftItem(sourceType, sourceIndex)
                                onRightClicked: (gx, gy) => {
                                    let p = mapToItem(menu, gx, gy)
                                    ctxMenu.openForItem(p.x, p.y, appTitle, sourceType, "", sourceIndex)
                                }
                            }
                        }

                        Separator {
                            Layout.fillWidth: true
                            lineColor: "#c8c6c0"
                        }

                        // "Alle programma's" met het echte groene 3D XP-pijltje
                        Rectangle {
                            id: allProgramsBar
                            Layout.fillWidth: true
                            Layout.preferredHeight: 34
                            Layout.leftMargin: 3
                            Layout.rightMargin: 3
                            Layout.bottomMargin: 2
                            readonly property bool activeState: allHover.containsMouse || menu.allPrograms
                            color: activeState ? "#316ac5" : "transparent"

                            Row {
                                anchors.horizontalCenter: parent.horizontalCenter
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 8

                                XpText {
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "All Programs"
                                    color: allProgramsBar.activeState ? "white" : "black"
                                    heavy: true
                                    font.pixelSize: 12
                                }
                                Image {
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: 18
                                    height: 18
                                    source: Qt.resolvedUrl("../images/icons/alle-programmas-pijl.svg")
                                    sourceSize.width: 36
                                    sourceSize.height: 36
                                    smooth: true
                                }
                            }
                            MouseArea {
                                id: allHover
                                anchors.fill: parent
                                hoverEnabled: true
                                onEntered: {
                                    closeAllProgsTimer.stop()
                                    menu.showRecentDocs = false
                                    if (!menu.allPrograms) {
                                        menu.allProgramsOpenedAt = Date.now()
                                        menu.allPrograms = true
                                    }
                                }
                                onClicked: {
                                    closeAllProgsTimer.stop()
                                    menu.showRecentDocs = false
                                    let now = Date.now()
                                    if (!menu.allPrograms) {
                                        menu.allProgramsOpenedAt = now
                                        menu.allPrograms = true
                                    } else if (now - menu.allProgramsOpenedAt > 600) {
                                        menu.allPrograms = false
                                        menu.activeCategoryIndex = -1
                                        menu.activeBuiltinFolder = ""
                                        menu.activeSubFolder = ""
                                    } else {
                                        // Net geopend door erop te wijzen -> klik houdt het menu juist open!
                                        menu.allPrograms = true
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.preferredWidth: 1
                    Layout.fillHeight: true
                    color: "#95bdee"
                }

                // Rechterkolom (#d3e5fa) met de 11 authentieke Windows XP plaatsen & systeemitems
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "#d3e5fa"

                    Column {
                        anchors.fill: parent
                        anchors.topMargin: 5

                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; bold: true; light: true
                            label: "My Documents"; iconFile: "docs.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.openFolder(StandardPaths.writableLocation(StandardPaths.DocumentsLocation))
                        }
                        AppEntry {
                            id: recentDocsEntry
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; bold: true; light: true; arrow: true
                            activeHighlight: menu.showRecentDocs
                            label: "My Recent Documents"; iconFile: "recent.svg"
                            onHovered: {
                                menu.scheduleCloseAllPrograms()
                                menu.showRecentDocs = true
                            }
                            onActivated: menu.openFolder("recentlyused:/files/")
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; bold: true; light: true
                            label: "My Pictures"; iconFile: "pics.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.openFolder(StandardPaths.writableLocation(StandardPaths.PicturesLocation))
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; bold: true; light: true
                            label: "My Music"; iconFile: "music.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.openFolder(StandardPaths.writableLocation(StandardPaths.MusicLocation))
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; bold: true; light: true
                            label: "My Computer"; iconFile: "computer.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.runXpMode("computer")
                            onRightClicked: (gx, gy) => {
                                let p = mapToItem(menu, gx, gy)
                                ctxMenu.openForItem(p.x, p.y, "My Computer", "computer", "", -1)
                            }
                        }
                        Separator { width: parent.width; lineColor: "#95bdee" }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; light: true
                            label: "Control Panel"; iconFile: "controlpanel.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.runXpMode("configuratiescherm")
                            onRightClicked: (gx, gy) => {
                                let p = mapToItem(menu, gx, gy)
                                ctxMenu.openForItem(p.x, p.y, "Control Panel", "controlpanel", "", -1)
                            }
                        }
                        AppEntry {
                            width: parent.width; height: 38; iconSize: 24; fontSize: 11; light: true; allowWrap: true
                            label: "Set Program Access and Defaults"; iconFile: "defapps.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.run("kcmshell6 kcm_componentchooser")
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; light: true
                            label: "Printers and Faxes"; iconFile: "printers.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.run("kcmshell6 kcm_printer_manager")
                        }
                        Separator { width: parent.width; lineColor: "#95bdee" }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; light: true
                            label: "Help and Support"; iconFile: "help.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.run("khelpcenter")
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; light: true
                            label: "Search"; iconFile: "search.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.run("krunner")
                        }
                        AppEntry {
                            width: parent.width; height: 32; iconSize: 24; fontSize: 11; light: true
                            label: "Run..."; iconFile: "run.svg"
                            onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                            onActivated: menu.runXpMode("uitvoeren")
                        }
                    }
                }
            }

            // Voetbalk met glanzende XP Afmelden- en Uitschakelen-knoppen
            Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: -2
                Layout.rightMargin: -2
                Layout.preferredHeight: 42
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#3d8bea" }
                    GradientStop { position: 0.15; color: "#2a71dc" }
                    GradientStop { position: 0.85; color: "#1f62d0" }
                    GradientStop { position: 1.0; color: "#1650b8" }
                }

                Row {
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 4

                    SessionButton {
                        label: "Log Off"
                        iconFile: "logout.svg"
                        onActivated: menu.runXpMode("afmelden")
                    }
                    SessionButton {
                        label: "Turn Off Computer"
                        iconFile: "shutdown.svg"
                        onActivated: {
                            menu.closeRequested()
                            session.requestShutdown()
                        }
                    }
                }
            }
        }

        // === RESIZE HANDLES VANAF DE RANDEN (Bovenrand, Rechterrand, Rechterbovenhoek) ===
        // 1. Bovenrand (Hoogte aanpassen)
        MouseArea {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 14
            height: 7
            cursorShape: Qt.SizeVerCursor
            property real startMouseY: 0
            property int startHeight: 0
            onPressed: mouse => {
                startMouseY = mapToGlobal(mouse.x, mouse.y).y
                startHeight = menu.menuHeight
            }
            onPositionChanged: mouse => {
                if (pressed) {
                    let curY = mapToGlobal(mouse.x, mouse.y).y
                    let deltaY = startMouseY - curY
                    let nh = Math.max(430, Math.min(860, startHeight + deltaY))
                    menu.menuHeight = nh
                    Plasmoid.configuration.menuHeight = nh
                    menu.rebuildLeftItems()
                }
            }
        }

        // 2. Rechterrand (Breedte aanpassen)
        MouseArea {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.topMargin: 14
            width: 7
            cursorShape: Qt.SizeHorCursor
            property real startMouseX: 0
            property int startWidth: 0
            onPressed: mouse => {
                startMouseX = mapToGlobal(mouse.x, mouse.y).x
                startWidth = menu.menuWidth
            }
            onPositionChanged: mouse => {
                if (pressed) {
                    let curX = mapToGlobal(mouse.x, mouse.y).x
                    let deltaX = curX - startMouseX
                    let nw = Math.max(360, Math.min(720, startWidth + deltaX))
                    menu.menuWidth = nw
                    Plasmoid.configuration.menuWidth = nw
                }
            }
        }

        // 3. Rechterbovenhoek (Breedte + Hoogte tegelijk aanpassen)
        MouseArea {
            anchors.top: parent.top
            anchors.right: parent.right
            width: 14
            height: 14
            cursorShape: Qt.SizeBDiagCursor
            property real startMouseX: 0
            property real startMouseY: 0
            property int startWidth: 0
            property int startHeight: 0
            onPressed: mouse => {
                let g = mapToGlobal(mouse.x, mouse.y)
                startMouseX = g.x
                startMouseY = g.y
                startWidth = menu.menuWidth
                startHeight = menu.menuHeight
            }
            onPositionChanged: mouse => {
                if (pressed) {
                    let g = mapToGlobal(mouse.x, mouse.y)
                    let nw = Math.max(360, Math.min(720, startWidth + (g.x - startMouseX)))
                    let nh = Math.max(430, Math.min(860, startHeight + (startMouseY - g.y)))
                    menu.menuWidth = nw
                    menu.menuHeight = nh
                    Plasmoid.configuration.menuWidth = nw
                    Plasmoid.configuration.menuHeight = nh
                    menu.rebuildLeftItems()
                }
            }
        }
    }

    // === KLASSIEK WINDOWS XP MENU START ("Classic Start Menu" - 1 kolom #d4d0c8 met verticale zijbalk) ===
    Rectangle {
        id: classicBox
        visible: menu.isClassicStart
        x: 0
        anchors.bottom: parent.bottom
        width: 244
        height: classicCol.implicitHeight + 10
        color: "#d4d0c8"

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
        }

        // Buitenste 3D randen
        Rectangle { anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; height: 1; color: "#ffffff" }
        Rectangle { anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left; width: 1; color: "#ffffff" }
        Rectangle { anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; height: 1; color: "#404040" }
        Rectangle { anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.right: parent.right; width: 1; color: "#404040" }

        // Binnenste 3D randen
        Rectangle { anchors.top: parent.top; anchors.topMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1; height: 1; color: "#dfdfdf" }
        Rectangle { anchors.top: parent.top; anchors.topMargin: 1; anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1; width: 1; color: "#dfdfdf" }
        Rectangle { anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.left: parent.left; anchors.leftMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1; height: 1; color: "#808080" }
        Rectangle { anchors.top: parent.top; anchors.topMargin: 1; anchors.bottom: parent.bottom; anchors.bottomMargin: 1; anchors.right: parent.right; anchors.rightMargin: 1; width: 1; color: "#808080" }

        // Verticale blauwe "Windows XP Professional" zijbalk links
        Rectangle {
            id: classicSidebar
            anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.left: parent.left
            anchors.margins: 3
            width: 26
            clip: true
            gradient: Gradient {
                GradientStop { position: 0.00; color: "#000080" }
                GradientStop { position: 0.65; color: "#08389c" }
                GradientStop { position: 1.00; color: "#1084d0" }
            }

            Row {
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 10
                anchors.horizontalCenter: parent.horizontalCenter
                rotation: -90
                transformOrigin: Item.BottomLeft
                x: 20
                spacing: 4

                Text {
                    text: "Windows"
                    color: "#ffffff"
                    font.family: "Franklin Gothic Medium, Arial, Tahoma, sans-serif"
                    font.pixelSize: 16
                    font.bold: true
                }
                Text {
                    text: "XP"
                    color: "#ffffff"
                    font.family: "Arial, Tahoma, sans-serif"
                    font.pixelSize: 11
                    font.bold: true
                }
                Text {
                    text: "Professional"
                    color: "#dce8ff"
                    font.family: "Tahoma, sans-serif"
                    font.pixelSize: 14
                }
            }
        }

        Column {
            id: classicCol
            anchors.left: classicSidebar.right
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 2
            anchors.rightMargin: 4
            anchors.topMargin: 4
            spacing: 1

            AppEntry {
                width: parent.width; height: 28; iconSize: 20; fontSize: 11
                label: "Windows Update"; iconFile: "cp-updates.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.run("bazaar || konsole -e ujust update")
            }

            Separator { width: parent.width; lineColor: "#808080" }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11; arrow: true
                activeHighlight: menu.allPrograms
                label: "Programs"; iconFile: "progfolder.svg"
                onHovered: {
                    closeAllProgsTimer.stop()
                    menu.showRecentDocs = false
                    menu.allProgramsOpenedAt = Date.now()
                    menu.allPrograms = true
                }
                onActivated: {
                    closeAllProgsTimer.stop()
                    menu.allPrograms = true
                }
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11; arrow: true
                activeHighlight: menu.showRecentDocs
                label: "Documents"; iconFile: "docs.svg"
                onHovered: {
                    menu.scheduleCloseAllPrograms()
                    menu.showRecentDocs = true
                }
                onActivated: menu.openFolder(StandardPaths.writableLocation(StandardPaths.DocumentsLocation))
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11; arrow: true
                label: "Settings"; iconFile: "controlpanel.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.runXpMode("configuratiescherm")
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11
                label: "Search"; iconFile: "search.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.run("krunner")
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11
                label: "Help and Support"; iconFile: "help.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.run("khelpcenter")
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11
                label: "Run..."; iconFile: "run.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.runXpMode("uitvoeren")
            }

            Separator { width: parent.width; lineColor: "#808080" }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11
                label: "Log Off " + (user.fullName || "King Geoffrey") + "..."; iconFile: "logout.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: menu.runXpMode("afmelden")
            }

            AppEntry {
                width: parent.width; height: 30; iconSize: 22; fontSize: 11
                label: "Turn Off Computer..."; iconFile: "shutdown.svg"
                onHovered: { menu.scheduleCloseAllPrograms(); menu.showRecentDocs = false }
                onActivated: {
                    menu.closeRequested()
                    session.requestShutdown()
                }
            }
        }
    }

    // === UITKLAPMENU: ALLE PROGRAMMA'S (Authentiek Windows XP Cascade Flyout Menu) ===
    // Kolom 1: Hoofdmenu van Alle programma's (opent rechts naast de Alle programma's-knop zodat de linkerkolom vrij blijft!)
    Rectangle {
        id: allProgramsCol1
        visible: menu.allPrograms
        x: menu.isClassicStart ? (classicBox.width - 2) : Math.round(menu.menuWidth * 0.36)
        anchors.bottom: parent.bottom
        anchors.bottomMargin: menu.isClassicStart ? 32 : 42
        width: 268
        height: Math.min(menu.menuHeight - 44, col1Layout.implicitHeight + 8)
        color: "#ffffff"
        border.color: "#7b9ebd"
        border.width: 1

        // Blokkeer muis-hover doorlekken naar de rechterkolom erachter!
        MouseArea {
            id: col1Blocker
            anchors.fill: parent
            hoverEnabled: true
            onEntered: closeAllProgsTimer.stop()
        }

        // Kenmerkende verticale blauwe XP-strook aan de linkerkant van het popupmenu
        Rectangle {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 2
            width: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#4c96f0" }
                GradientStop { position: 0.5; color: "#2b73dc" }
                GradientStop { position: 1.0; color: "#1952b8" }
            }
        }

        Flickable {
            anchors.fill: parent
            anchors.leftMargin: 9
            anchors.rightMargin: 2
            anchors.topMargin: 3
            anchors.bottomMargin: 3
            contentHeight: col1Layout.implicitHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            Column {
                id: col1Layout
                width: parent.width
                spacing: 1

                // Bovenste 3 vaste XP items boven de scheidingslijn
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Set Program Access and Defaults"; iconFile: "defapps.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("kcmshell6 kcm_componentchooser")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Windows Catalog"; iconFile: "cp-folderopts.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("xdg-open https://flathub.org")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Windows Update"; iconFile: "cp-updates.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("bazaar || konsole -e ujust update")
                }

                Rectangle {
                    width: parent.width - 8
                    x: 4
                    height: 1
                    color: "#d4d0c8"
                }

                // Ingebouwde Windows XP mappen (Accessories, Startup)
                AppEntry {
                    id: accEntry
                    width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                    label: "Accessories"; iconFile: "progfolder.svg"
                    activeHighlight: menu.activeBuiltinFolder === "accessories"
                    onHovered: {
                        menu.requestCol2Change(-1, "accessories", accEntry.mapToItem(menu, 0, 0).y)
                    }
                    onActivated: {
                        col2SwitchTimer.stop()
                        menu.col2TargetY = accEntry.mapToItem(menu, 0, 0).y
                        menu.activeCategoryIndex = -1
                        menu.activeBuiltinFolder = "accessories"
                    }
                }

                AppEntry {
                    id: startupEntry
                    width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                    label: "Startup"; iconFile: "progfolder.svg"
                    activeHighlight: menu.activeBuiltinFolder === "startup"
                    onHovered: {
                        menu.requestCol2Change(-1, "startup", startupEntry.mapToItem(menu, 0, 0).y)
                    }
                    onActivated: menu.run("kcmshell6 kcm_autostart")
                }

                // Alle echte KDE-applicatiecategorieën (met het gele XP programmamap-icoon)
                Repeater {
                    model: menu.catRootModel
                    delegate: AppEntry {
                        id: catEntryItem
                        required property int index
                        required property var model

                        readonly property string catName: (model.display || "").toString()
                        readonly property bool isCat: catName !== ""

                        width: col1Layout.width
                        height: isCat ? 24 : 0
                        visible: isCat
                        iconSize: 18
                        fontSize: 11
                        label: catName
                        iconFile: "progfolder.svg"
                        arrow: true
                        activeHighlight: menu.activeCategoryIndex === index
                        onHovered: {
                            menu.requestCol2Change(index, "", catEntryItem.mapToItem(menu, 0, 0).y)
                        }
                        onActivated: {
                            col2SwitchTimer.stop()
                            menu.col2TargetY = catEntryItem.mapToItem(menu, 0, 0).y
                            menu.activeBuiltinFolder = ""
                            menu.activeSubFolder = ""
                            menu.activeCategoryIndex = index
                        }
                    }
                }

                // Losse klassieke XP-programma's onder de mappen
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Internet Explorer"; iconFile: "ie6.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("xdg-open https://www.google.nl")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "MSN"; iconFile: "msn.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("xdg-open https://messenger.steelhullstudio.nl")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Outlook Express"; iconFile: "outlook.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("xdg-open https://mail.steelhullstudio.nl")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16; fontSize: 11
                    label: "Windows Explorer"; iconFile: "computer.svg"
                    onHovered: menu.requestCol2Change(-1, "", 160)
                    onActivated: menu.run("dolphin")
                }

                // Favoriete programma's van de gebruiker onderaan de lijst
                Repeater {
                    model: leftAppsModel
                    delegate: AppEntry {
                        required property int index
                        required property string appTitle
                        required property string iconName
                        required property string sourceType
                        required property int sourceIndex

                        width: col1Layout.width
                        height: 24
                        iconSize: 16
                        fontSize: 11
                        label: appTitle
                        icon: iconName
                        onHovered: {
                            menu.requestCol2Change(-1, "", 160)
                        }
                        onActivated: menu.triggerLeftItem(sourceType, sourceIndex)
                        onRightClicked: (gx, gy) => {
                            let p = mapToItem(menu, gx, gy)
                            ctxMenu.openForItem(p.x, p.y, appTitle, sourceType, "", sourceIndex)
                        }
                    }
                }
            }
        }
    }

    // Kolom 2: Submenu rechts naast Kolom 1 (uitgelijnd op de aangewezen map, precies zoals Windows XP!)
    Rectangle {
        id: allProgramsCol2
        readonly property var subCatModel: (menu.activeCategoryIndex >= 0 && menu.catRootModel)
            ? menu.catRootModel.modelForRow(menu.activeCategoryIndex)
            : null
        visible: menu.allPrograms && (menu.activeBuiltinFolder !== "" || subCatModel !== null)
        x: allProgramsCol1.x + allProgramsCol1.width - 2
        width: 230
        height: Math.min(menu.menuHeight - 44, col2Layout.implicitHeight + 8)
        y: Math.max(8, Math.min(menu.col2TargetY, (allProgramsCol1.y + allProgramsCol1.height) - height))
        color: "#ffffff"
        border.color: "#7b9ebd"
        border.width: 1

        // Blokkeer muis-hover doorlekken en annuleer sluit-/wisseltimers zodra muis in Kolom 2 komt
        MouseArea {
            id: col2Blocker
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                closeAllProgsTimer.stop()
                col2SwitchTimer.stop()
            }
        }

        // Verticale blauwe XP-strook links
        Rectangle {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 2
            width: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#4c96f0" }
                GradientStop { position: 0.5; color: "#2b73dc" }
                GradientStop { position: 1.0; color: "#1952b8" }
            }
        }

        Flickable {
            anchors.fill: parent
            anchors.leftMargin: 9
            anchors.rightMargin: 2
            anchors.topMargin: 3
            anchors.bottomMargin: 3
            contentHeight: col2Layout.implicitHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            Column {
                id: col2Layout
                width: parent.width
                spacing: 1

                // Als Bureau-accessoires actief is: submappen + klassieke accessoires met originele XP-iconen!
                Column {
                    width: parent.width
                    visible: menu.activeBuiltinFolder === "accessories"
                    spacing: 1

                    AppEntry {
                        id: subAccEntry
                        width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                        label: "Accessibility"; iconFile: "progfolder.svg"
                        activeHighlight: menu.activeSubFolder === "accessibility"
                        onHovered: {
                            menu.col3TargetY = subAccEntry.mapToItem(menu, 0, 0).y
                            menu.activeSubFolder = "accessibility"
                        }
                        onActivated: menu.activeSubFolder = "accessibility"
                    }
                    AppEntry {
                        id: subCommEntry
                        width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                        label: "Communications"; iconFile: "progfolder.svg"
                        activeHighlight: menu.activeSubFolder === "communications"
                        onHovered: {
                            menu.col3TargetY = subCommEntry.mapToItem(menu, 0, 0).y
                            menu.activeSubFolder = "communications"
                        }
                        onActivated: menu.activeSubFolder = "communications"
                    }
                    AppEntry {
                        id: subEntEntry
                        width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                        label: "Entertainment"; iconFile: "progfolder.svg"
                        activeHighlight: menu.activeSubFolder === "entertainment"
                        onHovered: {
                            menu.col3TargetY = subEntEntry.mapToItem(menu, 0, 0).y
                            menu.activeSubFolder = "entertainment"
                        }
                        onActivated: menu.activeSubFolder = "entertainment"
                    }
                    AppEntry {
                        id: subSysEntry
                        width: parent.width; height: 24; iconSize: 18; fontSize: 11; arrow: true
                        label: "System Tools"; iconFile: "progfolder.svg"
                        activeHighlight: menu.activeSubFolder === "systools"
                        onHovered: {
                            menu.col3TargetY = subSysEntry.mapToItem(menu, 0, 0).y
                            menu.activeSubFolder = "systools"
                        }
                        onActivated: menu.activeSubFolder = "systools"
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Address Book"; iconFile: "addressbook.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.runXpMode("configuratiescherm")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Notepad"; iconFile: "notepad.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("kwrite || kate")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Command Prompt"; iconFile: "cmd.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("ptyxis || konsole")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Paint"; iconFile: "paint.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("gimp || spectacle")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Calculator"; iconFile: "calc.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("kcalc || gnome-calculator || ptyxis -e python3")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Synchronize"; iconFile: "cp-updates.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("bazaar || konsole -e ujust update")
                    }
                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Windows Explorer"; iconFile: "folder.svg"
                        onHovered: menu.activeSubFolder = ""
                        onActivated: menu.run("dolphin")
                    }
                }

                // Als Opstarten actief is
                Column {
                    width: parent.width
                    visible: menu.activeBuiltinFolder === "startup"
                    spacing: 1

                    AppEntry {
                        width: parent.width; height: 24; iconSize: 16; fontSize: 11
                        label: "Manage Startup Programs"; iconFile: "cp-updates.svg"
                        onActivated: menu.run("kcmshell6 kcm_autostart")
                    }
                }

                // Als een KDE-categorie actief is: alle apps in die categorie
                Repeater {
                    model: allProgramsCol2.subCatModel
                    delegate: AppEntry {
                        required property int index
                        required property var model

                        width: col2Layout.width
                        height: 24
                        iconSize: 16
                        fontSize: 11
                        label: model.display || ""
                        icon: model.decoration
                        onHovered: menu.activeSubFolder = ""
                        onActivated: {
                            allProgramsCol2.subCatModel.trigger(index, "", null)
                            menu.closeRequested()
                        }
                        onRightClicked: (gx, gy) => {
                            let p = mapToItem(menu, gx, gy)
                            ctxMenu.openForItem(p.x, p.y, model.display || "", "subcat", "", index)
                        }
                    }
                }
            }
        }
    }

    // Kolom 3: Derde-niveau submenu rechts naast Kolom 2 (bijv. Bureau-accessoires -> Systeemwerkset)
    Rectangle {
        id: allProgramsCol3
        visible: menu.allPrograms && menu.activeBuiltinFolder === "accessories" && menu.activeSubFolder !== ""
        x: allProgramsCol2.x + allProgramsCol2.width - 2
        width: 225
        height: col3Layout.implicitHeight + 8
        y: Math.max(8, Math.min(menu.col3TargetY, (allProgramsCol1.y + allProgramsCol1.height) - height))
        color: "#ffffff"
        border.color: "#7b9ebd"
        border.width: 1

        MouseArea {
            id: col3Blocker
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                closeAllProgsTimer.stop()
                col2SwitchTimer.stop()
            }
        }

        Rectangle {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 2
            width: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#4c96f0" }
                GradientStop { position: 0.5; color: "#2b73dc" }
                GradientStop { position: 1.0; color: "#1952b8" }
            }
        }

        Column {
            id: col3Layout
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 9
            anchors.rightMargin: 2
            anchors.topMargin: 3
            spacing: 1

            // System Tools
            Column {
                width: parent.width
                visible: menu.activeSubFolder === "systools"
                spacing: 1

                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Backup"; iconFile: "hdd.svg"
                    onActivated: menu.run("kcmshell6 kcm_disks")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Security Center"; iconFile: "xp-shield.svg"
                    onActivated: menu.run("bazaar || konsole -e ujust update")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Scheduled Tasks"; iconFile: "cp-updates.svg"
                    onActivated: menu.run("kcmshell6 kcm_autostart")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Disk Defragmenter"; iconFile: "cp-defrag.svg"
                    onActivated: menu.run("kcmshell6 kcm_disks")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Disk Cleanup"; iconFile: "cp-clean.svg"
                    onActivated: menu.run("plasma-systemmonitor")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Character Map"; iconFile: "cp-fonts.svg"
                    onActivated: menu.run("plasma-emojier")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "System Restore"; iconFile: "cp-system.svg"
                    onActivated: menu.runXpMode("systeem")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "System Information"; iconFile: "cp-admin.svg"
                    onActivated: menu.runXpMode("systeem")
                }
            }

            // Accessibility
            Column {
                width: parent.width
                visible: menu.activeSubFolder === "accessibility"
                spacing: 1

                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Accessibility Wizard"; iconFile: "cat-access.svg"
                    onActivated: menu.run("kcmshell6 kcm_access")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "On-Screen Keyboard"; iconFile: "cp-keyboard.svg"
                    onActivated: menu.run("kcmshell6 kcm_virtualkeyboard")
                }
            }

            // Communications
            Column {
                width: parent.width
                visible: menu.activeSubFolder === "communications"
                spacing: 1

                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Network Connections"; iconFile: "cp-network.svg"
                    onActivated: menu.run("kcmshell6 kcm_networkmanagement")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Wireless Network Setup Wizard"; iconFile: "cp-wireless.svg"
                    onActivated: menu.run("kcmshell6 kcm_networkmanagement")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Remote Desktop Connection"; iconFile: "computer.svg"
                    onActivated: menu.run("krdc || kcmshell6 kcm_krdpserver")
                }
            }

            // Entertainment
            Column {
                width: parent.width
                visible: menu.activeSubFolder === "entertainment"
                spacing: 1

                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Volume Control"; iconFile: "cp-sound.svg"
                    onActivated: menu.run("kcmshell6 kcm_pulseaudio")
                }
                AppEntry {
                    width: parent.width; height: 24; iconSize: 16
                    label: "Sound Recorder & Audio"; iconFile: "cat-sound.svg"
                    onActivated: menu.run("kcmshell6 kcm_soundtheme")
                }
            }
        }
    }

    // === UITKLAPMENU: MIJN RECENTE DOCUMENTEN ===
    Rectangle {
        id: recentDocsPopup
        visible: menu.showRecentDocs
        x: menu.isClassicStart ? (classicBox.width - 2) : (menu.menuWidth - 4)
        y: menu.isClassicStart ? (classicBox.y + 60) : (startBox.y + 92)
        width: 240
        height: Math.min(340, Math.max(32, recentDocsCol.implicitHeight + 8))
        color: "#ffffff"
        border.color: "#7b9ebd"
        border.width: 1

        Rectangle {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 2
            width: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#4c96f0" }
                GradientStop { position: 0.5; color: "#2b73dc" }
                GradientStop { position: 1.0; color: "#1952b8" }
            }
        }

        Column {
            id: recentDocsCol
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 9
            anchors.rightMargin: 2
            anchors.topMargin: 3
            spacing: 1

            Repeater {
                model: menu.recentDocsModel
                delegate: AppEntry {
                    required property int index
                    required property var model

                    width: recentDocsCol.width
                    height: index < 12 ? 24 : 0
                    visible: index < 12
                    iconSize: 16
                    label: model.display || "(Leeg)"
                    icon: model.decoration || "text-x-generic"
                    onActivated: {
                        menu.recentDocsModel.trigger(index, "", null)
                        menu.closeRequested()
                    }
                }
            }
        }
    }

    // === WINDOWS XP RECHTERMUISKNOP CONTEXTMENU ===
    Rectangle {
        id: ctxMenu
        visible: false
        width: 215
        height: ctxCol.implicitHeight + 6
        color: "#ffffff"
        border.color: "#aca899"
        border.width: 1
        z: 100

        property string targetLabel: ""
        property string targetType: ""
        property string targetCmd: ""
        property int targetIndex: -1

        function openForItem(px, py, label, sType, sCmd, sIdx) {
            targetLabel = label
            targetType = sType
            targetCmd = sCmd
            targetIndex = sIdx
            x = Math.min(px, menu.width - width - 4)
            y = Math.max(4, Math.min(py, menu.height - height - 4))
            visible = true
        }

        Column {
            id: ctxCol
            anchors.fill: parent
            anchors.margins: 3
            spacing: 1

            // 1. Open (Bold)
            AppEntry {
                width: parent.width; height: 22; iconSize: 14; bold: true
                label: "Open"; iconFile: "run.svg"
                onActivated: {
                    ctxMenu.visible = false
                    if (ctxMenu.targetType === "cmd") {
                        menu.run(ctxMenu.targetCmd)
                    } else if (ctxMenu.targetType === "computer") {
                        menu.runXpMode("computer")
                    } else if (ctxMenu.targetType === "controlpanel") {
                        menu.runXpMode("configuratiescherm")
                    } else if (ctxMenu.targetType === "subcat" && allProgramsCol2.subCatModel) {
                        allProgramsCol2.subCatModel.trigger(ctxMenu.targetIndex, "", null)
                        menu.closeRequested()
                    } else {
                        menu.triggerLeftItem(ctxMenu.targetType, ctxMenu.targetIndex)
                    }
                }
            }

            // Extra option for My Computer: Explore in Dolphin
            AppEntry {
                width: parent.width; height: ctxMenu.targetType === "computer" ? 22 : 0
                visible: ctxMenu.targetType === "computer"
                iconSize: 14
                label: "Explore in Dolphin"; iconFile: "folder.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.run("dolphin \"$HOME\"")
                }
            }

            Rectangle { width: parent.width - 6; x: 3; height: 1; color: "#d4d0c8" }

            // 2. Pin to / Unpin from Start menu
            AppEntry {
                width: parent.width; height: 22; iconSize: 14
                label: menu.isPinned(ctxMenu.targetLabel) ? "Unpin from Start menu" : "Pin to Start menu"
                iconFile: "progfolder.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.togglePinItem(ctxMenu.targetLabel)
                }
            }

            // 2b. Add to / Remove from Quick Launch
            AppEntry {
                width: parent.width; height: 22; iconSize: 14
                label: menu.isInQuickLaunch(ctxMenu.targetLabel) ? "Remove from Quick Launch" : "Add to Quick Launch"
                iconFile: "show-desktop.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.toggleQuickLaunch(ctxMenu.targetLabel)
                }
            }

            // 3. Remove from This List
            AppEntry {
                width: parent.width; height: 22; iconSize: 14
                label: "Remove from This List"
                iconFile: "cp-clean.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.removeItemFromList(ctxMenu.targetLabel)
                }
            }

            // 4. Restore removed items
            AppEntry {
                width: parent.width
                height: menu.removedList.length > 0 ? 22 : 0
                visible: menu.removedList.length > 0
                iconSize: 14
                label: "Restore Removed Items (" + menu.removedList.length + ")"
                iconFile: "cp-updates.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.restoreRemovedItems()
                }
            }

            Rectangle { width: parent.width - 6; x: 3; height: 1; color: "#d4d0c8" }

            // 5. Reset Start Menu Size
            AppEntry {
                width: parent.width; height: 22; iconSize: 14
                label: "Reset Start Menu Size"
                iconFile: "cp-display.svg"
                onActivated: {
                    ctxMenu.visible = false
                    menu.resetMenuSize()
                }
            }

            // 6. Properties
            AppEntry {
                width: parent.width; height: 22; iconSize: 14
                label: "Properties"
                iconFile: "controlpanel.svg"
                onActivated: {
                    ctxMenu.visible = false
                    if (ctxMenu.targetType === "computer") {
                        menu.runXpMode("systeem")
                    } else {
                        menu.runXpMode("taakbalk")
                    }
                }
            }
        }
    }
}
