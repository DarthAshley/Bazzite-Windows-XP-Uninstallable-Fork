# 🌐 Publiceren op Officiële KDE Plasma Theme Sites (`store.kde.org` & `pling.com`)

Ja! Dit thema en alle bijbehorende widgets zijn opgebouwd volgens de **officiële KDE Plasma 6 `KPackage` standaard** (`metadata.json` met `"X-Plasma-API-Minimum-Version": "6.0"` en `"KPackageStructure"`).

Daardoor kun je dit thema direct delen op **[store.kde.org](https://store.kde.org)** en **[pling.com](https://www.pling.com)** — en verschijnt het daarna óók automatisch in KDE Systeeminstellingen onder **"Nieuwe globale thema's ophalen..."** en **"Nieuwe widgets ophalen..."**!

---

## 📦 Kant-en-klare Uploadpakketten (`kde-store-pakketten/`)

In de map [`kde-store-pakketten/`](./kde-store-pakketten/) staan de 4 officiële pakketbestanden klaar om direct te uploaden naar `store.kde.org`:

| Bestand in `kde-store-pakketten/` | Categorie op `store.kde.org` / `pling.com` | Wat zit erin? |
| :--- | :--- | :--- |
| **`nl.steelhull.xpstart.plasmoid`** | **Plasma 6 -> Plasma Widgets -> Application Launchers** | Het volledige **Windows XP Startmenu & Werkbalk Snel starten** (inclusief Luna Blue én Classic modus, eigen instellingenvenster, vliegensvlugge *Alle programma's* en rechtermuisknopmenu). |
| **`nl.steelhull.xptray.plasmoid`** | **Plasma 6 -> Plasma Widgets -> System Information** | Het **Windows XP Systeemvak (Notification Area)** met live achtergrond-apps (Discord, Steam, etc.), XP-geluid/netwerk/schild-icoontjes, Luna & Classic modus en XP-klok. |
| **`org.magpie.xpluna.desktop.tar.gz`** | **Plasma 6 -> Global Themes (Look and Feel)** | Het **Globale Windows XP Thema** inclusief het 1-op-1 **Windows XP Welkomstscherm / Vergrendelscherm** én het **Klassieke 'Log On to Windows' scherm** + echt 3D Microsoft Windows XP-logo. |
| **`XPLuna-SDDM-Plasma6.tar.gz`** | **Plasma 6 -> SDDM Login Themes** | Het **SDDM Aanmeldscherm** met zowel de Windows XP Welcome stijl als de Classic Logon stijl. |

---

## 🚀 Stap-voor-stap Publiceren op `store.kde.org`

1. Maak een gratis account aan op **[store.kde.org](https://store.kde.org)** (of log in via **[pling.com](https://www.pling.com)**).
2. Klik rechtsboven op je profiel -> **Add Product**.
3. Kies als categorie bijvoorbeeld:
   - **KDE Store -> Plasma 6 -> Global Themes (Look and Feel)** (voor het totaalpakket + `org.magpie.xpluna.desktop.tar.gz`)
   - **KDE Store -> Plasma 6 -> Plasma Widgets -> Application Launchers** (voor `nl.steelhull.xpstart.plasmoid`)
4. Upload onder het tabblad **Files** het bijbehorende bestand uit `kde-store-pakketten/` (en eventueel een link naar je GitHub repository `https://github.com/RuisSoftware/Bazzite-Windows-XP` voor het 1-klik Bazzite installatiescript).
5. Voeg screenshots toe van:
   - Het **Windows XP Startmenu + Snel starten + Systeemvak**
   - Het **Windows XP Welkomstscherm (`welcome`)** en het **Klassieke `Log On to Windows` scherm**
   - De **Eigenschappen voor Taakbalk, menu Start en Aanmeldscherm**
6. Klik op **Publish** — je thema staat nu live op `store.kde.org` én is direct vindbaar vanuit KDE Plasma 6!

