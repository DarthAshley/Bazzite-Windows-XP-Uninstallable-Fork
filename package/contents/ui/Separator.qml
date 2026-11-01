import QtQuick

// Lijn die naar de randen vervaagt, zoals in het XP-startmenu
Item {
    id: separator

    property color lineColor

    implicitHeight: 7
    height: implicitHeight

    Rectangle {
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 8
        anchors.rightMargin: 8
        height: 1
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "transparent" }
            GradientStop { position: 0.5; color: separator.lineColor }
            GradientStop { position: 1.0; color: "transparent" }
        }
    }
}
