# 🤖 Windows XP Transformation Prompt for AI Agents

Copy and paste the prompt below into your AI assistant (**Claude Code**, **Google Antigravity**, **Cursor**, **Open Interpreter**, or **Aider**) running on Bazzite Linux:

---

```text
Please configure my Bazzite KDE Plasma 6 desktop as an authentic Windows XP Professional (Luna Blue & Classic) environment using this repository: https://github.com/RuisSoftware/Bazzite-Windows-XP (or Bazzite-Windows-XP-Compleet.zip).

Execute these steps autonomously:
1. Clone https://github.com/RuisSoftware/Bazzite-Windows-XP into a local directory (or extract the zip).
2. Verify that `zstd`, `tar`, and `python3-gobject` (PyGObject) are installed (default on Bazzite KDE).
3. Run `bash installeren.sh` from the repository directory.
4. Ensure the bottom KDE panel has the Windows XP Start Menu + Quick Launch bar (`nl.steelhull.xpstart`) on the left and the Windows XP System Tray (`nl.steelhull.xptray`) on the right. If any legacy widgets (`org.kde.plasma.kickoff`, `org.kde.plasma.kicker`, or duplicate `org.kde.plasma.systemtray`) remain, cleanly configure `~/.config/plasma-org.kde.plasma.desktop-appletsrc` and run `systemctl --user restart plasma-plasmashell.service`.
5. Test that `python3 ~/.local/share/xp-startknop/xp-verkenner.py sni-list` executes properly and returns active system tray applications.
6. Notify me when my complete Windows XP experience is ready!
```

---

## What the Agent Will Configure

- **Start Menu & Quick Launch**: Green 3D Start button, 2-column Luna menu or Classic 1-column menu, Quick Launch icons (*Show Desktop*, *Firefox*, *Explorer*).
- **System Tray**: Windows XP blue notification area (or Classic 3D recessed tray) with clock, volume, network, security center, and live background apps (Discord, Steam, Unity Hub, etc.).
- **Explorer & Control Panel**: Full Windows XP Explorer replica with both Category View and Classic View, System Properties, Display Properties, and Task Manager.
- **Logon & Lock Screen**: Authentic Windows XP Welcome Screen with 3D logo or Classic *Log On to Windows* dialog.
- **Theme, Sounds & Wallpapers**: High-resolution Bliss wallpaper, authentic Windows XP startup/shutdown/click sound scheme, and Luna Blue color palette.
