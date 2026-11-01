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
            Kirigami.FormData.label: "Taakbalk- & Startknopstijl:"
            model: ["Standaard (Uit XP Eigenschappen)", "Windows XP Luna (Groene Startknop)", "Klassieke Windows-stijl (Grijze 3D Startknop)"]
            currentIndex: cfg_taskbarStyle === "classic" ? 2 : (cfg_taskbarStyle === "xp" ? 1 : 0)
            onActivated: index => {
                cfg_taskbarStyle = index === 2 ? "classic" : (index === 1 ? "xp" : "")
            }
        }

        QQC2.ComboBox {
            id: smStyleCombo
            Kirigami.FormData.label: "Stijl van Menu Start:"
            model: ["Standaard (Uit XP Eigenschappen)", "Windows XP Menu Start (2 kolommen)", "Klassiek Menu Start (1 kolom met zijbalk)"]
            currentIndex: cfg_startMenuStyle === "classic" ? 2 : (cfg_startMenuStyle === "xp" ? 1 : 0)
            onActivated: index => {
                cfg_startMenuStyle = index === 2 ? "classic" : (index === 1 ? "xp" : "")
            }
        }

        QQC2.ComboBox {
            id: modeCombo
            Kirigami.FormData.label: "Programmalijst in Menu Start:"
            model: [
                "Standaard (Uit XP Eigenschappen)",
                "Favorieten + Meest gebruikte programma's",
                "Alleen Favorieten",
                "Alleen Meest gebruikte programma's",
                "Vaste eigen lijst"
            ]
            currentIndex: cfg_startItemsMode === "custom" ? 4 : (cfg_startItemsMode === "recent" ? 3 : (cfg_startItemsMode === "favorites" ? 2 : (cfg_startItemsMode === "both" ? 1 : 0)))
            onActivated: index => {
                const map = ["", "both", "favorites", "recent", "custom"]
                cfg_startItemsMode = map[index] || ""
            }
        }

        QQC2.ComboBox {
            id: iconSizeCombo
            Kirigami.FormData.label: "Pictogramgrootte in Menu Start:"
            model: ["Standaard (Uit XP Eigenschappen)", "Grote pictogrammen (30 px)", "Kleine pictogrammen (20 px)"]
            currentIndex: cfg_startIconSize === "small" ? 2 : (cfg_startIconSize === "large" ? 1 : 0)
            onActivated: index => {
                cfg_startIconSize = index === 2 ? "small" : (index === 1 ? "large" : "")
            }
        }

        QQC2.SpinBox {
            id: countSpin
            Kirigami.FormData.label: "Aantal programma's (0 = automatisch):"
            from: 0
            to: 15
        }

        QQC2.CheckBox {
            id: showQLCheck
            Kirigami.FormData.label: "Werkbalk Snel starten:"
            text: "Snelkoppelingen (Bureaublad tonen, Firefox, Verkenner) naast Startknop tonen"
        }
    }
}
