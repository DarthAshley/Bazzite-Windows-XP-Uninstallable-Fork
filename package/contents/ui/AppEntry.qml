import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: entry

    property string label: ""
    property string subtitle: ""
    property var icon: ""
    property string iconFile: ""
    property int iconSize: 32
    property int fontSize: 12
    property bool bold: false
    property bool light: false
    property bool arrow: false
    property bool allowWrap: false
    property bool activeHighlight: false

    signal activated()
    signal rightClicked(real globalX, real globalY)
    signal hovered()

    readonly property bool isHighlighted: hover.containsMouse || entry.activeHighlight
    color: isHighlighted ? "#316ac5" : "transparent"

    readonly property string effectiveIconFile: {
        if (entry.iconFile !== "") return entry.iconFile;
        var ic = ("" + (entry.icon || "")).toLowerCase().trim();
        if (ic === "discord" || ic === "com.discordapp.discord" || ic === "dev.vencord.vesktop" || ic.indexOf("discord") !== -1 || ic.indexOf("vesktop") !== -1) {
            return "discord.svg";
        }
        if (ic === "lutris" || ic === "net.lutris.lutris" || ic.indexOf("lutris") !== -1) {
            return "lutris.png";
        }
        if (ic === "firefox" || ic === "org.mozilla.firefox" || ic.indexOf("firefox") !== -1) {
            return "firefox.svg";
        }
        if (ic === "internet explorer" || ic === "ie6" || ic === "internet-explorer" || ic === "msie") {
            return "ie6.svg";
        }
        return "";
    }

    Image {
        id: customIcon
        x: 7
        anchors.verticalCenter: parent.verticalCenter
        width: entry.iconSize
        height: entry.iconSize
        visible: entry.effectiveIconFile !== ""
        source: entry.effectiveIconFile !== "" ? Qt.resolvedUrl("../images/icons/" + entry.effectiveIconFile) : ""
        sourceSize.width: entry.iconSize * 2
        sourceSize.height: entry.iconSize * 2
        smooth: true
    }

    Kirigami.Icon {
        id: entryIcon
        x: 7
        anchors.verticalCenter: parent.verticalCenter
        width: entry.iconSize
        height: entry.iconSize
        visible: entry.effectiveIconFile === ""
        source: entry.icon
        fallback: "application-x-executable"
    }

    Column {
        anchors.left: parent.left
        anchors.leftMargin: entry.iconSize + 14
        anchors.right: parent.right
        anchors.rightMargin: entry.arrow ? 18 : 6
        anchors.verticalCenter: parent.verticalCenter

        XpText {
            width: parent.width
            text: entry.label
            wrapMode: entry.allowWrap ? Text.WordWrap : Text.NoWrap
            maximumLineCount: entry.allowWrap ? 2 : 1
            elide: Text.ElideRight
            color: entry.isHighlighted ? "white" : (entry.light ? "#0a246a" : "black")
            heavy: entry.bold
            font.pixelSize: entry.fontSize
        }
        Text {
            width: parent.width
            visible: entry.subtitle !== ""
            text: entry.subtitle
            elide: Text.ElideRight
            color: entry.isHighlighted ? "#dce7f8" : "#808080"
            renderType: Text.NativeRendering
            font.family: "Tahoma"
            font.pixelSize: 11
        }
    }

    Text {
        anchors.right: parent.right
        anchors.rightMargin: 6
        anchors.verticalCenter: parent.verticalCenter
        visible: entry.arrow
        text: "▸"
        color: entry.isHighlighted ? "white" : "#0a246a"
        font.pixelSize: 12
    }

    MouseArea {
        id: hover
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onEntered: entry.hovered()
        onClicked: mouse => {
            if (mouse.button === Qt.RightButton) {
                entry.rightClicked(mouse.x, mouse.y)
            } else {
                entry.activated()
            }
        }
    }
}
