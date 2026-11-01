# 🪟 Bazzite KDE — Windows XP Professional (Luna Blue & Classic) Complete Omgeving

Welkom bij het **Bazzite Windows XP Professional (Service Pack 3 - Luna Blue & Classic)** totaalpakket voor **Bazzite KDE Plasma 6**!

Dit pakket transformeert een standaard Bazzite KDE Plasma 6 installatie met **één commando** (of via je AI-assistent) naar een authentieke, volledig functionele **Windows XP Professional** omgeving — inclusief uitgebreide instellingen om te schakelen tussen **Windows XP Luna** en **Windows Classic**.

---

## ✨ Wat zit er allemaal in dit pakket?

1. **Authentiek Windows XP Startmenu (`nl.steelhull.xpstart`) — Luna Blue én Classic!**
   - **Windows XP Luna-stijl**: Groene glanzende **start**-knop met originele Windows XP vlag, twee-koloms XP Luna Startmenu met avatar, vastgepinde apps (*Internet*, *E-mail*), je favoriete/meest gebruikte apps (of een vaste eigen lijst!) en de blauwe rechterkolom met alle XP-systeemplaatsen.
   - **Klassieke Windows-stijl (*Classic*)**: Schakel met één klik over naar de klassieke grijze 3D `[ 🪟 Start ]`-knop en het klassieke 1-koloms menu Start met de verticale blauwe **Windows XP Professional** zijbalk!
   - **Alle programma's** met authentiek groen driehoekje en drielaags uitschuifmenu (*Bureau-accessoires*, *Systeemwerkset*, *Ontspanning*, *Communicatie*, + al je geïnstalleerde Linux/Flatpak/Steam programma's) met slimme diagonale muistimers zodat submenu's nooit per ongeluk sluiten.
   - **Schaalbaar vanaf de randen**: sleep de boven- of rechterrand (of de rechterbovenhoek) van het Startmenu om het groter of kleiner te maken.

2. **Uitgebreide Instellingen voor Taakbalk, Menu Start & Aanmeldscherm**
   - Open via **Rechtermuisknop op de Startknop -> Eigenschappen** (of via *Configuratiescherm -> Taakbalk en menu Start* / *Gebruikersaccounts*):
     - **Tabblad `Taakbalk`**:
       - Kies tussen **Windows XP-stijl (Blauw Luna)** en **Klassieke Windows-stijl (Grijs 3D)**.
       - Stel de **taakbalkhoogte & knopgrootte** in: `30 px (Standaard)`, `36 px (Middelgroot)`, `42 px (Groot)` of `48 px (Extra groot)` voor grotere taakbalkknoppen en grotere Snel starten-iconen!
       - Schakel de **Werkbalk Snel starten** en de **Klok** naar wens in of uit.
     - **Tabblad `Menu Start`**:
       - Kies tussen **Menu Start van Windows XP (2 kolommen)** en **Klassiek menu Start (1 kolom met XP-zijbalk)**.
       - Kies tussen **Grote pictogrammen (30 px)** en **Kleine pictogrammen (20 px)** en stel het **aantal getoonde programma's** (`3` t/m `14`) in.
       - Kies welke programma's op de linkerlijst staan:
         1. *Favorieten + Meest gebruikte programma's*
         2. *Alleen Favorieten*
         3. *Alleen Meest gebruikte programma's*
         4. *Vaste eigen lijst* (direct te bewerken in het tekstvak!).
     - **Tabblad `Aanmeldscherm (Logon)`**:
       - Kies tussen het **Windows XP Welkomstscherm** (blauw scherm met het echte 3D Microsoft Windows XP-logo, gebruikerstegels, wachtwoordveld en *welcome*-scherm) en het **Klassieke Aanmeldingsvenster (`Log On to Windows`)** (met de *Microsoft Windows XP Professional x64 Edition* banner, oranje glanslijn en *User name* / *Password* velden).
       - Inclusief directe testknop: **"Aanmeldscherm nu testen (Sla op & vergrendel scherm)"**.

