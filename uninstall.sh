#!/bin/bash
# ===========================================================================================
# Complete Bazzite-Windows-XP Theme Uininstall & Restore Script for KDE Plasma 6
# Written by DarthAshley for users who wish to uninstall and restore their system settings.
# ===========================================================================================
set -u

K="${HOME:-/var/home/king}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

RC="$K/.config/plasma-org.kde.plasma.desktop-appletsrc"
PANEEL="$K/.config/plasmashellrc"
DOLPHIN_RC="$K/.config/dolphinrc"
DOLPHIN_UI="$K/.local/share/kxmlgui5/dolphin/dolphinui.rc"
DOLPHIN_UI6="$K/.local/share/kxmlgui6/dolphin/dolphinui.rc"
KVANTUM_CFG="$K/.config/Kvantum/XPLuna/XPLuna.kvconfig"

echo "==> [1/8] Stopping Plasma Shell..."
systemctl --user stop plasma-plasmashell 2>/dev/null || true

echo "==> [2/8] Restoring original configuration backups..."
[ -f "$RC.voor-xpstart" ] && cp -pf "$RC.voor-xpstart" "$RC" && rm -f "$RC.voor-xpstart"
[ -f "$PANEEL.voor-xpstart" ] && cp -pf "$PANEEL.voor-xpstart" "$PANEEL" && rm -f "$PANEEL.voor-xpstart"
[ -f "$DOLPHIN_RC.voor-xpstart" ] && cp -pf "$DOLPHIN_RC.voor-xpstart" "$DOLPHIN_RC" && rm -f "$DOLPHIN_RC.voor-xpstart"
[ -f "$DOLPHIN_UI.voor-xpstart" ] && cp -pf "$DOLPHIN_UI.voor-xpstart" "$DOLPHIN_UI" && rm -f "$DOLPHIN_UI.voor-xpstart"
[ -f "$KVANTUM_CFG.voor-xpstart" ] && cp -pf "$KVANTUM_CFG.voor-xpstart" "$KVANTUM_CFG" && rm -f "$KVANTUM_CFG.voor-xpstart"

echo "==> [3/8] Removing installed theme packages, icons, wallpapers, avatars, and splash screens..."
rm -rf "$K/.local/share/icons/XPLuna Icons"
rm -rf "$K/.local/share/sounds/XPLuna Sounds"
rm -rf "$K/.local/share/sounds/WinXPsound"
rm -rf "$K/.local/share/wallpapers/XPLuna"
rm -rf "$K/.local/share/aurorae/themes/__aurorae__svg__XPLuna"
rm -rf "$K/.local/share/color-schemes/XPLuna.colors"
rm -rf "$K/.local/share/plasma/desktopthemes/XPLuna"
rm -rf "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop"
rm -rf "$K/.local/share/sddm/themes/XPLuna"
rm -rf "$K/.local/share/xp-startknop"
rm -rf "$K/.config/Kvantum/XPLuna"

# Clean up modified SDDM/lockscreen QML overrides
rm -f "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/LockScreenUi.qml"
rm -f "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/xpConfig.js"
rm -rf "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/images"

# Restore stock avatar if created by installer
rm -f "$K/.face" "$K/.face.icon"

echo "==> [4/8] Removing installed fonts & autostart sound entries..."
rm -rf "$K/.local/share/fonts/xpstart"
rm -f "$K/.config/autostart/xp-opstartgeluid.desktop"
fc-cache -f "$K/.local/share/fonts" 2>/dev/null || true

echo "==> [5/8] Uninstalling Plasma 6 Applets..."
kpackagetool6 -t Plasma/Applet -r nl.steelhull.xpstart 2>/dev/null || true
kpackagetool6 -t Plasma/Applet -r nl.steelhull.xptray 2>/dev/null || true

echo "==> [6/8] Purging hijacked shortcuts & custom applications..."
rm -f "$K/.local/share/applications/systemsettings.desktop"
rm -f "$K/.local/share/applications/xp-taakbeheer.desktop"
rm -f "$K/.local/share/applications/msn.desktop"
rm -f "$K/.local/share/applications/discord.desktop"
rm -f "$DOLPHIN_UI" "$DOLPHIN_UI6"
rm -rf "$K/.local/share/locale/*/LC_MESSAGES/dolphin.mo" 2>/dev/null || true

echo "==> [7/8] Reverting Firefox IE6 & Vesktop MSN Messenger themes..."
# Clean Firefox profiles
for base in "$K/.mozilla/firefox" "$K/.var/app/org.mozilla.firefox/.mozilla/firefox"; do
    if [ -d "$base" ]; then
        for p in "$base"/*; do
            if [ -d "$p" ]; then
                rm -rf "$p/chrome"
                if [ -f "$p/user.js" ]; then
                    sed -i '/toolkit.legacyUserProfileCustomizations.stylesheets/d' "$p/user.js"
                    sed -i '/browser.tabs.drawInTitlebar/d' "$p/user.js"
                fi
            fi
        done
    fi
done

# Clean Vesktop profiles
for VDIR in "$K/.var/app/dev.vencord.Vesktop/config/vesktop" "$K/.config/vesktop"; do
    if [ -d "$VDIR" ]; then
        rm -f "$VDIR/themes/Windows-XP-MSN-Messenger.theme.css"
        rm -f "$VDIR/settings/quickCss.css"
    fi
done

echo "==> [8/8] Resetting KDE Plasma defaults & restarting shell..."
if command -v kwriteconfig6 >/dev/null 2>&1; then
    kwriteconfig6 --file kdeglobals --group General --key ColorScheme "BreezeDark"
    kwriteconfig6 --file kdeglobals --group General --key font "Noto Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group General --key menuFont "Noto Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group General --key toolBarFont "Noto Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group WM --key activeFont "Noto Sans,10,-1,5,700,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group KDE --key LookAndFeelPackage "org.kde.breezedark.desktop"
    kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle "Breeze"
    kwriteconfig6 --file kdeglobals --group Icons --key Theme "breeze-dark"
    kwriteconfig6 --file kdeglobals --group Sounds --key Theme "ocean"

    kwriteconfig6 --file kcminputrc --group Mouse --key cursorTheme "breeze_cursors"

    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library "org.kde.kwin.aurorae"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme "org.kde.breeze"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft "MS"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight "HIAX"

    kwriteconfig6 --file plasmarc --group Theme --key name "default"
    kwriteconfig6 --file ksplashrc --group KSplash --key Theme "org.kde.breeze.desktop"
fi

# Set Kvantum theme back to standard default
cat > "$K/.config/Kvantum/kvantum.kvconfig" << 'EOF'
[General]
theme=KvBreezeDark
EOF

# Force KDE application launcher & configuration service cache update
kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
qdbus-qt6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
systemctl --user start plasma-plasmashell 2>/dev/null || true

echo "==> Done! All Windows XP theme elements have been completely uninstalled."
