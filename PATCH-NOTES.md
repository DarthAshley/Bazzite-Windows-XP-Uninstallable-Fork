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

