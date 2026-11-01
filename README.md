# 🪟 Bazzite KDE — Windows XP Professional (Luna Blue) Complete Omgeving

Welkom bij het **Bazzite Windows XP Professional (Service Pack 3 - Luna Blue)** totaalpakket voor **Bazzite KDE Plasma 6**!

Dit pakket transformeert een standaard Bazzite KDE Plasma 6 installatie met **één commando** (of via je AI-assistent) naar een authentieke, volledig functionele **Windows XP Professional (Luna Blue)** omgeving.

---

## ✨ Wat zit er allemaal in dit pakket?

1. **Authentiek Windows XP Startmenu (`nl.steelhull.xpstart`)**
   - Groene glanzende **start**-knop met originele Windows XP vlag, hover- en klik-staten en origineel klikgeluid.
   - **Twee-koloms XP Luna opmaak**:
     - **Linkerkolom**: Vastgepinde programma's (*Internet*, *E-mail*) + je eigen favoriete apps met ondertitels.
     - **Rechterkolom**: *Mijn documenten*, *Mijn recente documenten* (met live uitschuifmenu), *Mijn afbeeldingen*, *Mijn muziek*, *Deze computer*, *Configuratiescherm*, *Programmatoegang en -standaardinstellingen*, *Printers en faxen*, *Help en ondersteuning*, *Zoeken* en *Uitvoeren...*.
   - **Alle programma's** met authentiek groen driehoekje en drielaags uitschuifmenu (*Bureau-accessoires*, *Systeemwerkset*, *Ontspanning*, *Spellen*, + al je geïnstalleerde Linux/Flatpak/Steam programma's).
   - **Rechtermuisknop-opties** op elk programma (*Uit deze lijst verwijderen*, *Aan het menu Start vastmaken*, *Toevoegen aan Snel starten*, *Eigenschappen*) én rechtermuisknop op de Startknop (*Verkenner openen*, *Taakbeheer*, *Eigenschappen*).
   - **Schaalbaar vanaf de randen**: sleep de boven- of rechterrand (of de rechterbovenhoek) van het Startmenu om het groter of kleiner te maken.

2. **Werkbalk Snel starten (*Quick Launch*) rechts naast de Startknop**
   - Direct naast de groene `start`-knop en vóór het XP-schuifgreepje:
     - **Bureaublad weergeven** (`show-desktop.svg` — minimaliseert/herstelt direct alle open vensters)
     - **Mozilla Firefox**
     - **Windows Verkenner (Dolphin)**
     - Volledig aanpasbaar vanuit het Startmenu via rechtermuisknop -> *Toevoegen aan / Verwijderen uit Snel starten*.

3. **Windows XP Systeemvak (`nl.steelhull.xptray`) met Live Achtergrond-icoontjes**
   - Lichtblauwe verzonken Windows XP tray rechtsonder in de taakbalk met het ronde `<` pijltje.
   - Toont automatisch **alle actieve achtergrond-apps** (`StatusNotifierItem` via D-Bus), zoals **Discord**, **Steam**, **Unity Hub**, **Easy Effects**, **Browser-meldingen**, inclusief hun echte icoontjes!
   - **Linkermuisknop** op een tray-icoon opent of herstelt het geminimaliseerde venster (bijv. Discord); **rechtermuisknop** opent het bijbehorende contextmenu.
   - Bevat daarnaast de XP-systeemicoontjes voor *Volume*, *Netwerk*, *Energie*, *Hardware veilig verwijderen*, *Windows Beveiliging* en de **Windows XP Klok**.

