# 📝 Patch Notes — Bazzite Windows XP Suite v1.3.2

Welkom bij versie **1.3.2** van de Windows XP Suite voor Bazzite & KDE Plasma 6! Deze release introduceert de volledige **MSN Messenger Multi-Window Suite** met live Discord/Vesktop-integratie en brengt het authentieke MSN van 2004 met losse vensters, live chat en de legendarische Nudge terug op je desktop!

---

### 💬 1. Echte Multi-Window Architectuur voor MSN Messenger & Discord
- **Standalone Buddy List (Contactpersonenlijst)**: Een verticaal venster met profielkaart, statusselector, persoonlijk bericht en categorische vriendenlijsten (`Online`, `Away`, `Busy`, `Offline`).
- **Losse Gespreksvensters per Contact**: Dubbelklikken op een contactpersoon opent een ECHT LOS VENSTER (`[Contact] - Conversation`). Meerdere vensters kunnen gelijktijdig openstaan en hebben elk hun eigen venstertitel en knop op de KDE Plasma taakbalk!
- **100% Replica van de Originele MSN 2004 Gespreksinterface (`media_1793540755051_35913dea.jpg`)**:
  - Luna Blue titelbalk met MSN-icoon en vensterknoppen.
  - Menubalk: `File  Edit  Actions  Tools  Help`.
  - Actiewerkbalk met grote iconen voor `👥 Invite`, `📁 Send Files`, `📹 Webcam`, `🎧 Audio`, `🎲 Fun & Games`, circulaire actieknoppen en het klassieke 4-kleuren `msn` vlinderlogo.
  - Koptekst met `To: [Contact]` en beveiligingsmelding: *"Never give out your password or credit card number in an instant message conversation."*
  - Witte gesprekshistorie met Luna 3D inset border, Tahoma-lettertype en `[Contact] says:` layout.
  - Twee avatarboxen aan de rechterkant (Contact boven met lade-icoontje `>` en de authentieke voetbal op gras; Gebruiker onder met lade-icoontje `>` en de authentieke schaakstukken).
  - Opmaakbalk met `A Font`, `😊 ▾` (emoticon popup met 16 retro smilies), `🖼️ Backgrounds ▾` en de legendarische `⚡ Nudge!`.
  - Tekstinvoer met knipperende cursor en de klassieke Luna `Send` knop.

---

### ⚡ 2. De Legendarische MSN Nudge & Audio Chimes
- **Echte Schuddende Vensters**: Klikken op `⚡ Nudge!` of het ontvangen van een nudge schudt het gespreksvenster met authentieke dempende fysica over het beeldscherm en toont *"--- You have just sent a nudge! ---"*.
- **Originele MSN Geluiden & Custom Chime**: 
  - `LockChime.wav` is geïntegreerd als het heldere, nostalgische nieuwe-berichtgeluid (`msg.wav`).
  - `online.wav` bij het aanmelden en online komen van contacten.
  - De iconische `nudge.wav` zoemer bij het versturen of ontvangen van een nudge.

---

