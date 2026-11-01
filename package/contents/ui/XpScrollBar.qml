import QtQuick

Rectangle {
    id: scrollBar
    required property var target
    width: 16
    color: "#ece9d8"
    border.color: "#d4d0c8"
    border.width: 1
    clip: true

    readonly property bool canScroll: target && target.contentHeight > target.height
    visible: canScroll

    // Track area between top and bottom buttons
    readonly property real trackHeight: Math.max(1, height - 32)
    readonly property real contentRatio: canScroll ? Math.min(1.0, target.height / target.contentHeight) : 1.0
    readonly property real thumbHeight: canScroll ? Math.max(20, trackHeight * contentRatio) : 20
    readonly property real scrollableRange: canScroll ? (target.contentHeight - target.height) : 1
    readonly property real trackRange: Math.max(1, trackHeight - thumbHeight)

    // Top arrow button (16x16)
    Rectangle {
        id: upBtn
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 16
        color: upMouse.pressed ? "#d4d0c8" : (upMouse.containsMouse ? "#faf8f5" : "#ece9d8")
        border.color: "#aca899"
        border.width: 1

        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.right: parent.right; height: 1
            color: upMouse.pressed ? "#707070" : "#ffffff"
        }
        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom; width: 1
            color: upMouse.pressed ? "#707070" : "#ffffff"
        }

        Canvas {
            anchors.centerIn: parent
            width: 7; height: 4
            onPaint: {
                let ctx = getContext("2d")
                ctx.reset()
                ctx.fillStyle = upMouse.pressed ? "#000000" : (upMouse.containsMouse ? "#003c74" : "#404040")
                ctx.beginPath()
                ctx.moveTo(3.5, 0)
                ctx.lineTo(7, 4)
                ctx.lineTo(0, 4)
                ctx.closePath()
                ctx.fill()
            }
        }

        MouseArea {
            id: upMouse
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                if (target) target.contentY = Math.max(0, target.contentY - 38)
            }
        }
    }

    // Scroll Track (Trough)
    Item {
        id: track
        anchors.top: upBtn.bottom
        anchors.bottom: downBtn.top
        anchors.left: parent.left
        anchors.right: parent.right

        MouseArea {
            anchors.fill: parent
            onClicked: mouse => {
                if (!target) return
                if (mouse.y < thumb.y) {
                    target.contentY = Math.max(0, target.contentY - target.height * 0.8)
                } else if (mouse.y > thumb.y + thumb.height) {
                    target.contentY = Math.min(target.contentHeight - target.height, target.contentY + target.height * 0.8)
                }
            }
        }

        // Luna Blue Scroll Thumb (Slider)
        Rectangle {
            id: thumb
            x: 1
            width: parent.width - 2
            height: scrollBar.thumbHeight
            y: {
                if (!scrollBar.canScroll) return 0
                let fraction = Math.max(0, Math.min(1.0, target.contentY / scrollBar.scrollableRange))
                return fraction * scrollBar.trackRange
            }
            radius: 2

            gradient: Gradient {
                GradientStop { position: 0.0; color: thumbMouse.pressed ? "#7bb1e8" : (thumbMouse.containsMouse ? "#d8ecff" : "#c6e2ff") }
                GradientStop { position: 0.3; color: thumbMouse.pressed ? "#5a9ee6" : (thumbMouse.containsMouse ? "#b5d8fa" : "#a2cbf6") }
                GradientStop { position: 0.7; color: thumbMouse.pressed ? "#3b85d6" : (thumbMouse.containsMouse ? "#8cbef2" : "#7aaee8") }
                GradientStop { position: 1.0; color: thumbMouse.pressed ? "#2b6ebd" : (thumbMouse.containsMouse ? "#6ba7e6" : "#5b95da") }
            }
            border.color: thumbMouse.pressed ? "#164a85" : "#4577ab"
            border.width: 1

            Rectangle {
                anchors.left: parent.left; anchors.top: parent.top; anchors.right: parent.right; height: 1
                color: "#ffffff"; opacity: 0.7
            }

            Column {
                anchors.centerIn: parent
                spacing: 2
                Repeater {
                    model: 3
                    Row {
                        spacing: 0
                        Rectangle { width: 5; height: 1; color: "#ffffff"; opacity: 0.9 }
                        Rectangle { width: 5; height: 1; color: "#3a6ea5" }
                    }
                }
            }

            MouseArea {
                id: thumbMouse
                anchors.fill: parent
                hoverEnabled: true
                drag.target: thumb
                drag.axis: Drag.YAxis
                drag.minimumY: 0
                drag.maximumY: scrollBar.trackRange

                onPositionChanged: {
                    if (drag.active && scrollBar.canScroll) {
                        let fraction = thumb.y / scrollBar.trackRange
                        target.contentY = fraction * scrollBar.scrollableRange
                    }
                }
            }
        }
    }

    // Bottom arrow button (16x16)
    Rectangle {
        id: downBtn
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 16
        color: downMouse.pressed ? "#d4d0c8" : (downMouse.containsMouse ? "#faf8f5" : "#ece9d8")
        border.color: "#aca899"
        border.width: 1

        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.right: parent.right; height: 1
            color: downMouse.pressed ? "#707070" : "#ffffff"
        }
        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom; width: 1
            color: downMouse.pressed ? "#707070" : "#ffffff"
        }

        Canvas {
            anchors.centerIn: parent
            width: 7; height: 4
            onPaint: {
                let ctx = getContext("2d")
                ctx.reset()
                ctx.fillStyle = downMouse.pressed ? "#000000" : (downMouse.containsMouse ? "#003c74" : "#404040")
                ctx.beginPath()
                ctx.moveTo(0, 0)
                ctx.lineTo(7, 0)
                ctx.lineTo(3.5, 4)
                ctx.closePath()
                ctx.fill()
            }
        }

        MouseArea {
            id: downMouse
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                if (target) target.contentY = Math.min(target.contentHeight - target.height, target.contentY + 38)
            }
        }
    }
}
