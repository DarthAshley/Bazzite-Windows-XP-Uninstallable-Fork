#!/bin/bash
# ==============================================================================
# Bazzite KDE -> Origineel Windows XP (Luna Blue) Compleet Installatiescript
# ==============================================================================
# Installeert en configureert alles automatisch:
#  1. Thema's, Vensterranden (Aurorae XPLuna), Kvantum, Kleuren, Cursors & Iconen
#  2. Originele Windows XP Geluiden (Opstartgeluid, Afsluiten, Klik, Meldingen)
#  3. Windows XP Boot/Login Splash, Vergrendelscherm, Bliss Wallpaper & Schaak-avatar
#  4. Lettertype Tahoma + Scherpe 24px Verkenner-werkbalken in Dolphin
#  5. Windows XP Startmenu + Snel starten (nl.steelhull.xpstart)
#  6. Windows XP Systeemvak met live achtergrond-icoontjes zoals Discord/Steam (nl.steelhull.xptray)
#  7. Windows XP Deze computer, Configuratiescherm, Systeemeigenschappen,
#     Beeldscherm, Taakbalk-eigenschappen, Uitvoeren... én Windows Taakbeheer!
#  8. Windows XP Internet Explorer 6 thema voor Firefox (klassieke werkbalken, iconen & adresbalk)
#
# Gebruik:
#   bash installeren.sh          (Alles installeren en activeren)
#   bash installeren.sh firefox  (Alleen Firefox IE6 thema installeren)
#   bash installeren.sh terug    (Originele paneel/Dolphin-instellingen herstellen)
# ==============================================================================
set -u

K="${HOME:-/var/home/king}"
MAP="$(cd "$(dirname "$0")" && pwd)"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

RC="$K/.config/plasma-org.kde.plasma.desktop-appletsrc"
PANEEL="$K/.config/plasmashellrc"
DOLPHIN_RC="$K/.config/dolphinrc"
DOLPHIN_UI="$K/.local/share/kxmlgui5/dolphin/dolphinui.rc"
KVANTUM_CFG="$K/.config/Kvantum/XPLuna/XPLuna.kvconfig"
SYS_DESKTOP="$K/.local/share/applications/systemsettings.desktop"
XP_SHARE="$K/.local/share/xp-startknop"