### 🌐 3. Firefox Internet Explorer 6 Volledige Luna Transformatie
- **Forced Luna Beige (#ECE9D8) Light Theme**: Ongeacht of het OS of Firefox in Dark Mode staat, kleurt de volledige browser shell authentiek Windows XP beige.
- **Vaste Menubalk**: `Bestand  Bewerken  Beeld  Geschiedenis  Bladwijzers  Extra  Help` permanent zichtbaar met het geanimeerde Windows IE Flag / Globe throbber-icoon rechts.
- **Navigatiebalk**: Grote retro iconen (Vorige, Volgende, Stop, Vernieuwen, Startpagina, Zoeken, Favorieten, Geschiedenis, Afdrukken) met Luna reliëf.
- **Adresbalk & Koppelingen**: `Adres` label links, witte invoer met combobox dropdown-pijl en de groene `Ga naar` (Go) knop rechts.
- **Map-tabbladen onder de Adresbalk**: Klassieke XP tabbladen met lichte gradiënt voor inactieve tabs en zuiver wit verheven actief tabblad.
- **Statusbalk onderaan**: Vaste balk met status "Gereed" en het blauwe "Internet" zone-icoon.

---

### 🔄 4. Live Discord & Vesktop Integratie via CDP WebSocket
- **Directe Koppeling met Actieve Vesktop Sessie (`http://127.0.0.1:9222`)**:
  - Haalt live het echte gebruikersprofiel (`! Geoffrey`), avatar en statussen op.
  - Synchroniseert alle vrienden en DMs live inclusief online/offline indicatoren en custom actieve statusberichten.
  - Verzenden vanuit het MSN Gespreksvenster verstuurt het bericht direct via Discord (`sendMessage`).
  - Inkomende berichten via Discord worden live binnengehaald via `FluxDispatcher` (`MESSAGE_CREATE`) en getoond in het venster.
  - Buiten actieve vensters verschijnen authentieke slide-up **MSN Toast-meldingen** in de rechterbenedenhoek.

---

# 📝 Patch Notes — Bazzite Windows XP Suite v1.3.1

Welkom bij versie **1.3.1** van de Windows XP Suite voor Bazzite & KDE Plasma 6! Deze release perfectioneert de browser-shell van Firefox (pure IE6 look zonder webpagina's aan te tasten), lost vensterranden op in de afmeld- en afsluitdialogen, perfectioneert de systeemvak-contextmenu positie en zorgt dat Vesktop Vencord-instellingen direct bovenaan toont.

---

### 🌐 1. Firefox Internet Explorer 6 Shell Perfectionering
- **100% Zuivere Browser-Shell**: Geen CSS-hacks meer op websites zelf (sites renderen zoals bedoeld), maar de volledige Firefox-omlijsting is getransformeerd:
  - Bovenin de klassieke Menubalk (`Bestand`, `Bewerken`, `Beeld`, etc.) met rechts de draaiende Windows XP / IE vlag-globe throbber (`throbber.gif` / `throbber_busy.gif`).
  - Grote werkbalk met retro iconen (Vorige, Volgende, Vernieuwen, Startpagina, etc.) en reliëfhandvatten.
  - Brede adresbalk over de volle breedte met "Address" label en "Go" knop.
  - "Links" bladwijzerbalk met authentieke scheiding.
  - Windows XP tabbladen onder de adresbalk geplaatst (zoals klassieke Windows tab-mappen).
  - Authentieke Luna Blue schuifbalken (`scrollbar-color: #5587D8 #ECE9D8`).
- **Geen Verouderde Syntax**: Alle `:-moz-any()` vervangen door moderne `:is()` en `-moz-box-ordinal-group` vervangen door flexbox `order`, waardoor het thema vlekkeloos werkt op moderne Firefox (128+ / 159+ Flatpak en native).

---

### 🔒 2. Vensterloze XP Afmeld- & Afsluitdialogen
- **Geen Aurorae Vensterrand of Titelbalk**: Afmelden (`XpLogoffDialog`) en Afsluiten (`XpTurnOffDialog`) dwingen nu `GDK_BACKEND=x11` af en gebruiken `set_decorated(False)` met dialoog-hints, waardoor KWin geen vensterkaders of Aurorae-knoppen tekent.
- **Cairo Renders Bugfix**: Ontbrekende `import cairo` toegevoegd waardoor de Luna-verloopbalken en 3D-knoppen (Gebruiker wisselen, Afmelden, Stand-by, Uitschakelen, Opnieuw opstarten) vloeiend renderen.

---

### 📍 3. Systeemvak (Tray) Contextmenu Exact Boven Icoon
- **Echte Afmetingen via `get_preferred_size()`**: In plaats van voorlopige allocaties berekent het contextmenu nu de exacte hoogte (174px), zodat het menu direct gecentreerd boven het aangeklikte pictogram zweeft.
- **Precieze Cursoruitlijning**: Gebruikt live muiscoördinaten via `xdotool getmouselocation` en blijft altijd netjes binnen het scherm.

---

### 💬 4. Vesktop / Vencord Instellingen Direct Bovenaan
- **`settingsLocation: "top"`**: Vencord instellingen, Thema's en Plugins staan nu direct bovenaan in het Discord instellingenmenu (boven Account), zodat ze direct vindbaar zijn.
- **Repaired Vencord Cache**: Vencord-injectiebestanden zijn bijgewerkt voor de nieuwste Discord clientversies.

---

### 🎨 5. Startmenu Icon Fallback Garantie
- **Nooit Meer Lege Plekken**: In `AppEntry.qml` schakelt elk pictogram dat niet kan laden direct over naar `Kirigami.Icon` met het originele systeemicoon van de applicatie of de executable fallback.

---

# 📝 Patch Notes — Bazzite Windows XP Suite v1.3.0

Welkom bij versie **1.3.0** van de ultieme Windows XP Suite voor Bazzite & KDE Plasma 6! Deze update brengt volledige transformaties voor Firefox (Internet Explorer 6) en Vesktop (MSN Messenger 2004), lost contextmenu-positionering in het systeemvak op, herstelt ontbrekende pictogrammen in het startmenu en perfectioneert de authentieke Luna Blue afwerking.

---

### 🌐 1. Firefox getransformeerd naar Internet Explorer 6
- **Klassieke IE6 Werkbalken**: Authentieke Luna Blue achtergronden, gegroefde werkbalkhandvatten, grote ronde Vorige/Volgende knoppen, Stop, Vernieuwen, Startpagina, Zoeken, Favorieten en de iconische animatie/globe.
- **Adresbalk & Statusbalk**: Klassieke adrescombobox met groen "Ga naar"-pijltje en onderaan de vertrouwde statusbalk met "Gereed".
- **Automatische Profiel-installatie**: `bash installeren.sh` (of `bash installeren.sh firefox`) installeert het thema automatisch in al je actieve Firefox profielen (zowel native als Flatpak).
- **Documentatie**: Zie [`FIREFOX-IE6.md`](FIREFOX-IE6.md) voor alle details en tips.

---

### 💬 2. Vesktop / Discord omgetoverd tot MSN Messenger 2004
- **Volledig MSN Thema**: Titelbalken met authentieke Windows XP knoppen, tabbladen, chatbalken, retro MSN emoticons en statusindicatoren.
- **Geen Zwarte Schermen Meer**: Alle moderne Discord CSS design tokens (`--bg-base-primary`, etc.) en donkere modus variabelen worden nu overschreven naar retro `#ece9d8` en wit.
- **Direct Actief**: Wordt automatisch geplaatst in zowel de Vencord Themes-map als `quickCss.css`. Zelfs het opstartlaadscherm is afgestemd in XP-kleuren.
- **Documentatie**: Zie [`VESKTOP-MSN.md`](VESKTOP-MSN.md) inclusief de beste retro Vencord plugins.

---

### 🎯 3. Systeemvak (Tray) Contextmenu Positie Gecentreerd
- **Precieze Uitlijning**: Bij het rechtsklikken op systeemvak-iconen (zoals Discord, Steam of geluid) opent het contextmenu nu exact gecentreerd boven het aangeklikte icoon via live X11 muiscoördinaten (`cx - w // 2`).
- **Geen Verspringing Meer**: Het menu schiet niet langer 180px naar links.
- **Strakke Vensterloze XP Popups**: Zonder moderne vensterkaders of Aurorae titelbalken.

---

### 🪟 4. Startmenu Pictogrammen & Kopbalk Perfectionering
- **Geen Lege Iconen Meer**: Dankzij de nieuwe alias-resolver tonen Discord, Lutris en alle andere Flatpaks nu altijd direct hun iconen (met betrouwbare fallback naar `application-x-executable`).
- **Authentieke Luna Blue Kopbalk**: Verloop met 1px glanslijn en 48x48 avatar frame met 2px witte rand en subtiele slagschaduw.
- **Strakke Oranje Accentlijn**: De oranje 2px accentbalk (`#e5801a`) loopt nu strak over de linkerkolom, precies zoals in het originele Windows XP!

---

### 📦 Installatie & Updates
Voer simpelweg uit in de terminal:
```bash
bash installeren.sh
```
Of herstel op elk gewenst moment de standaardinstellingen via:
```bash
bash installeren.sh terug
```

