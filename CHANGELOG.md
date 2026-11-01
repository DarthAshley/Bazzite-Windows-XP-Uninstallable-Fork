# Changelog — Bazzite Windows XP Suite

All notable changes to the Windows XP Suite for Bazzite / KDE Plasma 6 will be documented in this file.

## [v1.3.0] — 2026-11-01

### 🌐 Firefox Internet Explorer 6 Transformation
- **Authentic IE6 Interface**: Fully transforms Firefox into classic Windows XP Internet Explorer 6 with Luna Blue gradients, embossed toolbar handles, classic navigation buttons (Back, Forward, Stop, Refresh, Home, Search, Favorites), classic address combobox, and status bar.
- **Automated Multi-Profile Installer**: Integrated `installeer_firefox_ie6()` in `installeren.sh` (or standalone `bash installeren.sh firefox`) supporting both native Firefox (`~/.mozilla/firefox/*.default*`) and Bazzite Flatpak Firefox (`~/.var/app/org.mozilla.firefox/`).
- **Configuration & Styling**: Automatically configures `toolkit.legacyUserProfileCustomizations.stylesheets = true` and `browser.tabs.drawInTitlebar = false` in `user.js`.
- **Documentation**: Dedicated guide added in [`FIREFOX-IE6.md`](FIREFOX-IE6.md).

### 💬 Vesktop MSN Messenger 2004 Suite
- **Complete Visual Overhaul**: Fully transforms Vesktop / Discord into MSN Messenger 2004 / Windows Live Messenger with authentic Luna Blue titlebars, tabs, chat textures, buddy lists, retro fonts, and status indicators.
- **Modern Discord Dark Mode Fix**: Overrides all modern Discord design tokens (`--bg-base-primary`, `--bg-surface-raised`, `--bg-mod-faint`, etc.) across `:root`, `.theme-dark`, and `.theme-light` so Discord never reverts to black voids or unstyled areas.
- **QuickCSS & Theme Support**: Automatically installs both to Vencord's `themes/` directory and `settings/quickCss.css` for instant 100% activation.
- **Splash Screen**: Configures Vesktop's loading splash screen to retro `#ece9d8`.
- **Documentation**: Dedicated guide added in [`VESKTOP-MSN.md`](VESKTOP-MSN.md) with recommended Vencord plugins.

### 🎯 System Tray & Taskbar Enhancements
- **Tray Context Menu Centered**: Fixed status notifier context menu positioning in `xp-verkenner.py` using live Gdk X11 root pointer querying (`cx - w // 2`). Menus now open centered directly above clicked tray icons instead of shifting to the left.
- **Borderless XP Popups**: Retained clean borderless Windows XP popup styling without modern window manager titlebars.

### 🪟 Start Menu Visual Polish
- **Icon Fallbacks & Resolvers**: Added `effectiveIconFile` resolver in `AppEntry.qml` supporting Flatpaks (Discord, Lutris, Firefox, IE6) with clean fallback to `application-x-executable` so no app entry ever displays a blank space.
- **Luna Blue Header Gradient**: Replaced flat header with authentic Windows XP Luna Blue gradient (`#0c58e8` -> `#2471f5` -> `#1f6ce6` -> `#0047cc`) with a 1px white highlight line.
- **Crisp Solid Orange Line**: Replaced horizontal gradient glow with a crisp 2px solid orange accent line (`#e5801a`) across the left column, paired with a seamless Luna separator over the right column.
- **User Avatar Frame**: 48x48 avatar frame with a 2px white border and soft outer blue drop shadow.

---

## [v1.2.0] — 2026-11-01
- Pinned and favorite items promoted to the top pinned section of the Start Menu.
- Replaced deprecated package update mechanisms with Bazaar and `ujust update`.
- Added square product logo for OpenDesktop / KDE Store.

## [v1.1.0] — 2026-11-01
- Complete English translation and HD screenshot gallery.
- Live background app tray support for Discord, Steam, and Flatpaks.

## [v1.0.0] — 2026-10-31
- Initial release of Windows XP Professional SP3 Luna & Classic Suite for Bazzite KDE Plasma 6.

