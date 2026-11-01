# 💬 Vesktop & Vencord — Windows XP MSN Messenger 2004 Handleiding

Deze handleiding legt uit hoe het **Windows XP MSN Messenger 2004 thema** en **Vencord plugins** werken binnen **Vesktop** (de privacy- en prestatiegerichte Discord-client met ingebouwde Vencord).

---

## 🧭 Waar vind je de Vencord-instellingen in Vesktop?

In Vesktop zijn alle thema's en plugins ingebouwd via de Vencord-extensie. Je vindt ze als volgt:

1. Open **Discord / Vesktop** (via het Windows XP Startmenu of `flatpak run dev.vencord.Vesktop`).
2. Klik linksonder op het **Tandwieltje** (Gebruikersinstellingen / *User Settings*).
3. Scroll in het linkermenu helemaal naar beneden tot aan de sectie **VENCORD**:
   - **Vencord Settings**: Algemene instellingen, updates en transparantie.
   - **Plugins**: Lijst met meer dan 150 uitbreidingen (schakel hier retro plugins in).
   - **Themes**: Beheer BetterDiscord / Vencord CSS-thema's.
   - **Cloud**: Synchronisatie van instellingen.

---

## 🎨 Hoe werkt het Windows XP MSN Messenger Thema?

### 1. Automatische Installatie
Het installatiescript (`bash installeren.sh`) installeert het thema direct op twee plekken:
- **Themes map**: `~/.var/app/dev.vencord.Vesktop/config/vesktop/themes/Windows-XP-MSN-Messenger.theme.css`
- **QuickCSS**: `~/.var/app/dev.vencord.Vesktop/config/vesktop/settings/quickCss.css`

Omdat het thema ook direct in **QuickCSS** is geplaatst en geactiveerd in `settings.json`, is het thema **meteen 100% actief** zodra je Vesktop opent!

### 2. Oplossing voor het 'Zwarte Scherm' in Modern Discord
Moderne Discord-versies gebruiken nieuwe CSS Design Tokens (`--bg-base-primary`, `--bg-base-secondary`, `--bg-surface-raised`, etc.) en overschrijven de standaard BetterDiscord `--background-primary` variabelen via `.theme-dark`.

Ons gecombineerde thema overschrijft:
1. **Zowel `:root`, `.theme-dark` als `.theme-light`** met de authentieke Windows XP Luna Blue & Beige `#ece9d8` kleurwaarden.
2. **Forced Container Styling**: `#app-mount`, `.appAsidePanelWrapper`, `.layers`, sidebar en instellingenpanelen zijn geforceerd naar `#ece9d8`, en het chatvenster naar `#ffffff`.
3. **Authentieke MSN 7 Grafische Assets**:
   - Originele XP Luna Blue titelbalkknoppen (Minimaliseren, Maximaliseren, Sluiten).
   - MSN Messenger vensterranden en tabbladen.
   - MSN Messenger emoji-, status- en zoekbalkiconen.
   - Chatberichten met de legendarische `[Gebruikersnaam] says:` opmaak.

---

## 🧩 Aanbevolen Vencord Plugins voor de Ultieme Retro Ervaring

Ga naar **User Settings** -> **Plugins** in Vesktop en schakel de volgende plugins in:

| Plugin | Waarom aangeraden? |
| :--- | :--- |
| **`ThemeAttributes`** | Voegt HTML-attributen toe aan Discord-elementen zodat het MSN-thema nog meer specifieke vensterelementen kan stylen. |
| **`CustomRPC`** | Toon in je Discord-status dat je op *"Windows XP SP3 — MSN Messenger 7.0"* chat. |
| **`RelationshipNotifier`** | Krijg direct meldingen als vrienden online komen of contactverzoeken sturen (authentiek MSN-gevoel). |
| **`NoMosaic`** | Voorkomt dat Discord afbeeldingen in een modern raster forceert; toont afbeeldingen klassiek onder elkaar. |
| **`PlainFolderIcon`** | Geeft servermappen een klassiek XP map-uiterlijk. |
| **`PlatformIndicators`** | Toont handige icoontjes naast vrienden om te zien of ze mobiel, desktop of web gebruiken. |
| **`FakeNitro`** | Gebruik custom emoticons en stickers overal, net zoals vroeger op MSN met custom animated emoticons (`(H)`, `(K)`, `(L)`). |
| **`TypingTweaks`** | Zorgt voor subtielere typ-indicatoren onderaan het chatvenster. |
| **`NoProfileThemes`** | Negeert opdringerige custom Nitro profielkleuren van anderen, zodat alles netjes in XP-stijl blijft. |
| **`ClearURLs`** | Verwijdert tracking-parameters uit links voor een schone retro chat. |

---

## 🛠️ Handmatig Aanpassen & Live Herladen

Vesktop ondersteunt live CSS-herladen:
- Druk in Vesktop op **`Ctrl + R`** om de interface direct opnieuw te laden.
- Wil je zelf tweaks toevoegen aan het thema? Bewerk `~/.var/app/dev.vencord.Vesktop/config/vesktop/settings/quickCss.css` en sla op; wijzigingen zijn direct zichtbaar!