installeer_firefox_ie6() {
    local THEME_SRC="$MAP/firefox-ie6-theme/chrome"
    if [ ! -d "$THEME_SRC" ]; then
        echo "    Waarschuwing: $THEME_SRC niet gevonden, overslaan."
        return 0
    fi

    echo "    Firefox omtoveren naar Windows XP Internet Explorer 6..."
    local PROFIELEN=()
    local ZOEKPADEN=(
        "$K/.mozilla/firefox"
        "$K/.var/app/org.mozilla.firefox/.mozilla/firefox"
    )

    for base in "${ZOEKPADEN[@]}"; do
        if [ -d "$base" ]; then
            for p in "$base"/*default*; do
                if [ -d "$p" ]; then
                    local al_in_lijst=false
                    if [ ${#PROFIELEN[@]} -gt 0 ]; then
                        for bestaand in "${PROFIELEN[@]}"; do
                            if [ "$bestaand" = "$p" ]; then
                                al_in_lijst=true
                                break
                            fi
                        done
                    fi
                    if [ "$al_in_lijst" = false ]; then
                        PROFIELEN+=("$p")
                    fi
                fi
            done
        fi
    done

    # Fallback: controleer mappen met prefs.js als er geen default matches zijn
    if [ ${#PROFIELEN[@]} -eq 0 ]; then
        for base in "${ZOEKPADEN[@]}"; do
            if [ -d "$base" ]; then
                for p in "$base"/*; do
                    if [ -d "$p" ] && [ -f "$p/prefs.js" ]; then
                        PROFIELEN+=("$p")
                    fi
                done
            fi
        done
    fi

    if [ ${#PROFIELEN[@]} -eq 0 ]; then
        echo "    (Geen actieve Firefox profielen gevonden; thema staat klaar in $THEME_SRC)"
        return 0
    fi

    for prof in "${PROFIELEN[@]}"; do
        echo "    -> IE6 thema installeren in profiel: $prof"
        mkdir -p "$prof/chrome"
        cp -rf "$THEME_SRC/"* "$prof/chrome/"

        local UJS="$prof/user.js"
        touch "$UJS"
        if grep -q '^user_pref("toolkit.legacyUserProfileCustomizations.stylesheets"' "$UJS" 2>/dev/null; then
            sed -i 's|^user_pref("toolkit.legacyUserProfileCustomizations.stylesheets".*|user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);|' "$UJS"
        else
            echo 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);' >> "$UJS"
        fi

        if grep -q '^user_pref("browser.tabs.drawInTitlebar"' "$UJS" 2>/dev/null; then
            sed -i 's|^user_pref("browser.tabs.drawInTitlebar".*|user_pref("browser.tabs.drawInTitlebar", false);|' "$UJS"
        else
            echo 'user_pref("browser.tabs.drawInTitlebar", false);' >> "$UJS"
        fi
    done
    echo "    -> Windows XP Internet Explorer 6 thema succesvol geconfigureerd in Firefox."
}

if [ "${1:-}" = "firefox" ]; then
    installeer_firefox_ie6
    echo "Firefox IE6 thema installatie voltooid."
    exit 0
fi

if [ "${1:-}" = "terug" ]; then
    systemctl --user stop plasma-plasmashell 2>/dev/null || true
    [ -f "$RC.voor-xpstart" ] && cp -p "$RC.voor-xpstart" "$RC"
    [ -f "$PANEEL.voor-xpstart" ] && cp -p "$PANEEL.voor-xpstart" "$PANEEL"
    [ -f "$DOLPHIN_RC.voor-xpstart" ] && cp -p "$DOLPHIN_RC.voor-xpstart" "$DOLPHIN_RC"
    [ -f "$DOLPHIN_UI.voor-xpstart" ] && cp -p "$DOLPHIN_UI.voor-xpstart" "$DOLPHIN_UI"
    [ -f "$KVANTUM_CFG.voor-xpstart" ] && cp -p "$KVANTUM_CFG.voor-xpstart" "$KVANTUM_CFG"
    rm -f "$SYS_DESKTOP" "$K/.config/autostart/xp-opstartgeluid.desktop"
    systemctl --user start plasma-plasmashell 2>/dev/null || true
    echo "Originele instellingen zijn hersteld."
    exit 0
fi

echo "==> [1/9] Back-ups maken van huidige configuratie..."
[ -f "$RC" ] && [ ! -f "$RC.voor-xpstart" ] && cp -p "$RC" "$RC.voor-xpstart"
[ -f "$PANEEL" ] && [ ! -f "$PANEEL.voor-xpstart" ] && cp -p "$PANEEL" "$PANEEL.voor-xpstart"
[ -f "$DOLPHIN_RC" ] && [ ! -f "$DOLPHIN_RC.voor-xpstart" ] && cp -p "$DOLPHIN_RC" "$DOLPHIN_RC.voor-xpstart"
[ -f "$DOLPHIN_UI" ] && [ ! -f "$DOLPHIN_UI.voor-xpstart" ] && cp -p "$DOLPHIN_UI" "$DOLPHIN_UI.voor-xpstart"
[ -f "$KVANTUM_CFG" ] && [ ! -f "$KVANTUM_CFG.voor-xpstart" ] && cp -p "$KVANTUM_CFG" "$KVANTUM_CFG.voor-xpstart"

echo "==> [2/9] Windows XP Thema-archieven uitpakken (indien aanwezig in thema-pakket/)..."
mkdir -p "$K/.local/share" "$K/.config" "$XP_SHARE"
if [ -f "$MAP/thema-pakket/xpluna-basis.tar.zst" ]; then
    tar --use-compress-program=zstd -xf "$MAP/thema-pakket/xpluna-basis.tar.zst" -C "$K"
fi
if [ -f "$MAP/thema-pakket/xpluna-icons-basis.tar.zst" ] && [ ! -d "$K/.local/share/icons/XPLuna Icons/scalable/apps" ]; then
    echo "    Uitpakken van XPLuna Icons (basis)..."
    mkdir -p "$K/.local/share/icons"
    tar --use-compress-program=zstd -xf "$MAP/thema-pakket/xpluna-icons-basis.tar.zst" -C "$K/.local/share/icons"
fi
if [ -f "$MAP/thema-pakket/xpluna-icons-mimetypes.tar.zst" ] && [ ! -d "$K/.local/share/icons/XPLuna Icons/scalable/mimetypes" ]; then
    echo "    Uitpakken van XPLuna Icons (mimetypes)..."
    mkdir -p "$K/.local/share/icons"
    tar --use-compress-program=zstd -xf "$MAP/thema-pakket/xpluna-icons-mimetypes.tar.zst" -C "$K/.local/share/icons"
fi

# Zorg dat 3840x2160.png naast bliss.png bestaat in de XPLuna wallpaper-map
if [ -f "$K/.local/share/wallpapers/XPLuna/contents/images/bliss.png" ] && [ ! -f "$K/.local/share/wallpapers/XPLuna/contents/images/3840x2160.png" ]; then
    cp -f "$K/.local/share/wallpapers/XPLuna/contents/images/bliss.png" "$K/.local/share/wallpapers/XPLuna/contents/images/3840x2160.png"
fi

# Installeer originele Windows XP Schaak-gebruikersafbeelding als de gebruiker nog geen avatar heeft
if [ -f "$MAP/thema-pakket/xp-avatar.png" ] && [ ! -f "$K/.face.icon" ]; then
    cp -f "$MAP/thema-pakket/xp-avatar.png" "$K/.face"
    cp -f "$MAP/thema-pakket/xp-avatar.png" "$K/.face.icon"
fi

# Installeer het 1-op-1 Windows XP Welcome / Login / Lockscreen & Splash scherm
if [ -d "$MAP/xp-login-screen" ]; then
    mkdir -p "$K/.local/share/plasma/shells"
    if [ -d "/usr/share/plasma/shells/org.kde.plasma.desktop" ] && [ ! -d "$K/.local/share/plasma/shells/org.kde.plasma.desktop" ]; then
        cp -r /usr/share/plasma/shells/org.kde.plasma.desktop "$K/.local/share/plasma/shells/"
    fi
    mkdir -p "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/images"
    cp -f "$MAP/xp-login-screen/LockScreenUi.qml" "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/LockScreenUi.qml"
    cp -f "$MAP/xp-login-screen/xpConfig.js" "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/xpConfig.js"
    cp -f "$MAP/xp-login-screen/images/"* "$K/.local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/images/"

    mkdir -p "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/images"
    [ -f "/usr/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/LockScreen.qml" ] && cp -f "/usr/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/LockScreen.qml" "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/LockScreen.qml"
    cp -f "$MAP/xp-login-screen/LockScreenUi.qml" "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/LockScreenUi.qml"
    cp -f "$MAP/xp-login-screen/xpConfig.js" "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/xpConfig.js"
    cp -f "$MAP/xp-login-screen/images/"* "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/images/"

    mkdir -p "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/splash/images"
    cp -f "$MAP/xp-login-screen/Splash.qml" "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/splash/Splash.qml"
    cp -f "$MAP/xp-login-screen/xpConfig.js" "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/splash/xpConfig.js"
    cp -f "$MAP/xp-login-screen/images/"* "$K/.local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/splash/images/"

    mkdir -p "$K/.local/share/sddm/themes/XPLuna/assets"
    cp -f "$MAP/xp-login-screen/SddmMain.qml" "$K/.local/share/sddm/themes/XPLuna/Main.qml"
    cp -f "$MAP/xp-login-screen/xpConfig.js" "$K/.local/share/sddm/themes/XPLuna/xpConfig.js"
    cp -f "$MAP/xp-login-screen/images/"* "$K/.local/share/sddm/themes/XPLuna/assets/"
fi

echo "==> [3/9] Tahoma-lettertypen en XP-script installeren..."
mkdir -p "$K/.local/share/fonts/xpstart"
cp -f "$MAP/fonts/"*.ttf "$K/.local/share/fonts/xpstart/"
fc-cache -f "$K/.local/share/fonts" 2>/dev/null || true

cp -f "$MAP/xp-verkenner.py" "$XP_SHARE/xp-verkenner.py"
chmod +x "$XP_SHARE/xp-verkenner.py" "$MAP/xp-verkenner.py"
cp -f "$MAP/package/contents/images/start-normaal.png" "$XP_SHARE/start-groen.png" 2>/dev/null || true

echo "==> [4/9] XPLuna Icons werkbalk-symlinks en Kvantum bijwerken..."
ACT_DIR="$K/.local/share/icons/XPLuna Icons/scalable/actions"
if [ -d "$ACT_DIR" ]; then
    ln -sf ./go-previous.svg "$ACT_DIR/go-previous-symbolic.svg"
    ln -sf ./go-previous.svg "$ACT_DIR/go-previous-view.svg"
    ln -sf ./go-next.svg "$ACT_DIR/go-next-symbolic.svg"
    ln -sf ./go-next.svg "$ACT_DIR/go-next-view.svg"
    ln -sf ../places/folder-upload.svg "$ACT_DIR/go-up.svg"
    ln -sf ../places/folder-upload.svg "$ACT_DIR/go-up-symbolic.svg"
fi

mkdir -p "$K/.config/Kvantum"
cat > "$K/.config/Kvantum/kvantum.kvconfig" << 'EOF'
[General]
theme=XPLuna
EOF
if [ -f "$KVANTUM_CFG" ]; then
    sed -i 's/^toolbar_icon_size=.*/toolbar_icon_size=24/' "$KVANTUM_CFG"
fi

echo "==> [5/9] KDE Thema's, Vensterranden, Cursors, Login-Splash, Lockscreen & XP-Geluiden instellen..."
if command -v kwriteconfig6 >/dev/null 2>&1; then
    # Globale XP Luna look, kleuren, iconen, geluiden en Tahoma-lettertype
    kwriteconfig6 --file kdeglobals --group General --key ColorScheme "XPLuna"
    kwriteconfig6 --file kdeglobals --group General --key font "Tahoma,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group General --key menuFont "Tahoma,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group General --key toolBarFont "Tahoma,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group WM --key activeFont "Tahoma,10,-1,5,700,0,0,0,0,0,0,0,0,0,0,1"
    kwriteconfig6 --file kdeglobals --group KDE --key LookAndFeelPackage "org.magpie.xpluna.desktop"
    kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle "kvantum"
    kwriteconfig6 --file kdeglobals --group Icons --key Theme "XPLuna Icons"
    kwriteconfig6 --file kdeglobals --group Sounds --key Theme "XPLuna Sounds"
    kwriteconfig6 --file kdeglobals --group Sounds --key Enable "true"

    # Windows XP Cursors
    kwriteconfig6 --file kcminputrc --group Mouse --key cursorTheme "XPLuna Cursors"

    # Windows XP Luna Blauwe Vensterranden (Aurorae)
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library "org.kde.kwin.aurorae"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme "__aurorae__svg__XPLuna"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft "M"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight "IAX"

    # Windows XP Plasma Paneelthema
    kwriteconfig6 --file plasmarc --group Theme --key name "XPLuna"

    # Windows XP Boot/Login Splash Screen
    kwriteconfig6 --file ksplashrc --group KSplash --key Engine "KSplashQML"
    kwriteconfig6 --file ksplashrc --group KSplash --key Theme "org.magpie.xpluna.desktop"

    # Windows XP Vergrendelscherm (Bliss achtergrond)
    if [ -f "$K/.local/share/wallpapers/XPLuna/contents/images/bliss.png" ]; then
        kwriteconfig6 --file kscreenlockerrc --group Greeter --key WallpaperPlugin "org.kde.image"
        kwriteconfig6 --file kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image "$K/.local/share/wallpapers/XPLuna/contents/images/bliss.png"
    fi
fi

# Autostart voor het originele Windows XP Opstartgeluid bij inloggen
mkdir -p "$K/.config/autostart"
cat > "$K/.config/autostart/xp-opstartgeluid.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Windows XP Opstartgeluid
Comment=Speelt het originele Windows XP opstartgeluid bij aanmelden
Exec=/bin/sh -c 'sleep 2 && pw-play "$K/.local/share/sounds/XPLuna Sounds/stereo/desktop-login.ogg" 2>/dev/null || pw-play "$K/.local/share/sounds/WinXPsound/stereo/desktop-login-00.wav" 2>/dev/null'
Icon=preferences-desktop-sound
Terminal=false
X-KDE-autostart-phase=2
EOF

echo "==> [6/9] Dolphin configureren als Windows XP Verkenner..."
cat > "$DOLPHIN_RC" << 'EOF'
MenuBar=Enabled

[DetailsMode]
PreviewSize=144

[General]
EditableUrl=true
FilterBar=false
RememberOpenedTabs=false
ShowFullPath=true
ShowFullPathInTitlebar=false
ShowStatusBar=true
ShowZoomSlider=false
Version=202
ViewPropsTimestamp=2026,1,15,15,39,14.766

[IconsMode]
PreviewSize=64
IconSize=48

[KFileDialog Settings]
Places Icons Auto-resize=false
Places Icons Static Size=22

[MainWindow]
MenuBar=Enabled
ToolBarsMovable=Disabled

[PreviewSettings]
Plugins=imagethumbnail,windowsimagethumbnail,rawthumbnail,blenderthumbnail,cursorthumbnail,djvuthumbnail,ebookthumbnail,exrthumbnail,audiothumbnail,heif,jpegthumbnail,opendocumentthumbnail,kraorathumbnail,fontthumbnail,directorythumbnail,mobithumbnail,gsthumbnail,rom-properties,comicbookthumbnail,svgthumbnail,windowsexethumbnail,ffmpegthumbs
EOF

mkdir -p "$(dirname "$DOLPHIN_UI")"
cat > "$DOLPHIN_UI" << 'EOF'
<!DOCTYPE gui>
<gui name="dolphin" translationDomain="kxmlgui6" version="52">
 <MenuBar alreadyVisited="1">
  <Menu alreadyVisited="1" name="file" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;File</text>
   <Action name="file_new"/>
   <Action name="new_menu"/>
   <Action name="new_tab"/>
   <Action name="file_close"/>
   <Separator/>
   <Action name="renamefile"/>
   <Action name="movetotrash"/>
   <Action name="deletefile"/>
   <Separator/>
   <Action name="properties"/>
   <Separator/>
   <Action name="file_quit"/>
  </Menu>
  <Menu alreadyVisited="1" name="edit" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;Edit</text>
   <Action name="edit_undo"/>
   <Action name="edit_redo"/>
   <Separator/>
   <Action name="edit_cut"/>
   <Action name="edit_copy"/>
   <Action name="edit_paste"/>
   <Separator/>
   <Action name="edit_select_all"/>
   <Action name="invert_selection"/>
  </Menu>
  <Menu alreadyVisited="1" name="view" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;View</text>
   <Action name="view_mode"/>
   <Action name="sort"/>
   <Action name="show_preview"/>
   <Action name="show_in_groups"/>
   <Action name="show_hidden_files"/>
   <Separator/>
   <Action name="panels"/>
   <Menu icon="edit-select-text" name="location_bar" noMerge="1">
    <text context="@title:menu" translationDomain="dolphin">Location Bar</text>
    <Action name="editable_location"/>
    <Action name="replace_location"/>
   </Menu>
   <Separator/>
   <Action name="redisplay"/>
  </Menu>
  <Menu alreadyVisited="1" name="go" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;Favorites</text>
   <Action name="go_back"/>
   <Action name="go_forward"/>
   <Action name="go_up"/>
   <Action name="go_home"/>
   <Separator/>
   <Action name="bookmarks"/>
  </Menu>
  <Menu alreadyVisited="1" name="tools" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;Tools</text>
   <Action name="open_preferred_search_tool"/>
   <Action name="open_terminal"/>
   <Action name="compare_files"/>
   <Separator/>
   <Action name="options_configure"/>
  </Menu>
  <Menu name="help" noMerge="1">
   <text translationDomain="kxmlgui6">&amp;Help</text>
   <Action name="help_contents"/>
   <Separator/>
   <Action name="help_about_app"/>
  </Menu>
 </MenuBar>
 <ToolBar alreadyVisited="1" iconSize="24" iconText="icontextright" name="mainToolBar" noMerge="1">
  <text context="@title:menu" translationDomain="dolphin">Main Toolbar</text>
  <Action name="go_back"/>
  <Action name="go_forward"/>
  <Action name="go_up"/>
  <Separator name="separator_0"/>
  <Action name="toggle_search"/>
  <Action name="show_folders_panel"/>
  <Separator name="separator_1"/>
  <Action name="view_mode"/>
  <Separator name="separator_2"/>
  <Action name="url_navigators"/>
 </ToolBar>
 <ActionProperties scheme="Default">
  <Action iconText="Terug" name="go_back" priority="128"/>
  <Action name="go_forward" priority="0"/>
  <Action name="go_up" priority="0"/>
  <Action iconText="Zoeken" name="toggle_search" priority="128"/>
  <Action iconText="Mappen" name="show_folders_panel" priority="128"/>
  <Action name="view_mode" priority="0"/>
 </ActionProperties>
</gui>
EOF

echo "==> [7/9] Snelkoppelingen voor Windows XP Apps, MSN Messenger & Vesktop configureren..."
mkdir -p "$K/.local/share/applications" "$XP_SHARE/sounds"
cp -f "$MAP/xp-verkenner.py" "$XP_SHARE/xp-verkenner.py"
cp -f "$MAP/xp-msn.py" "$XP_SHARE/xp-msn.py" 2>/dev/null || true
[ -d "$MAP/sounds" ] && cp -rf "$MAP/sounds/"* "$XP_SHARE/sounds/" 2>/dev/null || true

cat > "$SYS_DESKTOP" << EOF
[Desktop Entry]
Type=Application
Name=Configuratiescherm
GenericName=Systeeminstellingen
Comment=Windows XP Configuratiescherm
Exec=python3 "$XP_SHARE/xp-verkenner.py" configuratiescherm
Icon=preferences-system
Terminal=false
Categories=Qt;KDE;Settings;
EOF

cat > "$K/.local/share/applications/xp-taakbeheer.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Windows Taakbeheer
GenericName=Taakbeheer
Comment=Windows XP Taakbeheer
Exec=python3 "$XP_SHARE/xp-verkenner.py" taakbeheer
Icon=utilities-system-monitor
Terminal=false
Categories=Qt;KDE;System;
EOF

cat > "$K/.local/share/applications/msn.desktop" << EOF
[Desktop Entry]
Name=MSN Messenger
GenericName=Internet Messenger
Comment=Send instant messages, chat with friends, and see who is online (MSN Messenger 2004)
Exec=python3 "$XP_SHARE/xp-msn.py"
Icon=msn
Terminal=false
Type=Application
Categories=Network;InstantMessaging;
StartupWMClass=xp-msn.py
Keywords=msn;messenger;chat;live;retro;
EOF

cat > "$K/.local/share/applications/dev.vencord.Vesktop.desktop" << EOF
[Desktop Entry]
Categories=Network;InstantMessaging;
Comment=All-in-one voice and text chat (Vesktop)
Exec=flatpak run dev.vencord.Vesktop @@u %U @@
GenericName=Discord
Icon=discord
Keywords=discord;vencord;electron;chat;
MimeType=x-scheme-handler/discord;
Name=Discord
NoDisplay=false
StartupNotify=true
StartupWMClass=vesktop
Terminal=false
Type=Application
X-Desktop-File-Install-Version=0.28
X-Flatpak=dev.vencord.Vesktop
EOF
cp -f "$K/.local/share/applications/dev.vencord.Vesktop.desktop" "$K/.local/share/applications/discord.desktop" 2>/dev/null || true

installeer_vesktop_msn() {
    local THEME_SRC="$MAP/vesktop-theme/Windows-XP-MSN-Messenger.theme.css"
    [ ! -f "$THEME_SRC" ] && return 0

    local CONFIG_DIRS=(
        "$K/.var/app/dev.vencord.Vesktop/config/vesktop"
        "$K/.config/vesktop"
    )

    local GEVONDEN=0
    for VDIR in "${CONFIG_DIRS[@]}"; do
        if [ -d "$VDIR" ] || [ -d "$(dirname "$VDIR")" ]; then
            GEVONDEN=1
            echo "    Vesktop configuratie gedetecteerd in $VDIR..."
            mkdir -p "$VDIR/themes" "$VDIR/settings"

            # 1. Thema installeren in themes/
            cp -f "$THEME_SRC" "$VDIR/themes/Windows-XP-MSN-Messenger.theme.css"

            # 2. OOK direct naar quickCss.css kopiëren voor 100% directe activatie
            cp -f "$THEME_SRC" "$VDIR/settings/quickCss.css"

            # 3. settings.json veilig bijwerken
            python3 - "$VDIR/settings/settings.json" "$VDIR/settings.json" << 'PYEOF'
import sys, json, os

vencord_settings = sys.argv[1]
vesktop_settings = sys.argv[2]

try:
    if os.path.exists(vencord_settings):
        with open(vencord_settings, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {}
    cfg["useQuickCss"] = True
    themes = cfg.get("enabledThemes", [])
    if "Windows-XP-MSN-Messenger.theme.css" not in themes:
        themes.append("Windows-XP-MSN-Messenger.theme.css")
    cfg["enabledThemes"] = themes
    os.makedirs(os.path.dirname(vencord_settings), exist_ok=True)
    with open(vencord_settings, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
except Exception as e:
    print(f"Fout bijwerken Vencord settings: {e}", file=sys.stderr)

try:
    if os.path.exists(vesktop_settings):
        with open(vesktop_settings, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["splashBackground"] = "rgb(236, 233, 216)"
        cfg["splashColor"] = "rgb(0, 25, 97)"
        with open(vesktop_settings, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
except Exception as e:
    pass
PYEOF
            echo "    -> Windows XP MSN Messenger thema & QuickCSS geactiveerd in $VDIR."
        fi
    done

    if [ "$GEVONDEN" -eq 0 ]; then
        echo "    (Vesktop configuratiemap nog niet aanwezig; thema staat klaar in $THEME_SRC)"
    fi
}

installeer_vesktop_msn
installeer_firefox_ie6
kbuildsycoca6 >/dev/null 2>&1 || true

echo "==> [8/9] Plasma 6 Applets installeren (nl.steelhull.xpstart & nl.steelhull.xptray)..."
kpackagetool6 -t Plasma/Applet -u "$MAP/package" 2>/dev/null || kpackagetool6 -t Plasma/Applet -i "$MAP/package"
kpackagetool6 -t Plasma/Applet -u "$MAP/tray-package" 2>/dev/null || kpackagetool6 -t Plasma/Applet -i "$MAP/tray-package"

echo "==> [9/9] Windows XP Taakbalk, Snel starten, Systeemvak & Bliss-bureaublad activeren..."
systemctl --user stop plasma-plasmashell 2>/dev/null || true

python3 - "$RC" "$PANEEL" "$K" << 'PYEOF'
import sys, os, re

rc_path, paneel_path, home_dir = sys.argv[1], sys.argv[2], sys.argv[3]

if os.path.exists(rc_path):
    with open(rc_path, "r") as f:
        rc = f.read()

    # 1. Vind het paneel-containment (bijv. 444 of 2)
    panel_id = "444"
    m_panel = re.search(r'\[Containments\]\[(\d+)\][^\[]*?plugin=org\.kde\.panel', rc, re.S)
    if m_panel:
        panel_id = m_panel.group(1)

    # 2. Vervang standaard startmenu (kickoff/kicker/kickerdash) door nl.steelhull.xpstart
    rc = re.sub(r'(?m)^plugin=org\.kde\.plasma\.(kickoff|kicker|kickerdash)$', 'plugin=nl.steelhull.xpstart', rc)

    # 3. Vervang icontasks door klassieke Windows XP taskmanager met venstertitels
    rc = re.sub(r'(?m)^plugin=org\.kde\.plasma\.icontasks$', 'plugin=org.kde.plasma.taskmanager', rc)
    rc = re.sub(r'(?m)^launchers=.*$', 'launchers=\nmaxStripes=1', rc)
    rc = re.sub(r'(?m)^onlyGroupWhenFull=false$', 'onlyGroupWhenFull=true', rc)

    # 4. Zoek de applet-IDs van xpstart en taskmanager binnen het paneel
    start_id = "445"
    m_start = re.search(rf'\[Containments\]\[{panel_id}\]\[Applets\]\[(\d+)\][^\[]*?plugin=nl\.steelhull\.xpstart', rc, re.S)
    if m_start:
        start_id = m_start.group(1)

    task_id = "447"
    m_task = re.search(rf'\[Containments\]\[{panel_id}\]\[Applets\]\[(\d+)\][^\[]*?plugin=org\.kde\.plasma\.taskmanager', rc, re.S)
    if m_task:
        task_id = m_task.group(1)

    tray_id = "468"
    m_tray = re.search(rf'\[Containments\]\[{panel_id}\]\[Applets\]\[(\d+)\][^\[]*?plugin=nl\.steelhull\.xptray', rc, re.S)
    if m_tray:
        tray_id = m_tray.group(1)

    # 5. Verwijder andere losse paneel-applets (zoals oude systemtray, digitalclock, marginsseparator, pager)
    keep_ids = {start_id, task_id, tray_id}
    blocks = re.split(r'\n(?=\[)', rc)
    filtered_blocks = []
    for b in blocks:
        header = b.split('\n', 1)[0].strip()
        m_app = re.match(rf'^\[Containments\]\[{panel_id}\]\[Applets\]\[(\d+)\]', header)
        if m_app and m_app.group(1) not in keep_ids:
            continue
        filtered_blocks.append(b)
    rc = '\n'.join(filtered_blocks)

    # 6. Voeg nl.steelhull.xptray toe als die er nog niet in staat
    if f"[Containments][{panel_id}][Applets][{tray_id}]" not in rc:
        rc += f"\n\n[Containments][{panel_id}][Applets][{tray_id}]\nimmutability=1\nplugin=nl.steelhull.xptray\n"

    # 7. Zet AppletOrder exact op: Start + Snel starten -> Taakbalkknoppen -> XP Systeemvak
    rc = re.sub(
        rf'(\[Containments\]\[{panel_id}\]\[General\]\s*\nAppletOrder=).*',
        rf'\g<1>{start_id};{task_id};{tray_id}',
        rc
    )

    # 8. Stel de Bliss wallpaper in op alle bureaublad-containments (org.kde.plasma.folder)
    bliss_dir = os.path.join(home_dir, ".local/share/wallpapers/XPLuna")
    if os.path.isdir(bliss_dir):
        for m_desk in re.finditer(r'\[Containments\]\[(\d+)\][^\[]*?plugin=org\.kde\.plasma\.folder', rc, re.S):
            desk_id = m_desk.group(1)
            wp_sec = f"[Containments][{desk_id}][Wallpaper][org.kde.image][General]"
            if wp_sec not in rc:
                rc += f"\n\n{wp_sec}\nImage={bliss_dir}/\n"

    with open(rc_path, "w") as f:
        f.write(rc)

if os.path.exists(paneel_path):
    with open(paneel_path, "r") as f:
        paneel = f.read()
    paneel = re.sub(r'(?m)^floating=1$', 'floating=0', paneel)
    paneel = re.sub(r'(?m)^thickness=\d+$', 'thickness=30', paneel)
    with open(paneel_path, "w") as f:
        f.write(paneel)
PYEOF

qdbus-qt6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
systemctl --user start plasma-plasmashell 2>/dev/null || true

# Speel het Windows XP aanmeldgeluid bij voltooiing!
(pw-play "$K/.local/share/sounds/XPLuna Sounds/stereo/desktop-login.ogg" >/dev/null 2>&1 || true) &
echo "==> Klaar! Bazzite KDE is volledig ingesteld als origineel Windows XP (Luna Blue)."