3. **Werkbalk Snel starten (*Quick Launch*) rechts naast de Startknop**
   - Direct naast de `start`-knop: **Bureaublad weergeven**, **Mozilla Firefox**, **Windows Verkenner (Dolphin)** + je eigen toegevoegde apps (via rechtermuisknop in het Startmenu -> *Toevoegen aan Snel starten*).

4. **Windows XP Systeemvak (`nl.steelhull.xptray`) met Live Achtergrond-icoontjes**
   - Lichtblauwe verzonken Windows XP tray (of grijs 3D verzonken in Classic-modus) rechtsonder in de taakbalk met het `<` pijltje.
   - Toont automatisch **alle actieve achtergrond-apps** (`StatusNotifierItem` via D-Bus), zoals **Discord**, **Steam**, **Unity Hub**, **Easy Effects**, inclusief hun echte icoontjes en klik-om-te-herstellen!

5. **Windows XP Verkenner, Configuratiescherm & Systeemvensters (`xp-verkenner.py`)**
   - **Configuratiescherm**, **Deze computer**, **Systeemeigenschappen**, **Eigenschappen voor Beeldscherm**, **Eigenschappen voor Taakbalk, menu Start en Aanmeldscherm**, **Windows Taakbeheer**, **Uitvoeren...** en **Afmelden bij Windows**.

6. **Officiële KDE Store / Pling.com Pakketten (`kde-store-pakketten/`)**
   - Direct klaar om te uploaden naar **[store.kde.org](https://store.kde.org)** en **[pling.com](https://www.pling.com)**! Zie [`KDE-STORE-PUBLICEREN.md`](./KDE-STORE-PUBLICEREN.md) voor alle details.

---

## 🚀 Automatische Installatie (1 Commando)

Clone deze repository en voer het installatiescript uit:

```bash
git clone https://github.com/RuisSoftware/Bazzite-Windows-XP.git
cd Bazzite-Windows-XP
bash installeren.sh
```

---

## 🤖 Installeren via een AI-Agent (Claude Code, Antigravity, Cursor, Open Interpreter, etc.)

Gebruik je een AI-assistent op Bazzite? Geef je AI-agent simpelweg de onderstaande prompt (of bekijk [`PROMPT-VOOR-AI-AGENT.md`](./PROMPT-VOOR-AI-AGENT.md)):

> **Prompt voor je AI-Agent:**
> ```text
> Ik wil dat je mijn Bazzite KDE Plasma 6 desktop volledig instelt als originele Windows XP Professional (Luna Blue & Classic) met behulp van deze repository: https://github.com/RuisSoftware/Bazzite-Windows-XP (of de bijgevoegde Bazzite-Windows-XP-Compleet.zip).
>
> Voer de volgende stappen volledig zelfstandig voor mij uit:
> 1. Als je de zip hebt gekregen, pak deze dan uit. Als je de GitHub link gebruikt, clone dan https://github.com/RuisSoftware/Bazzite-Windows-XP naar een lokale map.
> 2. Controleer of `zstd`, `tar` en `python3-gobject` aanwezig zijn (standaard aanwezig op Bazzite KDE).
> 3. Voer `bash installeren.sh` uit vanuit de Bazzite-Windows-XP map.
> 4. Controleer of het onderste KDE-paneel aan de linkerkant de Windows XP Startknop + Werkbalk Snel starten (`nl.steelhull.xpstart`) heeft en aan de rechterkant het Windows XP Systeemvak (`nl.steelhull.xptray`). Als er op het paneel nog een oude `org.kde.plasma.kickoff`, `org.kde.plasma.kicker` of dubbele `org.kde.plasma.systemtray` staat, vervang die dan netjes in `~/.config/plasma-org.kde.plasma.desktop-appletsrc` door `nl.steelhull.xpstart` (links) en `nl.steelhull.xptray` (rechts) en herstart `systemctl --user restart plasma-plasmashell.service`.
> 5. Test of `python3 ~/.local/share/xp-startknop/xp-verkenner.py sni-list` werkt en meld mij zodra mijn volledige Windows XP omgeving klaar is!
> ```
