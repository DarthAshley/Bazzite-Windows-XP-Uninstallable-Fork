# 🤖 Kant-en-klare Prompt voor je AI-Agent (Bazzite KDE -> Windows XP)

Stuur dit bestand (samen met `Bazzite-Windows-XP-Compleet.zip` **óf** de publieke GitHub-link `https://github.com/RuisSoftware/Bazzite-Windows-XP`) naar een vriend met Bazzite KDE. Plak onderstaande prompt in de AI-assistent (zoals Antigravity, Claude Code, Cursor, Windsurf of Open Interpreter) en de AI regelt alles van A tot Z!

---

## 📋 Kopieer en plak deze prompt in je AI-Agent:

```text
Maak van mijn Bazzite KDE Plasma 6 pc een 1-op-1 originele Windows XP Professional (Luna Blue) omgeving, precies zoals geconfigureerd in het Bazzite-Windows-XP pakket.

Gebruik hiervoor:
- GitHub repository: https://github.com/RuisSoftware/Bazzite-Windows-XP
(Of, als ik het zip-bestand `Bazzite-Windows-XP-Compleet.zip` heb meegegeven, pak dat zip-bestand eerst uit.)

Voer zelfstandig de volgende stappen uit zonder mij om tussenstappen te vragen:

1. Clone de repository `https://github.com/RuisSoftware/Bazzite-Windows-XP` (of ga naar de uitgepakte map `Bazzite-Windows-XP`).
2. Voer het hoofdscript uit:
   `bash installeren.sh`
   Dit script installeert automatisch vanuit `thema-pakket/`:
   - Het volledige XPLuna thema (Aurorae XP-vensterranden met rode sluitknop, Kvantum XP-stijl, XP-kleurenschema, XP-cursors, Plasma Luna-paneel, Windows XP opstart-/loginscherm, vergrendelscherm en de originele Bliss bureaubladachtergrond).
   - Alle 3.500+ originele Windows XP icoontjes (`XPLuna` icons + mimetypes).
   - Originele Windows XP geluiden (opstarten, afsluiten, foutmeldingen en het klassieke Start-navigatie klikgeluid `klick.wav`).
   - Tahoma lettertypes in `~/.local/share/fonts/windows-xp`.
   - Dolphin ingesteld als klassieke Windows XP Verkenner (met Terug/Vooruit/Omhoog/Zoeken/Mappen/Weergave-knoppen en adresbalk).
   - Het Windows XP Startmenu + Werkbalk Snel starten (`nl.steelhull.xpstart` — inclusief Bureaublad weergeven, Firefox, Verkenner, schaalbare randen, rechtermuisknopmenu's en het drielaagse Alle programma's-menu).
   - Het Windows XP Systeemvak rechtsonder (`nl.steelhull.xptray` — toont live geminimaliseerde achtergrond-apps zoals Discord, Steam en Easy Effects via D-Bus StatusNotifierItem, plus de XP-systeemicoontjes en klok).
   - De Windows XP Systeemtoepassingen (`~/.local/share/xp-startknop/xp-verkenner.py`):
     * Configuratiescherm (Categorieweergave & Klassieke weergave)
     * Deze computer (met live schijfruimte en XP-zijpaneel)
     * Systeemeigenschappen (met live CPU/RAM-gegevens van deze pc)
     * Eigenschappen voor Beeldscherm (met live XP-venstervoorbeeld en achtergronden)
     * Eigenschappen voor Taakbalk en het menu Start
     * Windows Taakbeheer (Toepassingen, Processen en Prestaties met live groene CPU/RAM-grafieken)
     * Authentiek 'Computer uitschakelen' venster (Stand-by, Uitschakelen, Opnieuw opstarten)
     * Uitvoeren...
   - MSN Messenger 2004 Suite (`~/.local/share/xp-startknop/xp-msn.py` & `msn.desktop`):
     * Authentiek MSN Messenger opstart-/aanmeldscherm met 3D-buddy, statuskeuze en Luna-knoppen.
     * Contactenlijst met profielkaart, aanpasbare persoonlijke boodschap (bijv. "listening 2 music ♫"), zoekbalk en inklapbare groepen (Online, Afwezig, Bezet, Offline).
     * Chatvenster met actiebalk (Uitnodigen, Bestanden, Video, Spelletjes), weergave-afbeeldingen, emoticons en de iconische NUDGE (trillen + nudge.wav!).
     * MSN Toast-notificaties rechtsonderin bij het aanmelden van contacten met online.wav.
   - Discord & Vesktop integratie:
     * "Discord" start automatisch Vesktop (`flatpak run dev.vencord.Vesktop`).
     * "Discord Legacy" start de officiële Discord (`flatpak run com.discordapp.Discord`).
     * Installeert het custom MSN Messenger thema voor Vesktop (`vesktop-theme/Windows-XP-MSN-Messenger.theme.css`).

3. Controleer na `bash installeren.sh` mijn `~/.config/plasma-org.kde.plasma.desktop-appletsrc`:
   - Zorg dat op het onderste taakbalk-paneel helemaal links `nl.steelhull.xpstart` staat (verwijder eventuele standaard `org.kde.plasma.kickoff` of `org.kde.plasma.kicker` en `org.kde.plasma.icontasks` als er al een gewone `org.kde.plasma.taskmanager` met tekstlabels is, of zet `org.kde.plasma.icontasks` om naar `org.kde.plasma.taskmanager` zodat vensters als echte Windows XP taakbalkknoppen met tekst getoond worden).
   - Zorg dat helemaal rechts op het onderste taakbalk-paneel `nl.steelhull.xptray` staat (en verwijder eventuele losse `org.kde.plasma.systemtray` of `org.kde.plasma.digitalclock` zodat ze niet dubbel naast het XP-systeemvak staan).
   - Zet de paneelhoogte op `30` pixels (originele Windows XP taakbalkhoogte).

4. Herstart de desktop-shell netjes via systemd zodat de taakbalk altijd actief blijft:
   `systemctl --user restart plasma-plasmashell.service`

5. Verifieer dat `plasmashell` draait en dat `python3 ~/.local/share/xp-startknop/xp-verkenner.py sni-list` JSON-uitvoer geeft. Geef mij daarna een kort overzicht van wat er is ingesteld!
```

