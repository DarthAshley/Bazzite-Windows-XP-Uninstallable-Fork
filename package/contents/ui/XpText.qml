import QtQuick

// Wine's Tahoma Bold heeft dunne lijnen; een tweede laag op 1 pixel geeft de XP-dikte
Text {
    id: base

    property bool heavy: false

    font.family: heavy ? "TahomB" : "Tahoma"
    renderType: Text.NativeRendering

    Text {
        x: 1
        visible: base.heavy
        width: base.width
        text: base.text
        elide: base.elide
        color: base.color
        font: base.font
        renderType: base.renderType
    }
}
