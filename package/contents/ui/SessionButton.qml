import QtQuick

Rectangle {
    id: sessionButton

    property string label
    property string iconFile

    signal activated()

    width: content.width + 14
    height: 32
    radius: 3
    color: hover.containsMouse ? "#3b82e6" : "transparent"
    border.color: hover.containsMouse ? "#76aef8" : "transparent"
    border.width: 1

    Row {
        id: content
        x: 7
        anchors.verticalCenter: parent.verticalCenter
        spacing: 6

        Image {
            anchors.verticalCenter: parent.verticalCenter
            width: 24
            height: 24
            source: Qt.resolvedUrl("../images/icons/" + sessionButton.iconFile)
            sourceSize.width: 48
            sourceSize.height: 48
            smooth: true
        }
        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: sessionButton.label
            color: "white"
            renderType: Text.NativeRendering
            font.family: "Tahoma"
            font.pixelSize: 12
        }
    }

    MouseArea {
        id: hover
        anchors.fill: parent
        hoverEnabled: true
        onClicked: sessionButton.activated()
    }
}