4. **Windows XP Verkenner, Configuratiescherm & Systeemvensters (`xp-verkenner.py`)**
   - **Configuratiescherm** (`xp-verkenner.py configuratiescherm`): Authentieke XP Categorieweergave (*Vormgeving en thema's*, *Netwerk- en internetverbindingen*, *Software*, *Geluiden, spraak en audioapparaten*, *Prestaties en onderhoud*, *Printers en andere hardware*, *Gebruikersaccounts*, *Datum, tijd, taal en landinstellingen*, *Toegankelijkheidsopties*, *Beveiligingscentrum*) én Klassieke weergave.
   - **Deze computer** (`xp-verkenner.py deze-computer`): Overzicht van *Bestanden die op deze computer zijn opgeslagen*, *Stations met vaste schijven* (inclusief echte schijfruimte van `Lokaal station (C:)` en extra SSD's) en het klassieke blauwe linker zijpaneel (*Systeemtaken*, *Andere locaties*, *Details*).
   - **Systeemeigenschappen** (`xp-verkenner.py systeem`): *Algemeen* (met XP monitor-logo en live CPU/RAM-specificaties van je Bazzite pc), *Computernaam*, *Hardware* (Apparaatbeheer) en *Geavanceerd*.
   - **Eigenschappen voor Beeldscherm** (`xp-verkenner.py beeldscherm`): *Thema's*, *Bureaublad* (achtergrond kiezen), *Schermbeveiliging*, *Vormgeving* (live preview van Actief/Inactief XP-venster) en *Instellingen*.
   - **Eigenschappen voor Taakbalk en het menu Start** (`xp-verkenner.py taakbalk`): Tabbladen *Taakbalk* en *Menu Start*.
   - **Windows Taakbeheer** (`xp-verkenner.py taakbeheer`): Authentiek Windows XP Taakbeheer met de tabbladen *Toepassingen*, *Processen* (met *Proces beëindigen*) en *Prestaties* (met live groene CPU- en wisselbestandsgrafieken op een zwart raster!).
   - **Uitvoeren...** (`xp-verkenner.py uitvoeren`): Klassiek XP Uitvoeren-venster.

5. **Dolphin als Windows XP Verkenner**
   - Geconfigureerd met klassieke menubalk, XP Verkenner knoppenbalk (*Terug*, *Vooruit*, *Omhoog*, *Zoeken*, *Mappen*, *Weergave*) en directe *Locatiebalk* (Adresbalk).

6. **Volledig Thema-, Icoon-, Geluids- en Opstartpakket (`thema-pakket/`)**
   - **3.500+ Originele Windows XP Icoontjes** (`XPLuna` icon pack + mimetypes).
   - **Windows XP Luna Blue Vensterdecoraties** (`Aurorae XPLuna`), **Kvantum XP-stijl**, **Kleurenschema** en **Windows XP Cursors**.
   - **Originele Windows XP Geluiden** (*Windows XP Startup*, *Shutdown*, *Exclamation*, *Error*, *Notify*, *Recycle* en het *Start Navigation* klikgeluid `klick.wav`).
   - **Windows XP Login / Boot Splash Screen** (`LookAndFeel XPLuna`), **Vergrendelscherm**, **Schaker Gebruikersavatar** en de originele **Bliss** bureaubladachtergrond.
   - **Tahoma** lettertypes voor scherpe XP-typografie.

---

## 🚀 Automatische Installatie (1 Commando)

Clone deze repository en voer het installatiescript uit:

```bash
git clone https://github.com/RuisSoftware/Bazzite-Windows-XP.git
cd Bazzite-Windows-XP
bash installeren.sh
```

Het script (`installeren.sh`) pakt automatisch alle thema-archieven uit `thema-pakket/` uit, installeert het Startmenu, de Snel starten-balk, het Systeemvak, de XP Verkenner/Configuratiescherm/Taakbeheer-apps, de XP-geluiden, het opstartscherm, de Bliss-achtergrond en herstart `plasmashell` + `kwin_wayland` met het nieuwe thema.

---

## 🤖 Installeren via een AI-Agent (Claude Code, Antigravity, Cursor, Open Interpreter, etc.)

Gebruik je een AI-assistent op Bazzite? Geef je AI-agent simpelweg de onderstaande prompt (of bekijk `PROMPT-VOOR-AI-AGENT.md`):

> **Prompt voor je AI-Agent:**
> ```text
> Ik wil dat je mijn Bazzite KDE Plasma 6 desktop volledig instelt als originele Windows XP Professional (Luna Blue) met behulp van deze repository: https://github.com/RuisSoftware/Bazzite-Windows-XP (of de bijgevoegde Bazzite-Windows-XP-Compleet.zip).
>
> Voer de volgende stappen volledig zelfstandig voor mij uit:
> 1. Als je de zip hebt gekregen, pak deze dan uit. Als je de GitHub link gebruikt, clone dan https://github.com/RuisSoftware/Bazzite-Windows-XP naar een lokale map.
> 2. Controleer of `zstd`, `tar` en `python3-gobject` aanwezig zijn (standaard aanwezig op Bazzite KDE).
> 3. Voer `bash installeren.sh` uit vanuit de Bazzite-Windows-XP map.
> 4. Controleer of het onderste KDE-paneel aan de linkerkant de Windows XP Startknop + Werkbalk Snel starten (`nl.steelhull.xpstart`) heeft en aan de rechterkant het Windows XP Systeemvak (`nl.steelhull.xptray`). Als er op het paneel nog een oude `org.kde.plasma.kickoff`, `org.kde.plasma.kicker` of dubbele `org.kde.plasma.systemtray` staat, vervang die dan netjes in `~/.config/plasma-org.kde.plasma.desktop-appletsrc` door `nl.steelhull.xpstart` (links) en `nl.steelhull.xptray` (rechts) en herstart `plasmashell --replace`.
> 5. Test of `python3 ~/.local/share/xp-startknop/xp-verkenner.py sni-list` werkt en meld mij zodra mijn volledige Windows XP omgeving klaar is!
> ```
