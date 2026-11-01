# 🌐 Firefox Windows XP Internet Explorer 6 Thema

Transformeer Mozilla Firefox in een authentieke, pixel-perfecte replica van **Microsoft Internet Explorer 6** op Windows XP!

Dit thema brengt de iconische IE6 werkbalken, reliëf-knoppen, combobox-adresbalk ("Adres"), statusbalk en klassieke tabbladen naar moderne Firefox-versies (zowel Flatpak als native Linux installaties).

---

## 🎨 Kenmerken

- **Originele IE6 Werkbalkknoppen**: Grote kleurrijke knoppen voor *Vorige*, *Volgende*, *Stoppen*, *Vernieuwen*, *Startpagina*, *Zoeken*, *Favorieten*, *Geschiedenis* en *Afdrukken*.
- **Authentieke Adresbalk**: Klassieke verzonken combobox styling met dropdown-pijl en "Ga naar" knop.
- **Identiteitsicoon & Beveiliging**: Klassiek aarde/globe icoontje en Windows XP hangslotjes voor beveiligde verbindingen.
- **Klassieke Tabbladen**: Strakke rechthoekige tabbladen met 3D-randen die naadloos aansluiten op het Windows XP Luna thema.
- **Statusbalk onderaan**: Traditionele 3D statuspaneel-weergave.
- **Ondersteuning voor thema-grepen**: Reliëf handvatten links van werkbalken zoals in Windows XP.

---

## 📁 Bestandsstructuur

Alle themabestanden bevinden zich in de map `firefox-ie6-theme/chrome/`:

| Bestand | Beschrijving |
| :--- | :--- |
| `userChrome.css` | De hoofd-stylesheet die door Firefox geladen wordt en alle modules importeert. |
| `userContent.css` | Stijlen voor interne pagina's en webcontent. |
| `colors.css` | Kleurenvariabelen afgestemd op het Windows XP Luna kleurenpalet. |
| `icons.css` | Werkbalkknoppen en sprite mappings van IE6 pictogrammen. |
| `icon_size.css` | Formaten, marges en uitlijning van knoppen en werkbalken. |
| `identitybox_colors.css` / `identitybox.css` | Globe-icoon en slot-indicatoren in de adresbalk. |
| `locationbar.css` & `urlbar.css` | Stijl voor de URL-invoer en zoekbalk (combobox uiterlijk). |
| `tabs.css` | Vormgeving van de tabbladen en tab-balk. |
| `toolbars.css` | Menubalk, navigatiebalk en werkbalkgrepen (`toolbar_handle`). |
| `statusbar.css` | Statusbalkpaneel aan de onderzijde van het venster. |
| `image/` | Beeldbestanden en sprites (knop-texturen, handvatten, slotjes, throbbers). |

---

## ⚙️ Hoe het werkt

Moderne Firefox-versies ondersteunen aangepaste CSS via de map `chrome/` in het gebruikersprofiel. Om dit te activeren moeten twee instellingen worden ingeschakeld in Firefox:

1. **`toolkit.legacyUserProfileCustomizations.stylesheets` = `true`**  
   Geeft Firefox toestemming om `userChrome.css` en `userContent.css` te laden bij het opstarten.
2. **`browser.tabs.drawInTitlebar` = `false`**  
   Zorgt dat Firefox de tabbladen onder de menubalk en werkbalk plaatst, en de klassieke venstertitelbalk behoudt.

Deze instellingen worden automatisch geschreven naar het configuratiebestand `user.js` in uw Firefox profiel.

---

## 🚀 Snelle Installatie

### Optie 1: Automatisch via het hoofdscript
Het thema wordt automatisch geïnstalleerd bij het uitvoeren van het centrale script van deze repository:
```bash
bash installeren.sh
```

### Optie 2: Alleen het Firefox IE6 thema installeren
Wilt u uitsluitend Firefox omtoveren zonder de rest van uw bureaublad te wijzigen:
```bash
bash installeren.sh firefox
```
Het script detecteert automatisch al uw actieve Firefox-profielen (zowel **Flatpak** `org.mozilla.firefox` als **native Linux** `~/.mozilla/firefox/`).

---

## 🛠️ Handmatige Installatie

Wilt u het thema liever handmatig installeren in een specifiek profiel:

1. **Vind uw Firefox profielmap**:
   - Open Firefox en typ `about:profiles` in de adresbalk.
   - Zoek het profiel met de melding *"Dit is het momenteel gebruikte profiel"*.
   - Klik op **Map openen** bij de *Hoofdmap* (Root Directory).
   - *Typische paden op Bazzite / Fedora:*
     - Flatpak: `~/.var/app/org.mozilla.firefox/.mozilla/firefox/<profiel-naam>/`
     - Native: `~/.mozilla/firefox/<profiel-naam>/`

2. **Kopieer de bestanden**:
   - Maak in die profielmap een submap aan genaamd `chrome`:
     ```bash
     mkdir -p ~/.var/app/org.mozilla.firefox/.mozilla/firefox/<profiel>/chrome
     ```
   - Kopieer de volledige inhoud van `firefox-ie6-theme/chrome/` naar die nieuwe `chrome/` map:
     ```bash
     cp -rf "firefox-ie6-theme/chrome/"* ~/.var/app/org.mozilla.firefox/.mozilla/firefox/<profiel>/chrome/
     ```

3. **Activeer custom stylesheets**:
   - Open of maak het bestand `user.js` in uw profielmap en voeg toe:
     ```javascript
     user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
     user_pref("browser.tabs.drawInTitlebar", false);
     ```

4. **Herstart Firefox**:
   - Sluit Firefox volledig af (`Alt + F4` of via het menu) en start de browser opnieuw.

---

## 💡 Aanbevolen Firefox Instellingen voor het Echte IE6 Gevoel

Voor de meest authentieke ervaring:
1. **Menubalk activeren**: Klik met de rechtermuisknop op een lege plek op de werkbalk (of druk op `Alt`) en vink **Menubalk** aan.
2. **Knoppen aanpassen**: Klik met de rechtermuisknop op de werkbalk en kies **Werkbalk aanpassen...**. Plaats *Vorige*, *Volgende*, *Stoppen*, *Vernieuwen*, *Startpagina* en de *Adresbalk* in de gewenste klassieke volgorde.
3. **Bladwijzerbalk**: Vink via het werkbalkmenu ook de **Bladwijzerwerkbalk** aan ("Koppelingen" in IE6).

---

## 🗑️ De-installatie / Herstellen naar Standaard

Om terug te keren naar het standaard uiterlijk van Firefox:

1. Verwijder de `chrome` map uit uw profiel:
   ```bash
   rm -rf ~/.var/app/org.mozilla.firefox/.mozilla/firefox/*.default*/chrome
   rm -rf ~/.mozilla/firefox/*.default*/chrome
   ```

2. (Optioneel) Zet in `user.js` in uw profiel de instelling terug:
   ```javascript
   user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", false);
   ```

3. Herstart Firefox. De browser start weer op met het moderne uiterlijk.
