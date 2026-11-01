import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_showQuickLaunch: showQLCheck.checked
    property string cfg_taskbarStyle: ""
    property string cfg_startMenuStyle: ""
    property string cfg_startIconSize: ""
    property alias cfg_startItemsCount: countSpin.value
    property string cfg_startItemsMode: ""

    Kirigami.FormLayout {
        QQC2.ComboBox {
            id: tbStyleCombo
            Kirigami.FormData.label: "Taskbar & Start Button Style:"
            model: ["Default (From XP Properties)", "Windows XP Luna (Green Start Button)", "Windows Classic (Gray 3D Start Button)"]
            currentIndex: cfg_taskbarStyle === "classic" ? 2 : (cfg_taskbarStyle === "xp" ? 1 : 0)
            onActivated: index => {
                cfg_taskbarStyle = index === 2 ? "classic" : (index === 1 ? "xp" : "")
            }
        }

        QQC2.ComboBox {
            id: smStyleCombo
            Kirigami.FormData.label: "Start Menu Style:"
            model: ["Default (From XP Properties)", "Windows XP Start Menu (2 columns)", "Classic Start Menu (1 column with sidebar)"]
            currentIndex: cfg_startMenuStyle === "classic" ? 2 : (cfg_startMenuStyle === "xp" ? 1 : 0)
            onActivated: index => {
                cfg_startMenuStyle = index === 2 ? "classic" : (index === 1 ? "xp" : "")
            }
        }

        QQC2.ComboBox {
            id: modeCombo
            Kirigami.FormData.label: "Start Menu Program List:"
            model: [
                "Default (From XP Properties)",
                "Favorites + Most Frequently Used Programs",
                "Favorites Only",
                "Most Frequently Used Programs Only",
                "Custom Fixed List"
            ]
            currentIndex: cfg_startItemsMode === "custom" ? 4 : (cfg_startItemsMode === "recent" ? 3 : (cfg_startItemsMode === "favorites" ? 2 : (cfg_startItemsMode === "both" ? 1 : 0)))
            onActivated: index => {
                const map = ["", "both", "favorites", "recent", "custom"]
                cfg_startItemsMode = map[index] || ""
            }
        }

        QQC2.ComboBox {
            id: iconSizeCombo
            Kirigami.FormData.label: "Start Menu Icon Size:"
            model: ["Default (From XP Properties)", "Large Icons (30 px)", "Small Icons (20 px)"]
            currentIndex: cfg_startIconSize === "small" ? 2 : (cfg_startIconSize === "large" ? 1 : 0)
            onActivated: index => {
                cfg_startIconSize = index === 2 ? "small" : (index === 1 ? "large" : "")
            }
        }

        QQC2.SpinBox {
            id: countSpin
            Kirigami.FormData.label: "Number of programs on Start menu (0 = auto):"
            from: 0
            to: 15
        }

        QQC2.CheckBox {
            id: showQLCheck
            Kirigami.FormData.label: "Quick Launch Toolbar:"
            text: "Show Quick Launch icons (Show Desktop, Firefox, Explorer) next to Start button"
        }
    }
}
