# 🛒 Publishing Bazzite Windows XP to KDE Store & Pling.com

All official packages are pre-built and packaged inside the `kde-store-pakketten/` directory, ready for direct upload to **[store.kde.org](https://store.kde.org)** and **[pling.com](https://www.pling.com)**.

---

## 📦 Package Overview

| File | Store Category | Target ID | Description |
|---|---|---|---|
| `nl.steelhull.xpstart.plasmoid` | **Plasma 6 Applets** | `nl.steelhull.xpstart` | Windows XP Luna & Classic Start Menu + Quick Launch |
| `nl.steelhull.xptray.plasmoid` | **Plasma 6 Applets** | `nl.steelhull.xptray` | Windows XP Luna & Classic System Tray with Live App Icons |
| `org.magpie.xpluna.desktop.tar.gz` | **Plasma 6 Global Themes** | `org.magpie.xpluna.desktop` | Windows XP Luna Global Theme, Sound Scheme & Lock Screen |

---

## 📤 Step-by-Step Upload Instructions

### 1. Log In to the KDE Store
1. Visit **[store.kde.org](https://store.kde.org)** (or **[pling.com](https://www.pling.com)**).
2. Log in or create an account.
3. Click your profile avatar in the upper right and select **Add Product**.

### 2. Uploading the Start Menu Plasmoid
1. Select **Plasma 6 Applets** as the category.
2. Enter **Title**: `Windows XP Luna & Classic Start Menu (with Quick Launch)`.
3. Set **Version**: `2.0`.
4. Upload `kde-store-pakketten/nl.steelhull.xpstart.plasmoid`.
5. Upload screenshot previews from `screenshots/01-desktop-startmenu-luna.png` and `screenshots/05-classic-startmenu-taskbar.png`.
6. Add GitHub repository link: `https://github.com/RuisSoftware/Bazzite-Windows-XP`.

### 3. Uploading the System Tray Plasmoid
1. Select **Plasma 6 Applets** as the category.
2. Enter **Title**: `Windows XP Luna & Classic Notification Area (System Tray)`.
3. Set **Version**: `2.0`.
4. Upload `kde-store-pakketten/nl.steelhull.xptray.plasmoid`.
5. Upload screenshot preview from `screenshots/01-desktop-startmenu-luna.png` (or a tray close-up).

### 4. Uploading the Global Theme
1. Select **Plasma 6 Global Themes** as the category.
2. Enter **Title**: `Windows XP Professional Luna Blue & Classic Suite`.
3. Set **Version**: `2.0`.
4. Upload `kde-store-pakketten/org.magpie.xpluna.desktop.tar.gz`.
5. Upload all screenshots from `screenshots/`.

---

## 🔄 Rebuilding Packages Locally

To re-package the latest code into `.plasmoid` archives, run:

```bash
# Start menu
cd package && zip -r ../kde-store-pakketten/nl.steelhull.xpstart.plasmoid . && cd ..

# System tray
cd tray-package && zip -r ../kde-store-pakketten/nl.steelhull.xptray.plasmoid . && cd ..

# Global theme
tar -czvf kde-store-pakketten/org.magpie.xpluna.desktop.tar.gz -C ~/.local/share/plasma/look-and-feel/ org.magpie.xpluna.desktop
```

