#!/usr/bin/env python3
"""
Windows XP Verkenner, Configuratiescherm, Systeemeigenschappen en Uitvoeren
voor Bazzite KDE (XP Start).
Gebruik:
  xp-verkenner.py [computer | configuratiescherm | klassiek | systeem | uitvoeren]
"""
import os
import sys

# Force X11 backend for popup context menu and tray menus so KWin doesn't decorate with Aurorae
if len(sys.argv) > 1 and sys.argv[1].lower() in ("sni-menu",) and os.environ.get("GDK_BACKEND") != "x11":
    os.environ["GDK_BACKEND"] = "x11"
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        pass

import json
import shutil
import subprocess
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib, Gio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "package", "contents", "images", "icons")
if not os.path.isdir(ICONS_DIR):
    ICONS_DIR = os.path.expanduser(
        "~/.local/share/plasma/plasmoids/nl.steelhull.xpstart/contents/images/icons"
    )

REAL_SYSTEMSETTINGS = "/usr/bin/systemsettings"


def load_pixbuf(name, size=32):
    path = os.path.join(ICONS_DIR, name)
    if os.path.exists(path):
        try:
            return GdkPixbuf.Pixbuf.new_from_file_at_size(path, size, size)
        except Exception:
            pass
    theme = Gtk.IconTheme.get_default()
    try:
        return theme.load_icon(name.replace(".svg", ""), size, 0)
    except Exception:
        return None


def make_icon(name, size=32):
    pb = load_pixbuf(name, size)
    if pb is not None:
        return Gtk.Image.new_from_pixbuf(pb)
    return Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.BUTTON)


def run_cmd(cmd):
    if isinstance(cmd, str):
        subprocess.Popen(["/bin/sh", "-c", cmd], start_new_session=True)
    else:
        subprocess.Popen(cmd, start_new_session=True)


def play_xp_sound(name="klick.wav"):
    for snd_dir in (
        os.path.expanduser("~/.local/share/sounds/WinXPsound/stereo"),
        os.path.expanduser("~/.local/share/sounds/XPLuna Sounds/stereo"),
    ):
        snd_path = os.path.join(snd_dir, name)
        if os.path.exists(snd_path):
            subprocess.Popen(
                ["pw-play", snd_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return


def open_in_dolphin(path):
    run_cmd(["dolphin", path])


def get_disk_usage_str(path):
    try:
        usage = shutil.disk_usage(path)
        total_gb = usage.total / (1024 ** 3)
        free_gb = usage.free / (1024 ** 3)
        return f"Total Size: {total_gb:.1f} GB\nFree Space: {free_gb:.1f} GB"
    except Exception:
        return "System Folder"


XP_CSS = b"""
* {
    font-family: "Tahoma", "Noto Sans", sans-serif;
    font-size: 11px;
}

window, .xp-window {
    background-color: #ece9d8;
    color: #000000;
}

/* Menubar */
.xp-menubar {
    background-color: #ece9d8;
    border-bottom: 1px solid #d8d2bd;
    padding: 0px;
}
.xp-menubar-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 0px;
    padding: 3px 7px;
    color: #000000;
    box-shadow: none;
}
.xp-menubar-btn:hover {
    background-color: #316ac5;
    color: #ffffff;
}

/* Authentic Windows XP Context Menu */
.xp-popup-menu {
    background-color: #ffffff;
    border: 1px solid #716f64;
    padding: 2px 1px;
}
.xp-popup-item {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 0px;
    padding: 4px 22px 4px 18px;
    color: #000000;
    font-family: 'Tahoma', 'Segoe UI', sans-serif;
    font-size: 11px;
    box-shadow: none;
}
.xp-popup-item:hover {
    background-color: #316ac5;
    color: #ffffff;
}
.xp-popup-sep {
    background-color: #aca899;
    border-bottom: 1px solid #ffffff;
    min-height: 1px;
    margin: 3px 2px;
}
.xp-flag-box {
    background-color: #ffffff;
    border-left: 1px solid #d8d2bd;
    padding: 2px 8px;
}

/* Standard Buttons Toolbar */
.xp-toolbar {
    background-image: linear-gradient(to bottom, #f6f4ec, #ece9d8);
    border-top: 1px solid #ffffff;
    border-bottom: 1px solid #d8d2bd;
    padding: 2px 4px;
}
.xp-toolbtn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 2px 6px;
    color: #000000;
    box-shadow: none;
}
.xp-toolbtn:hover {
    background-image: linear-gradient(to bottom, #ffffff, #e3dfce);
    border-color: #c2bda9;
}
.xp-toolbtn:active {
    background-image: linear-gradient(to bottom, #dbd7c5, #ebe8d8);
    border-color: #9e9a8b;
}
.xp-toolbtn-disabled {
    opacity: 0.48;
}
.xp-vsep {
    background-color: #c5c2b2;
    min-width: 1px;
    margin: 3px 4px;
}

/* Address Bar */
.xp-addressbar {
    background-color: #ece9d8;
    border-top: 1px solid #ffffff;
    border-bottom: 2px solid #d4d0c2;
    padding: 1px 4px;
}
.xp-address-label {
    color: #44423b;
    padding: 0px 6px 0px 4px;
}
.xp-address-box {
    background-color: #ffffff;
    border: 1px solid #7f9db9;
    padding: 1px 4px;
}
.xp-address-entry {
    background: #ffffff;
    border: none;
    box-shadow: none;
    color: #000000;
    padding: 1px 4px;
    min-height: 18px;
}
.xp-go-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 2px;
    padding: 1px 6px;
    box-shadow: none;
}
.xp-go-btn:hover {
    border-color: #9e9a8b;
    background-color: #f4f2e8;
}

/* Left Explorer Task Pane */
.xp-sidebar {
    background-image: linear-gradient(to bottom, #7ba2e7, #6375d6);
    padding: 12px 10px;
}
.xp-card-header-dark {
    background-image: linear-gradient(to right, #2058c8, #2b71e2);
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 4px 8px;
    color: #ffffff;
    font-weight: bold;
}
.xp-card-header-light {
    background-image: linear-gradient(to right, #ffffff, #c7d4f7);
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 4px 8px;
    color: #215dc6;
    font-weight: bold;
}
.xp-card-body {
    background-color: #d6dff7;
    border-left: 1px solid #ffffff;
    border-right: 1px solid #ffffff;
    border-bottom: 1px solid #ffffff;
    padding: 8px 10px;
}
.xp-task-link {
    background: transparent;
    border: none;
    box-shadow: none;
    padding: 2px 2px;
    color: #215dc6;
}
.xp-task-link:hover {
    color: #428eff;
    text-decoration: underline;
}
.xp-chevron-btn {
    background-color: #ffffff;
    border: 1px solid #4a70c0;
    border-radius: 10px;
    min-width: 17px;
    min-height: 17px;
    padding: 0px;
    color: #215dc6;
    font-weight: bold;
    font-size: 9px;
}

/* Right Content: White Explorer View */
.xp-white-view {
    background-color: #ffffff;
}
.xp-section-title {
    color: #000000;
    font-weight: bold;
    font-size: 11px;
    padding: 8px 0px 2px 12px;
}
.xp-section-line {
    background-image: linear-gradient(to right, #709fd9, #ffffff 85%);
    min-height: 1px;
    margin: 0px 12px 8px 12px;
}
.xp-item-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 2px;
    padding: 6px 10px;
    color: #000000;
    box-shadow: none;
}
.xp-item-btn:hover {
    background-color: #e8f0fc;
    border-color: #98b8e8;
}
.xp-item-selected {
    background-color: #316ac5;
    color: #ffffff;
}

/* Right Content: Category View (Control Panel) */
.xp-cat-view {
    background-color: #6375d6;
    background-image: linear-gradient(135deg, #6375d6 0%, #5666c6 70%, #4d5cb8 100%);
}
.xp-cat-heading {
    color: #dce4fc;
    font-size: 22px;
    font-weight: bold;
    padding: 16px 24px 10px 24px;
}
.xp-cat-subhead {
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
    padding: 8px 24px 4px 24px;
}
.xp-cat-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 8px 12px;
    color: #ffffff;
    box-shadow: none;
}
.xp-cat-btn:hover {
    background-color: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.28);
}
.xp-cat-title {
    color: #ffffff;
    font-weight: bold;
    font-size: 12px;
}
.xp-cat-desc {
    color: #d6dff7;
    font-size: 11px;
}

/* Classic Control Panel Grid */
.xp-classic-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 2px;
    padding: 6px 4px;
    color: #000000;
    box-shadow: none;
}
.xp-classic-btn:hover {
    background-color: #316ac5;
    color: #ffffff;
}

/* Dialog / System Properties */
.xp-tab-bar {
    padding: 0px;
}
.xp-tab-btn {
    background-image: linear-gradient(to bottom, #ffffff, #ece9d8);
    border: 1px solid #919b9c;
    border-bottom: none;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    padding: 3px 9px;
    color: #000000;
    box-shadow: none;
}
.xp-tab-active {
    background-image: linear-gradient(to bottom, #ffb74c 0%, #ffffff 18%, #fcfcfe 100%);
    border-color: #919b9c;
    font-weight: bold;
}
.xp-tab-page {
    background-color: #fcfcfe;
    border: 1px solid #919b9c;
    padding: 14px;
}
.xp-push-btn {
    background-image: linear-gradient(to bottom, #ffffff, #e3dfce);
    border: 1px solid #003c74;
    border-radius: 3px;
    padding: 3px 14px;
    min-width: 75px;
    color: #000000;
    box-shadow: inset 0 0 0 1px #d6e4f8;
}
.xp-push-btn:hover {
    box-shadow: inset 0 0 0 2px #f8b334;
}
.xp-status-bar {
    background-color: #ece9d8;
    border-top: 1px solid #d0ccb8;
    padding: 2px 8px;
    color: #333333;
}

entry, textview, textview text, spinbutton, treeview, .view {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #7f9db9;
}

treeview header button {
    background-image: linear-gradient(to bottom, #ffffff, #ece9d8);
    color: #000000;
    border: 1px solid #d0ccb8;
    padding: 2px 6px;
}

combobox button.combo {
    background-image: linear-gradient(to bottom, #ffffff, #ece9d8);
    color: #000000;
    border: 1px solid #7f9db9;
    padding: 2px 6px;
}

notebook, notebook stack {
    background-color: #fcfcfe;
    color: #000000;
    border: 1px solid #919b9c;
}

notebook header {
    background-color: #ece9d8;
}

notebook header tabs tab {
    background-image: linear-gradient(to bottom, #ffffff, #ece9d8);
    color: #000000;
    border: 1px solid #919b9c;
    padding: 3px 8px;
}

notebook header tabs tab:checked {
    background-image: linear-gradient(to bottom, #ffb74c 0%, #ffffff 18%, #fcfcfe 100%);
    font-weight: bold;
}

frame > border {
    border: 1px solid #d0d0bf;
    border-radius: 3px;
}
"""

CLASSIC_ITEMS = [
    ("Accessibility\nOptions", "cat-access.svg", "kcmshell6 kcm_access"),
    ("Add or Remove\nPrograms", "cat-software.svg", "bazaar || konsole -e ujust update"),
    ("Administrative\nTools", "cp-admin.svg", "plasma-systemmonitor"),
    ("Appearance and\nThemes", "cat-appearance.svg", "__BEELDSCHERM__"),
    ("Bluetooth\nDevices", "tray-bt.svg", "kcmshell6 kcm_bluetooth"),
    ("Date and Time", "cat-datetime.svg", "kcmshell6 kcm_clock"),
    ("Display", "cp-display.svg", "__BEELDSCHERM__"),
    ("Folder Options", "cp-folderopts.svg", "kcmshell6 kcm_filetypes"),
    ("Fonts", "cp-fonts.svg", "kcmshell6 kcm_fontinst"),
    ("Game\nControllers", "cp-gamepad.svg", "kcmshell6 kcm_gamecontroller"),
    ("Internet\nOptions", "cat-network.svg", "kcmshell6 kcm_proxy"),
    ("Keyboard", "cp-keyboard.svg", "kcmshell6 kcm_keyboard"),
    ("Mouse", "cp-mouse.svg", "kcmshell6 kcm_mouse"),
    ("Network\nConnections", "cp-network.svg", "kcmshell6 kcm_networkmanagement"),
    ("Power Options", "cp-power.svg", "kcmshell6 kcm_powerdevilprofilesconfig"),
    ("Printers and\nFaxes", "printers.svg", "kcmshell6 kcm_printer_manager"),
    ("Program Access\nand Defaults", "defapps.svg", "kcmshell6 kcm_componentchooser"),
    ("Regional and\nLanguage Options", "defapps.svg", "kcmshell6 kcm_regionandlang"),
    ("Scanners and\nCameras", "pics.svg", "kcmshell6 kcm_kamera"),
    ("Scheduled\nTasks", "cp-updates.svg", "kcmshell6 kcm_autostart"),
    ("Security\nCenter", "xp-shield.svg", "bazaar || konsole -e ujust update"),
    ("Sounds and\nAudio Devices", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
    ("Speech", "cp-speech.svg", "kcmshell6 kcm_soundtheme"),
    ("System", "cp-system.svg", "__SYSTEEM__"),
    ("Taskbar and\nStart Menu", "cp-taskbar.svg", "__TAAKBALK__"),
    ("User Accounts", "cat-users.svg", "__LOGON__"),
    ("Windows\nFirewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
    ("Wireless\nNetwork Setup", "cp-wireless.svg", "kcmshell6 kcm_networkmanagement"),
]

CATEGORIES = [
    (
        "Appearance and Themes",
        "cat-appearance.svg",
        "Change the computer's theme, desktop background, or screen resolution",
        [
            ("Change the computer's theme", "cat-appearance.svg", "__BEELDSCHERM__"),
            ("Change the desktop background", "cp-display.svg", "kcmshell6 kcm_wallpaper"),
            ("Change the screen resolution", "cp-display.svg", "kcmshell6 kcm_kscreen"),
            ("Display", "cp-display.svg", "__BEELDSCHERM__"),
            ("Taskbar and Start Menu", "cp-taskbar.svg", "__TAAKBALK__"),
            ("Folder Options", "cp-folderopts.svg", "kcmshell6 kcm_filetypes"),
            ("Fonts", "cp-fonts.svg", "kcmshell6 kcm_fontinst"),
        ],
    ),
    (
        "Printers and Other Hardware",
        "cat-printers.svg",
        "Configure printers, mouse, keyboard, game controllers, and Bluetooth devices",
        [
            ("View installed printers or fax printers", "printers.svg", "kcmshell6 kcm_printer_manager"),
            ("Add a printer", "printers.svg", "kcmshell6 kcm_printer_manager"),
            ("Mouse", "cp-mouse.svg", "kcmshell6 kcm_mouse"),
            ("Keyboard", "cp-keyboard.svg", "kcmshell6 kcm_keyboard"),
            ("Game Controllers", "cp-gamepad.svg", "kcmshell6 kcm_gamecontroller"),
            ("Bluetooth Devices", "tray-bt.svg", "kcmshell6 kcm_bluetooth"),
        ],
    ),
    (
        "Network and Internet Connections",
        "cat-network.svg",
        "Connect to the Internet and home network, configure firewall and network adapters",
        [
            ("Set up or change your Internet connection", "cat-network.svg", "kcmshell6 kcm_networkmanagement"),
            ("Network Connections", "cp-network.svg", "kcmshell6 kcm_networkmanagement"),
            ("Wireless Network Setup Wizard", "cp-wireless.svg", "kcmshell6 kcm_networkmanagement"),
            ("Windows Firewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
            ("Internet Options", "cat-network.svg", "kcmshell6 kcm_proxy"),
        ],
    ),
    (
        "User Accounts",
        "cat-users.svg",
        "Change user accounts, passwords, and logon options (XP Welcome Screen vs Classic Logon)",
        [
            ("Change the way users log on or off (XP Welcome Screen / Classic Logon)", "cat-users.svg", "__LOGON__"),
            ("Change an account", "cat-users.svg", "kcmshell6 kcm_users"),
            ("Create a new account", "cat-users.svg", "kcmshell6 kcm_users"),
            ("Login Screen (SDDM)", "cat-users.svg", "kcmshell6 kcm_plasmalogin"),
        ],
    ),
    (
        "Add or Remove Programs",
        "cat-software.svg",
        "Install, update, or remove programs and Windows components",
        [
            ("Change or remove programs", "cat-software.svg", "bazaar || konsole -e ujust update"),
            ("Add new programs", "cat-software.svg", "bazaar || konsole -e ujust update"),
            ("Set Program Access and Defaults", "defapps.svg", "kcmshell6 kcm_componentchooser"),
        ],
    ),
    (
        "Date, Time, Language, and Regional Options",
        "cat-datetime.svg",
        "Change date, time, time zone, language, and number formats",
        [
            ("Change the date and time", "cat-datetime.svg", "kcmshell6 kcm_clock"),
            ("Change the format of numbers, dates, and times", "defapps.svg", "kcmshell6 kcm_regionandlang"),
            ("Date and Time", "cat-datetime.svg", "kcmshell6 kcm_clock"),
            ("Regional and Language Options", "defapps.svg", "kcmshell6 kcm_regionandlang"),
        ],
    ),
    (
        "Sounds, Speech, and Audio Devices",
        "cat-sound.svg",
        "Change the speaker volume and sound scheme, configure speakers and microphone",
        [
            ("Adjust the system volume", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
            ("Change the sound scheme", "cp-speech.svg", "kcmshell6 kcm_soundtheme"),
            ("Sounds and Audio Devices", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
        ],
    ),
    (
        "Accessibility Options",
        "cat-access.svg",
        "Adjust computer contrast, sound, and mouse behavior for vision, hearing, and mobility",
        [
            ("Configure accessibility options", "cat-access.svg", "kcmshell6 kcm_access"),
            ("Adjust screen color and night light", "cp-display.svg", "kcmshell6 kcm_nightlight"),
        ],
    ),
    (
        "Performance and Maintenance",
        "cat-perf.svg",
        "See basic information about your computer, free up disk space, power options, and system tasks",
        [
            ("See basic information about your computer", "cp-system.svg", "__SYSTEEM__"),
            ("Adjust visual effects", "cat-appearance.svg", "kcmshell6 kcm_animations"),
            ("Free up space on your hard disk / System Monitor", "cp-clean.svg", "plasma-systemmonitor"),
            ("System", "cp-system.svg", "__SYSTEEM__"),
            ("Power Options", "cp-power.svg", "kcmshell6 kcm_powerdevilprofilesconfig"),
            ("Administrative Tools", "cp-admin.svg", "plasma-systemmonitor"),
        ],
    ),
    (
        "Security Center",
        "xp-shield.svg",
        "Check the status of your computer's security settings, firewall, and Automatic Updates",
        [
            ("Windows Firewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
            ("Automatic Updates", "cp-updates.svg", "bazaar || konsole -e ujust update"),
            ("Application Permissions", "xp-shield.svg", "kcmshell6 kcm_app-permissions"),
        ],
    ),
]


def get_cpu_and_ram():
    cpu_model = "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    cpu_model = line.split(":", 1)[1].strip()
                    break
    except Exception:
        pass
    ram_gb = "16,0 GB RAM"
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    gb = round(kb / (1024 * 1024), 1)
                    ram_gb = f"{str(gb).replace('.', ',')} GB RAM"
                    break
    except Exception:
        pass
    return cpu_model, ram_gb


class SystemPropertiesDialog(Gtk.Window):
    """Exact replica of Windows XP 'System Properties'."""

    def __init__(self, parent=None):
        super().__init__(title="System Properties")
        self.set_default_size(410, 468)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        if parent:
            self.set_transient_for(parent)
        icon_pb = load_pixbuf("cp-system.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        self.add(vbox)

        # Two rows of XP tabs like in the screenshot
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        for t in ["System Restore", "Automatic Updates", "Remote"]:
            b = Gtk.Button(label=t)
            b.get_style_context().add_class("xp-tab-btn")
            b.set_hexpand(True)
            row1.pack_start(b, True, True, 0)
        vbox.pack_start(row1, False, False, 0)

        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        for idx, t in enumerate(["General", "Computer Name", "Hardware", "Advanced"]):
            b = Gtk.Button(label=t)
            b.get_style_context().add_class("xp-tab-btn")
            if idx == 0:
                b.get_style_context().add_class("xp-tab-active")
            if idx == 2:
                b.connect("clicked", lambda *_: run_cmd("plasma-systemmonitor"))
            b.set_hexpand(True)
            row2.pack_start(b, True, True, 0)
        vbox.pack_start(row2, False, False, 0)

        page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        page.get_style_context().add_class("xp-tab-page")
        vbox.pack_start(page, True, True, 0)

        # Left column: XP Monitor icon
        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        left_col.set_valign(Gtk.Align.START)
        left_col.set_margin_top(16)
        mon_img = make_icon("xp-monitor.svg", 115)
        left_col.pack_start(mon_img, False, False, 0)
        page.pack_start(left_col, False, False, 0)

        # Right column: System details
        cpu_model, ram_gb = get_cpu_and_ram()
        user_name = GLib.get_real_name() or "King Geoffrey"
        if user_name == "Unknown":
            user_name = "King Geoffrey"

        right_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        right_col.set_valign(Gtk.Align.START)

        def add_header(text):
            lbl = Gtk.Label(label=text, xalign=0)
            right_col.pack_start(lbl, False, False, 2)

        def add_indent(text):
            lbl = Gtk.Label(label=text, xalign=0)
            lbl.set_margin_start(14)
            lbl.set_line_wrap(True)
            lbl.set_max_width_chars(30)
            right_col.pack_start(lbl, False, False, 0)

        add_header("System:")
        add_indent("Microsoft Windows XP")
        add_indent("Professional")
        add_indent("Version 2002")
        add_indent("Service Pack 3")

        sep1 = Gtk.Box()
        sep1.set_size_request(-1, 8)
        right_col.pack_start(sep1, False, False, 0)

        add_header("Registered to:")
        add_indent(user_name)
        add_indent("Steel Hull Studio")
        add_indent("76456-640-1803887-23173")

        sep2 = Gtk.Box()
        sep2.set_size_request(-1, 8)
        right_col.pack_start(sep2, False, False, 0)

        add_header("Computer:")
        add_indent(cpu_model)
        add_indent(f"3.70 GHz, {ram_gb}")
        add_indent("Physical Address Extension")

        page.pack_start(right_col, True, True, 0)

        # Bottom OK / Cancel / Apply buttons
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)

        for label, close_win in [("OK", True), ("Cancel", True), ("Apply", False)]:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("xp-push-btn")
            if not close_win:
                btn.set_sensitive(False)
            else:
                btn.connect("clicked", lambda *_: self.destroy())
            btn_row.pack_start(btn, False, False, 0)

        vbox.pack_start(btn_row, False, False, 0)


class DisplayPropertiesDialog(Gtk.Window):
    """Exact replica of 'Display Properties'."""

    def __init__(self, parent=None):
        super().__init__(title="Display Properties")
        self.set_default_size(404, 448)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        if parent:
            self.set_transient_for(parent)
        icon_pb = load_pixbuf("cp-display.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        self.add(vbox)

        tabs = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        tab_defs = [
            ("Themes", lambda: run_cmd("kcmshell6 kcm_lookandfeel")),
            ("Desktop", lambda: run_cmd("kcmshell6 kcm_wallpaper")),
            ("Screen Saver", lambda: run_cmd("kcmshell6 kcm_screenlocker")),
            ("Appearance", None),
            ("Settings", lambda: run_cmd("kcmshell6 kcm_kscreen")),
        ]
        for idx, (t_label, cb) in enumerate(tab_defs):
            b = Gtk.Button(label=t_label)
            b.get_style_context().add_class("xp-tab-btn")
            if idx == 3:
                b.get_style_context().add_class("xp-tab-active")
            if cb:
                b.connect("clicked", lambda _, c=cb: c())
            tabs.pack_start(b, False, False, 0)
        vbox.pack_start(tabs, False, False, 0)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        page.get_style_context().add_class("xp-tab-page")
        vbox.pack_start(page, True, True, 0)

        # Preview image
        prev_pb = load_pixbuf("xp-appearance-preview.svg", 356)
        if prev_pb:
            prev_img = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_size(
                    os.path.join(ICONS_DIR, "xp-appearance-preview.svg"), 356, 172
                )
            )
            page.pack_start(prev_img, False, False, 2)

        # Bottom controls row: left combos + right Effects/Advanced buttons
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        page.pack_start(bottom_row, True, True, 4)

        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        left_col.set_hexpand(True)

        cur_cfg = load_xp_settings()
        self.disp_combos = []
        for label_txt, options in [
            ("Windows and buttons:", ["Windows XP style", "Windows Classic style"]),
            ("Color scheme:", ["Default (blue)", "Olive Green", "Silver"]),
            ("Font size:", ["Normal", "Large Fonts", "Extra Large Fonts"]),
        ]:
            lbl = Gtk.Label(label=label_txt, xalign=0)
            left_col.pack_start(lbl, False, False, 0)
            combo = Gtk.ComboBoxText()
            for opt in options:
                combo.append_text(opt)
            combo.set_active(0)
            self.disp_combos.append(combo)
            left_col.pack_start(combo, False, False, 2)

        if cur_cfg.get("taskbarStyle") == "classic":
            self.disp_combos[0].set_active(1)

        bottom_row.pack_start(left_col, True, True, 0)

        right_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        right_col.set_valign(Gtk.Align.END)

        btn_eff = Gtk.Button(label="Effects...")
        btn_eff.get_style_context().add_class("xp-push-btn")
        btn_eff.connect("clicked", lambda *_: run_cmd("kcmshell6 kcm_animations"))

        btn_adv = Gtk.Button(label="Advanced")
        btn_adv.get_style_context().add_class("xp-push-btn")
        btn_adv.connect("clicked", lambda *_: run_cmd("kcmshell6 kcm_colors"))

        right_col.pack_start(btn_eff, False, False, 0)
        right_col.pack_start(btn_adv, False, False, 0)
        bottom_row.pack_start(right_col, False, False, 0)

        def apply_disp(close_after=False):
            c = load_xp_settings()
            is_cl = self.disp_combos[0].get_active() == 1
            c["taskbarStyle"] = "classic" if is_cl else "xp"
            c["startMenuStyle"] = "classic" if is_cl else "xp"
            save_xp_settings(c, restart_plasma=True)
            if close_after:
                self.destroy()

        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)
        for label, close_win in [("OK", True), ("Cancel", None), ("Apply", False)]:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("xp-push-btn")
            if close_win is None:
                btn.connect("clicked", lambda *_: self.destroy())
            elif close_win:
                btn.connect("clicked", lambda *_: apply_disp(True))
            else:
                btn.connect("clicked", lambda *_: apply_disp(False))
            btn_row.pack_start(btn, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)


XP_SETTINGS_FILE = os.path.expanduser("~/.config/xp-instellingen.json")

DEFAULT_XP_SETTINGS = {
    "taskbarStyle": "xp",
    "taskbarHeight": 30,
    "showQuickLaunch": True,
    "showClock": True,
    "startMenuStyle": "xp",
    "startIconSize": "large",
    "startItemsCount": 6,
    "startItemsMode": "both",
    "customItems": [
        "Firefox|firefox|firefox",
        "Steam|steam|steam",
        "Discord|discord|flatpak run dev.vencord.Vesktop",
        "Discord Legacy|com.discordapp.Discord|flatpak run com.discordapp.Discord",
        "Lutris|lutris|lutris",
        "Windows Explorer|computer|dolphin",
        "Control Panel|preferences-system|python3 $HOME/.local/share/xp-startknop/xp-verkenner.py configuratiescherm",
    ],
    "logonStyle": "welcome",
}


def load_xp_settings():
    cfg = dict(DEFAULT_XP_SETTINGS)
    try:
        if os.path.exists(XP_SETTINGS_FILE):
            with open(XP_SETTINGS_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    cfg.update(loaded)
    except Exception:
        pass
    return cfg


def save_xp_settings(cfg, restart_plasma=True):
    try:
        os.makedirs(os.path.dirname(XP_SETTINGS_FILE), exist_ok=True)
        with open(XP_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    js_content = (
        ".pragma library\n\n"
        f'var taskbarStyle = {json.dumps(cfg.get("taskbarStyle", "xp"))};\n'
        f'var taskbarHeight = {int(cfg.get("taskbarHeight", 30))};\n'
        f'var showQuickLaunch = {"true" if cfg.get("showQuickLaunch", True) else "false"};\n'
        f'var showClock = {"true" if cfg.get("showClock", True) else "false"};\n'
        f'var startMenuStyle = {json.dumps(cfg.get("startMenuStyle", "xp"))};\n'
        f'var startIconSize = {json.dumps(cfg.get("startIconSize", "large"))};\n'
        f'var startItemsCount = {int(cfg.get("startItemsCount", 6))};\n'
        f'var startItemsMode = {json.dumps(cfg.get("startItemsMode", "both"))};\n'
        f'var customItems = {json.dumps(cfg.get("customItems", DEFAULT_XP_SETTINGS["customItems"]), ensure_ascii=False)};\n'
        f'var logonStyle = {json.dumps(cfg.get("logonStyle", "welcome"))};\n'
    )

    home = os.path.expanduser("~")
    targets = [
        os.path.join(home, ".local/share/plasma/plasmoids/nl.steelhull.xpstart/contents/ui/xpConfig.js"),
        os.path.join(home, ".local/share/plasma/plasmoids/nl.steelhull.xptray/contents/ui/xpConfig.js"),
        os.path.join(home, ".local/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/xpConfig.js"),
        os.path.join(home, ".local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/lockscreen/xpConfig.js"),
        os.path.join(home, ".local/share/plasma/look-and-feel/org.magpie.xpluna.desktop/contents/splash/xpConfig.js"),
        "/var/mnt/schijven/1TB SSD/AI Assistent/Github Repos/Bazzite-Windows-XP/xp-login-screen/xpConfig.js",
        "/var/mnt/schijven/1TB SSD/AI Assistent/Github Repos/Bazzite-Windows-XP/package/contents/ui/xpConfig.js",
        "/var/mnt/schijven/1TB SSD/AI Assistent/Github Repos/Bazzite-Windows-XP/tray-package/contents/ui/xpConfig.js",
    ]
    for t_path in targets:
        try:
            t_dir = os.path.dirname(t_path)
            if os.path.isdir(t_dir):
                with open(t_path, "w", encoding="utf-8") as f:
                    f.write(js_content)
        except Exception:
            pass

    # Pas de taakbalkhoogte (panel thickness) direct aan in plasmashellrc én plasma-org.kde.plasma.desktop-appletsrc
    tb_height = int(cfg.get("taskbarHeight", 30))
    home_appletsrc = os.path.join(home, ".config/plasma-org.kde.plasma.desktop-appletsrc")
    try:
        # Zoek alle panel containments in plasma-org.kde.plasma.desktop-appletsrc
        if os.path.exists(home_appletsrc):
            with open(home_appletsrc, "r", encoding="utf-8") as f:
                app_lines = f.readlines()
            cur_grp = ""
            for aln in app_lines:
                aln_s = aln.strip()
                if aln_s.startswith("[Containments][") and aln_s.endswith("]"):
                    cur_grp = aln_s[1:-1]
                elif aln_s == "plugin=org.kde.panel" and cur_grp:
                    subprocess.run(["kwriteconfig6", "--file", "plasma-org.kde.plasma.desktop-appletsrc", "--group", cur_grp.split("][")[0], "--group", cur_grp.split("][")[1], "--group", "General", "--key", "thickness", str(tb_height)], check=False)
    except Exception:
        pass

    try:
        subprocess.run(
            [
                "qdbus-qt6",
                "org.kde.plasmashell",
                "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript",
                f"for (var i = 0; i < panels().length; ++i) {{ panels()[i].height = {tb_height}; }}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
    except Exception:
        pass

    if restart_plasma:
        subprocess.run(
            ["systemctl", "--user", "restart", "plasma-plasmashell.service"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class TaskbarPropertiesDialog(Gtk.Window):
    """
    Comprehensive 'Taskbar, Start Menu and Logon Properties' with 3 working tabs:
    1. Taskbar (XP Luna vs Classic, Height 30/36/42/48 px for larger buttons, Quick Launch, Clock)
    2. Start Menu (XP vs Classic Start menu, Large/Small icons, Item count, Source: Favorites / Most Used / Custom Fixed List)
    3. Logon Screen (Windows XP Welcome Screen with user tiles vs Classic 'Log On to Windows' dialog)
    """

    def __init__(self, parent=None, initial_tab=0):
        super().__init__(title="Taskbar and Start Menu Properties")
        self.set_default_size(465, 530)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        if parent:
            self.set_transient_for(parent)
        icon_pb = load_pixbuf("cp-taskbar.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        self.cfg = load_xp_settings()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        self.add(vbox)

        # Tab buttons at top
        self.tab_btns = []
        tabs_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        for idx, t_label in enumerate(["Taskbar", "Start Menu", "Logon Screen"]):
            b = Gtk.Button(label=t_label)
            b.get_style_context().add_class("xp-tab-btn")
            b.connect("clicked", lambda _, i=idx: self._switch_tab(i))
            self.tab_btns.append(b)
            tabs_bar.pack_start(b, False, False, 0)
        vbox.pack_start(tabs_bar, False, False, 0)

        self.stack = Gtk.Stack()
        self.stack.get_style_context().add_class("xp-tab-page")
        vbox.pack_start(self.stack, True, True, 0)

        # === TAB 0: TASKBAR ===
        page_tb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        self.stack.add_named(page_tb, "tab0")

        grp_tb_style = Gtk.Label(xalign=0)
        grp_tb_style.set_markup("<span foreground='#1f4fd5' weight='bold'>Taskbar appearance and size</span>")
        page_tb.pack_start(grp_tb_style, False, False, 2)

        lbl_tb_style = Gtk.Label(label="Taskbar and Start button visual style:", xalign=0)
        page_tb.pack_start(lbl_tb_style, False, False, 0)

        self.combo_tb_style = Gtk.ComboBoxText()
        self.combo_tb_style.append_text("Windows XP style (Blue Luna taskbar with green Start button)")
        self.combo_tb_style.append_text("Windows Classic style (Gray 3D taskbar with classic Start button)")
        self.combo_tb_style.set_active(1 if self.cfg.get("taskbarStyle") == "classic" else 0)
        page_tb.pack_start(self.combo_tb_style, False, False, 2)

        lbl_tb_height = Gtk.Label(label="Taskbar height and taskbar button size:", xalign=0)
        page_tb.pack_start(lbl_tb_height, False, False, 0)

        self.height_values = [30, 36, 42, 48]
        self.combo_tb_height = Gtk.ComboBoxText()
        self.combo_tb_height.append_text("Standard Windows XP (30 pixels)")
        self.combo_tb_height.append_text("Medium — Slightly taller bar & larger buttons (36 pixels)")
        self.combo_tb_height.append_text("Large — Tall taskbar & large buttons (42 pixels)")
        self.combo_tb_height.append_text("Extra Large — Double height (48 pixels)")
        cur_h = int(self.cfg.get("taskbarHeight", 30))
        h_idx = self.height_values.index(cur_h) if cur_h in self.height_values else 0
        self.combo_tb_height.set_active(h_idx)
        page_tb.pack_start(self.combo_tb_height, False, False, 2)

        sep_tb1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        page_tb.pack_start(sep_tb1, False, False, 4)

        grp1 = Gtk.Label(xalign=0)
        grp1.set_markup("<span foreground='#1f4fd5' weight='bold'>Taskbar options</span>")
        page_tb.pack_start(grp1, False, False, 2)

        self.chk_lock = Gtk.CheckButton(label="Lock the taskbar")
        self.chk_lock.set_active(True)
        page_tb.pack_start(self.chk_lock, False, False, 0)

        self.chk_top = Gtk.CheckButton(label="Keep the taskbar on top of other windows")
        self.chk_top.set_active(True)
        page_tb.pack_start(self.chk_top, False, False, 0)

        self.chk_group = Gtk.CheckButton(label="Group similar taskbar buttons")
        self.chk_group.set_active(True)
        page_tb.pack_start(self.chk_group, False, False, 0)

        self.chk_ql = Gtk.CheckButton(label="Show Quick Launch (Show Desktop, Firefox, Windows Explorer)")
        self.chk_ql.set_active(bool(self.cfg.get("showQuickLaunch", True)))
        page_tb.pack_start(self.chk_ql, False, False, 0)

        sep_tb2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        page_tb.pack_start(sep_tb2, False, False, 4)

        grp2 = Gtk.Label(xalign=0)
        grp2.set_markup("<span foreground='#1f4fd5' weight='bold'>Notification area (System Tray)</span>")
        page_tb.pack_start(grp2, False, False, 2)

        self.chk_clock = Gtk.CheckButton(label="Show the clock")
        self.chk_clock.set_active(bool(self.cfg.get("showClock", True)))
        page_tb.pack_start(self.chk_clock, False, False, 0)

        self.chk_clean = Gtk.CheckButton(label="Show background apps (Discord, Steam, etc.) and system icons")
        self.chk_clean.set_active(True)
        page_tb.pack_start(self.chk_clean, False, False, 0)

        # === TAB 1: START MENU ===
        page_sm = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.stack.add_named(page_sm, "tab1")

        grp_sm_style = Gtk.Label(xalign=0)
        grp_sm_style.set_markup("<span foreground='#1f4fd5' weight='bold'>Start menu style</span>")
        page_sm.pack_start(grp_sm_style, False, False, 1)

        self.rb_sm_xp = Gtk.RadioButton.new_with_label_from_widget(
            None, "Start menu (Windows XP 2-column layout with user avatar, favorites & places)"
        )
        self.rb_sm_classic = Gtk.RadioButton.new_with_label_from_widget(
            self.rb_sm_xp, "Classic Start menu (Classic 3D 1-column layout with Windows XP sidebar)"
        )
        if self.cfg.get("startMenuStyle") == "classic":
            self.rb_sm_classic.set_active(True)
        else:
            self.rb_sm_xp.set_active(True)
        page_sm.pack_start(self.rb_sm_xp, False, False, 0)
        page_sm.pack_start(self.rb_sm_classic, False, False, 0)

        sep_sm1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        page_sm.pack_start(sep_sm1, False, False, 3)

        grp_sm_items = Gtk.Label(xalign=0)
        grp_sm_items.set_markup("<span foreground='#1f4fd5' weight='bold'>Customize Start menu programs and icons</span>")
        page_sm.pack_start(grp_sm_items, False, False, 1)

        row_ic_cnt = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        lbl_ic = Gtk.Label(label="Icon size:", xalign=0)
        self.combo_sm_icons = Gtk.ComboBoxText()
        self.combo_sm_icons.append_text("Large icons (30 px)")
        self.combo_sm_icons.append_text("Small icons (20 px)")
        self.combo_sm_icons.set_active(1 if self.cfg.get("startIconSize") == "small" else 0)

        lbl_cnt = Gtk.Label(label="Number of programs:", xalign=0)
        adj = Gtk.Adjustment(value=float(self.cfg.get("startItemsCount", 6)), lower=3, upper=14, step_increment=1, page_increment=2, page_size=0)
        self.spin_sm_count = Gtk.SpinButton(adjustment=adj, climb_rate=1, digits=0)

        row_ic_cnt.pack_start(lbl_ic, False, False, 0)
        row_ic_cnt.pack_start(self.combo_sm_icons, True, True, 0)
        row_ic_cnt.pack_start(lbl_cnt, False, False, 0)
        row_ic_cnt.pack_start(self.spin_sm_count, False, False, 0)
        page_sm.pack_start(row_ic_cnt, False, False, 2)

        lbl_mode = Gtk.Label(label="Programs shown on the left side of the Start menu:", xalign=0)
        page_sm.pack_start(lbl_mode, False, False, 0)

        self.mode_keys = ["both", "favorites", "recent", "custom"]
        self.combo_sm_mode = Gtk.ComboBoxText()
        self.combo_sm_mode.append_text("Favorites + Most frequently used programs (Default XP)")
        self.combo_sm_mode.append_text("Favorites only (Pinned programs)")
        self.combo_sm_mode.append_text("Most frequently used programs only")
        self.combo_sm_mode.append_text("Custom fixed list (Configure below)")
        cur_m = self.cfg.get("startItemsMode", "both")
        self.combo_sm_mode.set_active(self.mode_keys.index(cur_m) if cur_m in self.mode_keys else 0)
        page_sm.pack_start(self.combo_sm_mode, False, False, 2)

        lbl_custom = Gtk.Label(
            label="Custom fixed list (1 program per line as: Name|icon|command):",
            xalign=0,
        )
        page_sm.pack_start(lbl_custom, False, False, 0)

        sc_custom = Gtk.ScrolledWindow()
        sc_custom.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sc_custom.set_size_request(-1, 115)
        sc_custom.set_shadow_type(Gtk.ShadowType.IN)
        self.txt_custom = Gtk.TextView()
        self.txt_custom.set_monospace(True)
        custom_lines = self.cfg.get("customItems", DEFAULT_XP_SETTINGS["customItems"])
        self.txt_custom.get_buffer().set_text("\n".join(custom_lines))
        sc_custom.add(self.txt_custom)
        page_sm.pack_start(sc_custom, True, True, 0)

        # === TAB 2: LOGON SCREEN ===
        page_lg = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.stack.add_named(page_lg, "tab2")

        grp_lg = Gtk.Label(xalign=0)
        grp_lg.set_markup("<span foreground='#1f4fd5' weight='bold'>Select the way users log on</span>")
        page_lg.pack_start(grp_lg, False, False, 2)

        self.rb_lg_welcome = Gtk.RadioButton.new_with_label_from_widget(
            None, "Use the Welcome screen (Standard Windows XP Blue Welcome Screen)"
        )
        desc_w = Gtk.Label(
            label="   Displays the blue Windows XP login screen with the authentic 3D Windows XP logo,\n   user tiles, password field, and the italic 'welcome' screen.",
            xalign=0,
        )
        desc_w.get_style_context().add_class("xp-cat-desc")

        self.rb_lg_classic = Gtk.RadioButton.new_with_label_from_widget(
            self.rb_lg_welcome, "Use the Classic logon prompt ('Log On to Windows' dialog box)"
        )
        desc_c = Gtk.Label(
            label="   Displays the classic Windows XP Professional x64 'Log On to Windows' dialog\n   with User name, Password, and OK, Cancel, Shut Down..., and Options << buttons.",
            xalign=0,
        )
        desc_c.get_style_context().add_class("xp-cat-desc")

        if self.cfg.get("logonStyle") == "classic":
            self.rb_lg_classic.set_active(True)
        else:
            self.rb_lg_welcome.set_active(True)

        page_lg.pack_start(self.rb_lg_welcome, False, False, 0)
        page_lg.pack_start(desc_w, False, False, 2)
        page_lg.pack_start(self.rb_lg_classic, False, False, 4)
        page_lg.pack_start(desc_c, False, False, 2)

        sep_lg = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        page_lg.pack_start(sep_lg, False, False, 6)

        btn_test_lock = Gtk.Button(label="Test Logon Screen Now (Save & Lock Screen)")
        btn_test_lock.get_style_context().add_class("xp-push-btn")
        btn_test_lock.connect("clicked", self._on_test_logon)
        page_lg.pack_start(btn_test_lock, False, False, 4)

        # Bottom button row: OK / Cancel / Apply
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)

        btn_ok = Gtk.Button(label="OK")
        btn_ok.get_style_context().add_class("xp-push-btn")
        btn_ok.connect("clicked", lambda *_: self._apply_settings(close_after=True))

        btn_cancel = Gtk.Button(label="Cancel")
        btn_cancel.get_style_context().add_class("xp-push-btn")
        btn_cancel.connect("clicked", lambda *_: self.destroy())

        btn_apply = Gtk.Button(label="Apply")
        btn_apply.get_style_context().add_class("xp-push-btn")
        btn_apply.connect("clicked", lambda *_: self._apply_settings(close_after=False))

        btn_row.pack_start(btn_ok, False, False, 0)
        btn_row.pack_start(btn_cancel, False, False, 0)
        btn_row.pack_start(btn_apply, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)

        self.connect("realize", lambda *_: self._switch_tab(initial_tab))

    def _switch_tab(self, idx):
        for i, b in enumerate(self.tab_btns):
            ctx = b.get_style_context()
            if i == idx:
                ctx.add_class("xp-tab-active")
            else:
                ctx.remove_class("xp-tab-active")
        self.stack.set_visible_child_name(f"tab{idx}")

    def _collect_cfg(self):
        new_cfg = dict(self.cfg)
        new_cfg["taskbarStyle"] = "classic" if self.combo_tb_style.get_active() == 1 else "xp"
        h_idx = self.combo_tb_height.get_active()
        new_cfg["taskbarHeight"] = self.height_values[h_idx] if 0 <= h_idx < len(self.height_values) else 30
        new_cfg["showQuickLaunch"] = bool(self.chk_ql.get_active())
        new_cfg["showClock"] = bool(self.chk_clock.get_active())
        new_cfg["startMenuStyle"] = "classic" if self.rb_sm_classic.get_active() else "xp"
        new_cfg["startIconSize"] = "small" if self.combo_sm_icons.get_active() == 1 else "large"
        new_cfg["startItemsCount"] = int(self.spin_sm_count.get_value_as_int())
        m_idx = self.combo_sm_mode.get_active()
        new_cfg["startItemsMode"] = self.mode_keys[m_idx] if 0 <= m_idx < len(self.mode_keys) else "both"

        buf = self.txt_custom.get_buffer()
        raw_txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        lines = [ln.strip() for ln in raw_txt.splitlines() if ln.strip()]
        if lines:
            new_cfg["customItems"] = lines

        new_cfg["logonStyle"] = "classic" if self.rb_lg_classic.get_active() else "welcome"
        return new_cfg

    def _apply_settings(self, close_after=False):
        play_xp_click()
        self.cfg = self._collect_cfg()
        save_xp_settings(self.cfg, restart_plasma=True)
        if close_after:
            self.destroy()

    def _on_test_logon(self, *_):
        self._apply_settings(close_after=False)
        run_cmd(["loginctl", "lock-session"])


class RunDialog(Gtk.Window):
    """Exact replica of the Windows XP 'Run' dialog."""

    def __init__(self):
        super().__init__(title="Run")
        self.set_default_size(365, 175)
        self.set_resizable(False)
        icon_pb = load_pixbuf("run.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(14)
        vbox.set_margin_bottom(12)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        self.add(vbox)

        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        top.pack_start(make_icon("run.svg", 36), False, False, 0)
        desc = Gtk.Label(
            label="Type the name of a program, folder, document, or\nInternet resource, and Windows will open it for you.",
            xalign=0,
        )
        top.pack_start(desc, True, True, 0)
        vbox.pack_start(top, False, False, 0)

        mid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl = Gtk.Label(label="Open:", xalign=0)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.connect("activate", self._on_ok)
        mid.pack_start(lbl, False, False, 0)
        mid.pack_start(self.entry, True, True, 0)
        vbox.pack_start(mid, False, False, 0)

        btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btns.set_halign(Gtk.Align.END)
        btns.set_margin_top(8)

        ok_btn = Gtk.Button(label="OK")
        ok_btn.get_style_context().add_class("xp-push-btn")
        ok_btn.connect("clicked", self._on_ok)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.get_style_context().add_class("xp-push-btn")
        cancel_btn.connect("clicked", lambda *_: Gtk.main_quit())

        browse_btn = Gtk.Button(label="Browse...")
        browse_btn.get_style_context().add_class("xp-push-btn")
        browse_btn.connect("clicked", self._on_browse)

        btns.pack_start(ok_btn, False, False, 0)
        btns.pack_start(cancel_btn, False, False, 0)
        btns.pack_start(browse_btn, False, False, 0)
        vbox.pack_start(btns, False, False, 0)

    def _on_ok(self, *_):
        text = self.entry.get_text().strip()
        if not text:
            return
        low = text.lower()
        if low in ("control", "configuratiescherm"):
            run_cmd([sys.executable, os.path.abspath(__file__), "configuratiescherm"])
        elif low in ("cmd", "command", "konsole", "terminal"):
            run_cmd("ptyxis || konsole || xterm")
        elif low in ("explorer", "verkenner"):
            run_cmd([sys.executable, os.path.abspath(__file__), "computer"])
        elif low in ("sysdm.cpl", "systeem", "dxdiag"):
            run_cmd([sys.executable, os.path.abspath(__file__), "systeem"])
        elif os.path.isdir(os.path.expanduser(text)):
            open_in_dolphin(os.path.expanduser(text))
        else:
            run_cmd(text)
        Gtk.main_quit()

    def _on_browse(self, *_):
        open_in_dolphin(os.path.expanduser("~"))
        Gtk.main_quit()


class TaskManagerWindow(Gtk.Window):
    """Authentic Windows XP 'Windows Task Manager' with Applications, Processes, and green Performance graphs."""

    def __init__(self, initial_tab=0):
        super().__init__(title="Windows Task Manager")
        self.initial_tab = initial_tab
        self.set_default_size(435, 475)
        self.set_position(Gtk.WindowPosition.CENTER)
        icon_pb = load_pixbuf("cp-perf.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        self.cpu_history = [12, 18, 15, 22, 14, 19, 25, 17, 13, 16] * 6
        self.mem_history = [35] * 60
        self.last_cpu_stat = self._read_cpu_stat()
        self.proc_count = 0
        self.cur_cpu_pct = 14
        self.cur_mem_mb = 2048
        self.total_mem_mb = 16384

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.get_style_context().add_class("xp-window")
        self.add(vbox)

        menubar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        menubar.get_style_context().add_class("xp-menubar")
        for m_txt in ("File", "Options", "View", "Shut Down", "Help"):
            mb = Gtk.Button(label=m_txt)
            mb.get_style_context().add_class("xp-menubar-btn")
            if m_txt == "File":
                mb.connect("clicked", lambda *_: run_cmd([sys.executable, os.path.abspath(__file__), "uitvoeren"]))
            elif m_txt == "Help":
                mb.connect("clicked", lambda *_: run_cmd("plasma-systemmonitor"))
            menubar.pack_start(mb, False, False, 0)
        vbox.pack_start(menubar, False, False, 0)

        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_start(8)
        self.notebook.set_margin_end(8)
        self.notebook.set_margin_top(6)
        self.notebook.set_margin_bottom(4)
        vbox.pack_start(self.notebook, True, True, 0)

        # Tab 1: Applications
        app_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        app_tab.set_margin_start(8)
        app_tab.set_margin_end(8)
        app_tab.set_margin_top(8)
        app_tab.set_margin_bottom(8)

        self.app_store = Gtk.ListStore(str, str, int)
        app_tree = Gtk.TreeView(model=self.app_store)
        for idx, col_title in enumerate(("Task", "Status")):
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_title, renderer, text=idx)
            col.set_expand(idx == 0)
            app_tree.append_column(col)
        self.app_sel = app_tree.get_selection()

        app_scroll = Gtk.ScrolledWindow()
        app_scroll.set_shadow_type(Gtk.ShadowType.IN)
        app_scroll.add(app_tree)
        app_tab.pack_start(app_scroll, True, True, 0)

        app_btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        new_task_btn = Gtk.Button(label="New Task...")
        new_task_btn.get_style_context().add_class("xp-push-btn")
        new_task_btn.set_size_request(105, 24)
        new_task_btn.connect("clicked", lambda *_: run_cmd([sys.executable, os.path.abspath(__file__), "uitvoeren"]))
        end_task_btn = Gtk.Button(label="End Task")
        end_task_btn.get_style_context().add_class("xp-push-btn")
        end_task_btn.set_size_request(105, 24)
        end_task_btn.connect("clicked", self._on_kill_selected_app)
        app_btn_row.pack_end(new_task_btn, False, False, 0)
        app_btn_row.pack_end(end_task_btn, False, False, 0)
        app_tab.pack_start(app_btn_row, False, False, 0)
        self.notebook.append_page(app_tab, Gtk.Label(label="Applications"))

        # Tab 2: Processes
        proc_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        proc_tab.set_margin_start(8)
        proc_tab.set_margin_end(8)
        proc_tab.set_margin_top(8)
        proc_tab.set_margin_bottom(8)

        self.proc_store = Gtk.ListStore(str, str, str, str, int)
        proc_tree = Gtk.TreeView(model=self.proc_store)
        for idx, col_title in enumerate(("Image Name", "User Name", "CPU", "Mem Usage")):
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_title, renderer, text=idx)
            col.set_expand(idx == 0)
            proc_tree.append_column(col)
        self.proc_sel = proc_tree.get_selection()

        proc_scroll = Gtk.ScrolledWindow()
        proc_scroll.set_shadow_type(Gtk.ShadowType.IN)
        proc_scroll.add(proc_tree)
        proc_tab.pack_start(proc_scroll, True, True, 0)

        proc_btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        proc_chk = Gtk.CheckButton(label="Show processes from all users")
        proc_chk.set_active(True)
        proc_btn_row.pack_start(proc_chk, False, False, 0)
        end_proc_btn = Gtk.Button(label="End Process")
        end_proc_btn.get_style_context().add_class("xp-push-btn")
        end_proc_btn.set_size_request(115, 24)
        end_proc_btn.connect("clicked", self._on_kill_selected_proc)
        proc_btn_row.pack_end(end_proc_btn, False, False, 0)
        proc_tab.pack_start(proc_btn_row, False, False, 0)
        self.notebook.append_page(proc_tab, Gtk.Label(label="Processes"))

        # Tab 3: Performance (with black/green Windows XP graphs)
        perf_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        perf_tab.set_margin_start(8)
        perf_tab.set_margin_end(8)
        perf_tab.set_margin_top(8)
        perf_tab.set_margin_bottom(8)

        cpu_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cpu_gauge_frame = Gtk.Frame(label=" CPU Usage ")
        self.cpu_gauge_area = Gtk.DrawingArea()
        self.cpu_gauge_area.set_size_request(95, 86)
        self.cpu_gauge_area.connect("draw", self._draw_cpu_gauge)
        cpu_gauge_frame.add(self.cpu_gauge_area)
        cpu_row.pack_start(cpu_gauge_frame, False, False, 0)

        cpu_hist_frame = Gtk.Frame(label=" CPU Usage History ")
        self.cpu_hist_area = Gtk.DrawingArea()
        self.cpu_hist_area.set_size_request(260, 86)
        self.cpu_hist_area.connect("draw", self._draw_cpu_hist)
        cpu_hist_frame.add(self.cpu_hist_area)
        cpu_row.pack_start(cpu_hist_frame, True, True, 0)
        perf_tab.pack_start(cpu_row, False, False, 0)

        mem_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        mem_gauge_frame = Gtk.Frame(label=" PF Usage ")
        self.mem_gauge_area = Gtk.DrawingArea()
        self.mem_gauge_area.set_size_request(95, 86)
        self.mem_gauge_area.connect("draw", self._draw_mem_gauge)
        mem_gauge_frame.add(self.mem_gauge_area)
        mem_row.pack_start(mem_gauge_frame, False, False, 0)

        mem_hist_frame = Gtk.Frame(label=" Page File Usage History ")
        self.mem_hist_area = Gtk.DrawingArea()
        self.mem_hist_area.set_size_request(260, 86)
        self.mem_hist_area.connect("draw", self._draw_mem_hist)
        mem_hist_frame.add(self.mem_hist_area)
        mem_row.pack_start(mem_hist_frame, True, True, 0)
        perf_tab.pack_start(mem_row, False, False, 0)

        stats_grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        self.lbl_totals = Gtk.Label(label="Handles:   42180\nThreads:   1480\nProcesses: 215", xalign=0)
        self.lbl_phys = Gtk.Label(label="Total:        16384000\nAvailable:    10240000\nSystem Cache: 4120000", xalign=0)
        for idx, (f_title, w_lbl) in enumerate(((" Totals ", self.lbl_totals), (" Physical Memory (K) ", self.lbl_phys))):
            fr = Gtk.Frame(label=f_title)
            w_lbl.set_margin_start(6)
            w_lbl.set_margin_end(6)
            w_lbl.set_margin_top(4)
            w_lbl.set_margin_bottom(4)
            fr.add(w_lbl)
            fr.set_hexpand(True)
            stats_grid.attach(fr, idx, 0, 1, 1)
        perf_tab.pack_start(stats_grid, False, False, 0)
        self.notebook.append_page(perf_tab, Gtk.Label(label="Performance"))

        self.statusbar = Gtk.Label(label="Processes: --   |   CPU Usage: --%   |   Commit Charge: -- MB", xalign=0)
        self.statusbar.get_style_context().add_class("xp-status-bar")
        vbox.pack_start(self.statusbar, False, False, 0)

        self._refresh_processes()
        self._refresh_stats()
        if initial_tab > 0:
            self.notebook.set_current_page(initial_tab)
        GLib.timeout_add(1200, self._refresh_stats)
        GLib.timeout_add(3500, self._refresh_processes)

    def _read_cpu_stat(self):
        try:
            with open("/proc/stat") as f:
                parts = [int(x) for x in f.readline().split()[1:]]
                idle = parts[3] + (parts[4] if len(parts) > 4 else 0)
                return sum(parts), idle
        except Exception:
            return 100, 90

    def _refresh_stats(self):
        tot, idle = self._read_cpu_stat()
        prev_tot, prev_idle = self.last_cpu_stat
        self.last_cpu_stat = (tot, idle)
        dt = max(1, tot - prev_tot)
        didle = max(0, idle - prev_idle)
        pct = max(4, min(100, int(round(100.0 * (dt - didle) / dt))))
        self.cur_cpu_pct = pct
        self.cpu_history.append(pct)
        self.cpu_history = self.cpu_history[-60:]

        try:
            mem = {}
            with open("/proc/meminfo") as f:
                for line in f:
                    if ":" in line:
                        k, v = line.split(":", 1)
                        mem[k.strip()] = int(v.split()[0])
            tot_kb = mem.get("MemTotal", 16384000)
            avail_kb = mem.get("MemAvailable", 8192000)
            cached_kb = mem.get("Cached", 2048000)
            used_kb = max(0, tot_kb - avail_kb)
            self.total_mem_mb = tot_kb // 1024
            self.cur_mem_mb = used_kb // 1024
            mem_pct = max(1, min(100, int(round(100.0 * used_kb / max(1, tot_kb)))))
            self.mem_history.append(mem_pct)
            self.mem_history = self.mem_history[-60:]
            self.lbl_phys.set_text(
                f"Total:        {tot_kb}\nAvailable:    {avail_kb}\nSystem Cache: {cached_kb}"
            )
        except Exception:
            pass

        self.lbl_totals.set_text(
            f"Handles:    {self.proc_count * 142}\nThreads:    {self.proc_count * 6}\nProcesses:  {self.proc_count}"
        )
        self.statusbar.set_text(
            f"Processes: {self.proc_count}     |     CPU Usage: {self.cur_cpu_pct}%     |     Commit Charge: {self.cur_mem_mb}M / {self.total_mem_mb}M"
        )
        self.cpu_gauge_area.queue_draw()
        self.cpu_hist_area.queue_draw()
        self.mem_gauge_area.queue_draw()
        self.mem_hist_area.queue_draw()
        return True

    def _refresh_processes(self):
        try:
            out = subprocess.check_output(
                ["ps", "-eo", "pid,user,pcpu,rss,comm", "--sort=-pcpu"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            lines = out.strip().splitlines()[1:]
            self.proc_count = len(lines)
            self.proc_store.clear()
            self.app_store.clear()
            gui_keywords = ("firefox", "dolphin", "discord", "steam", "claude", "antigravity", "lutris", "kate", "kwrite", "vlc", "gimp", "xp-verkenner")
            for ln in lines[:85]:
                parts = ln.split(None, 4)
                if len(parts) < 5:
                    continue
                pid_s, usr, pcpu, rss_s, comm = parts
                pid = int(pid_s)
                kb_str = f"{int(rss_s):,} K"
                self.proc_store.append([comm, usr, f"{pcpu}%", kb_str, pid])
                if any(k in comm.lower() for k in gui_keywords):
                    self.app_store.append([comm, "Running", pid])
        except Exception:
            pass
        return True

    def _on_kill_selected_app(self, *_):
        model, it = self.app_sel.get_selected()
        if it:
            pid = model.get_value(it, 2)
            subprocess.Popen(["kill", str(pid)])
            self._refresh_processes()

    def _on_kill_selected_proc(self, *_):
        model, it = self.proc_sel.get_selected()
        if it:
            pid = model.get_value(it, 4)
            subprocess.Popen(["kill", str(pid)])
            self._refresh_processes()

    def _draw_xp_grid(self, cr, w, h):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        cr.set_source_rgb(0.0, 0.32, 0.0)
        cr.set_line_width(1.0)
        for x in range(0, w, 12):
            cr.move_to(x + 0.5, 0)
            cr.line_to(x + 0.5, h)
        for y in range(0, h, 12):
            cr.move_to(0, y + 0.5)
            cr.line_to(w, y + 0.5)
        cr.stroke()

    def _draw_cpu_gauge(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        bar_w = 34
        bx = (w - bar_w) // 2
        bars = 18
        active_bars = int(round((self.cur_cpu_pct / 100.0) * bars))
        for i in range(bars):
            by = h - 24 - (i + 1) * 3
            if i < active_bars:
                cr.set_source_rgb(0.0, 1.0, 0.0)
            else:
                cr.set_source_rgb(0.0, 0.32, 0.0)
            cr.rectangle(bx, by, bar_w, 2)
            cr.fill()
        cr.set_source_rgb(0.0, 1.0, 0.0)
        cr.select_font_face("Tahoma", 0, 1)
        cr.set_font_size(12)
        txt = f"{self.cur_cpu_pct} %"
        cr.move_to((w - len(txt) * 6.5) / 2, h - 7)
        cr.show_text(txt)

    def _draw_mem_gauge(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        bar_w = 34
        bx = (w - bar_w) // 2
        bars = 18
        pct = self.mem_history[-1] if self.mem_history else 35
        active_bars = int(round((pct / 100.0) * bars))
        for i in range(bars):
            by = h - 24 - (i + 1) * 3
            if i < active_bars:
                cr.set_source_rgb(0.0, 1.0, 0.0)
            else:
                cr.set_source_rgb(0.0, 0.32, 0.0)
            cr.rectangle(bx, by, bar_w, 2)
            cr.fill()
        cr.set_source_rgb(0.0, 1.0, 0.0)
        cr.select_font_face("Tahoma", 0, 1)
        cr.set_font_size(11)
        txt = f"{round(self.cur_mem_mb / 1024, 1)} GB"
        cr.move_to((w - len(txt) * 5.8) / 2, h - 7)
        cr.show_text(txt)

    def _draw_cpu_hist(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        self._draw_xp_grid(cr, w, h)
        if len(self.cpu_history) < 2:
            return
        cr.set_source_rgb(0.0, 1.0, 0.0)
        cr.set_line_width(1.4)
        step = w / float(len(self.cpu_history) - 1)
        for i, val in enumerate(self.cpu_history):
            x = i * step
            y = h - 4 - ((val / 100.0) * (h - 8))
            if i == 0:
                cr.move_to(x, y)
            else:
                cr.line_to(x, y)
        cr.stroke()

    def _draw_mem_hist(self, widget, cr):
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        self._draw_xp_grid(cr, w, h)
        if len(self.mem_history) < 2:
            return
        cr.set_source_rgb(0.0, 1.0, 0.0)
        cr.set_line_width(1.4)
        step = w / float(len(self.mem_history) - 1)
        for i, val in enumerate(self.mem_history):
            x = i * step
            y = h - 4 - ((val / 100.0) * (h - 8))
            if i == 0:
                cr.move_to(x, y)
            else:
                cr.line_to(x, y)
        cr.stroke()


class XpExplorerWindow(Gtk.Window):
    """
    Windows XP Explorer for 'My Computer' and 'Control Panel'
    (Category View + Classic View).
    """

    def __init__(self, initial_page="computer"):
        super().__init__(title="My Computer")
        self.set_default_size(880, 610)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.history = [initial_page]
        self.history_idx = 0
        self.cp_classic = (initial_page == "klassiek")
        if initial_page == "klassiek":
            self.history = ["configuratiescherm"]

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.get_style_context().add_class("xp-window")
        self.add(root)

        # 1. Menubar + Windows XP Flag
        menubar_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        menubar_row.get_style_context().add_class("xp-menubar")

        for m_label, action in [
            ("File", lambda: self.destroy()),
            ("Edit", None),
            ("View", lambda: self.toggle_cp_mode()),
            ("Favorites", lambda: open_in_dolphin(os.path.expanduser("~"))),
            ("Tools", lambda: run_cmd("kcmshell6 kcm_filetypes")),
            ("Help", lambda: run_cmd("khelpcenter")),
        ]:
            mb = Gtk.Button(label=m_label)
            mb.get_style_context().add_class("xp-menubar-btn")
            if action:
                mb.connect("clicked", lambda _, a=action: a())
            menubar_row.pack_start(mb, False, False, 0)

        flag_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        flag_box.get_style_context().add_class("xp-flag-box")
        flag_box.pack_start(make_icon("xp-flag.svg", 22), False, False, 0)
        menubar_row.pack_end(flag_box, False, False, 0)
        root.pack_start(menubar_row, False, False, 0)

        # 2. Standard Buttons Toolbar (Back, Forward, Up | Search, Folders | Views)
        tbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        tbar.get_style_context().add_class("xp-toolbar")

        self.btn_back = self._make_toolbtn("back.svg", "Back  ▾", self.go_back)
        self.btn_fwd = self._make_toolbtn("forward.svg", "▾", self.go_forward)
        self.btn_up = self._make_toolbtn("folder-up.svg", None, self.go_up)

        tbar.pack_start(self.btn_back, False, False, 0)
        tbar.pack_start(self.btn_fwd, False, False, 0)
        tbar.pack_start(self.btn_up, False, False, 0)
        tbar.pack_start(self._make_vsep(), False, False, 2)

        btn_search = self._make_toolbtn("search.svg", "Search", lambda: run_cmd("krunner"))
        btn_folders = self._make_toolbtn(
            "folder.svg", "Folders", lambda: open_in_dolphin(os.path.expanduser("~"))
        )
        tbar.pack_start(btn_search, False, False, 0)
        tbar.pack_start(btn_folders, False, False, 0)
        tbar.pack_start(self._make_vsep(), False, False, 2)

        btn_views = self._make_toolbtn("views.svg", "▾", self.toggle_cp_mode)
        tbar.pack_start(btn_views, False, False, 0)
        root.pack_start(tbar, False, False, 0)

        # 3. Address Bar
        abar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        abar.get_style_context().add_class("xp-addressbar")

        addr_lbl = Gtk.Label(label="Address")
        addr_lbl.get_style_context().add_class("xp-address-label")
        abar.pack_start(addr_lbl, False, False, 0)

        addr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        addr_box.get_style_context().add_class("xp-address-box")
        self.addr_icon = make_icon("computer.svg", 16)
        self.addr_entry = Gtk.Entry()
        self.addr_entry.get_style_context().add_class("xp-address-entry")
        self.addr_entry.connect("activate", self.on_address_go)
        down_lbl = Gtk.Label(label="▾")
        down_lbl.set_margin_end(4)

        addr_box.pack_start(self.addr_icon, False, False, 2)
        addr_box.pack_start(self.addr_entry, True, True, 0)
        addr_box.pack_start(down_lbl, False, False, 0)
        abar.pack_start(addr_box, True, True, 0)

        go_btn = Gtk.Button()
        go_btn.get_style_context().add_class("xp-go-btn")
        go_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        go_row.pack_start(make_icon("go-button.svg", 18), False, False, 0)
        go_row.pack_start(Gtk.Label(label="Go"), False, False, 0)
        go_btn.add(go_row)
        go_btn.connect("clicked", self.on_address_go)
        abar.pack_start(go_btn, False, False, 0)

        root.pack_start(abar, False, False, 0)

        # 4. Main Body: Left Blue Task Pane + Right Content Area
        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root.pack_start(body, True, True, 0)

        self.sidebar_scroll = Gtk.ScrolledWindow()
        self.sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.sidebar_scroll.set_size_request(215, -1)
        self.sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.sidebar_box.get_style_context().add_class("xp-sidebar")
        self.sidebar_scroll.add(self.sidebar_box)
        body.pack_start(self.sidebar_scroll, False, False, 0)

        self.content_scroll = Gtk.ScrolledWindow()
        self.content_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.content_holder = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.content_scroll.add(self.content_holder)
        body.pack_start(self.content_scroll, True, True, 0)

        # 5. Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.statusbar.get_style_context().add_class("xp-status-bar")
        self.status_lbl = Gtk.Label(label="My Computer", xalign=0)
        self.statusbar.pack_start(self.status_lbl, True, True, 0)
        root.pack_start(self.statusbar, False, False, 0)

        self.render_current_page()

    def _make_vsep(self):
        sep = Gtk.Box()
        sep.get_style_context().add_class("xp-vsep")
        return sep

    def _make_toolbtn(self, icon_name, text, callback):
        btn = Gtk.Button()
        btn.get_style_context().add_class("xp-toolbtn")
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        row.pack_start(make_icon(icon_name, 24), False, False, 0)
        if text:
            row.pack_start(Gtk.Label(label=text), False, False, 0)
        btn.add(row)
        if callback:
            btn.connect("clicked", lambda *_: callback())
        return btn

    def _make_card(self, title, links, dark_header=False, header_icon=None):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hdr.get_style_context().add_class(
            "xp-card-header-dark" if dark_header else "xp-card-header-light"
        )
        if header_icon:
            hdr.pack_start(make_icon(header_icon, 20), False, False, 0)
        lbl = Gtk.Label(label=title, xalign=0)
        if dark_header:
            lbl.set_markup(f"<span foreground='white' weight='bold'>{GLib.markup_escape_text(title)}</span>")
        else:
            lbl.set_markup(f"<span foreground='#215dc6' weight='bold'>{GLib.markup_escape_text(title)}</span>")
        hdr.pack_start(lbl, True, True, 0)

        chev = Gtk.Button(label="˄")
        chev.get_style_context().add_class("xp-chevron-btn")
        hdr.pack_end(chev, False, False, 0)
        card.pack_start(hdr, False, False, 0)

        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        body.get_style_context().add_class("xp-card-body")
        for item in links:
            if len(item) == 3:
                icon_name, text, cb = item
                btn = Gtk.Button()
                btn.get_style_context().add_class("xp-task-link")
                r = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                r.pack_start(make_icon(icon_name, 16), False, False, 0)
                tl = Gtk.Label(label=text, xalign=0)
                tl.set_line_wrap(True)
                tl.set_max_width_chars(22)
                tl.set_markup(f"<span foreground='#215dc6'>{GLib.markup_escape_text(text)}</span>")
                r.pack_start(tl, True, True, 0)
                btn.add(r)
                btn.connect("clicked", lambda _, c=cb: c())
                body.pack_start(btn, False, False, 0)
            else:
                # Plain detail text
                text, is_bold = item
                dl = Gtk.Label(label=text, xalign=0)
                dl.set_line_wrap(True)
                dl.set_max_width_chars(24)
                if is_bold:
                    dl.set_markup(f"<b>{GLib.markup_escape_text(text)}</b>")
                body.pack_start(dl, False, False, 0)

        def toggle_body(*_):
            vis = body.get_visible()
            body.set_visible(not vis)
            chev.set_label("˅" if vis else "˄")

        chev.connect("clicked", toggle_body)
        card.pack_start(body, False, False, 0)
        return card

    def navigate(self, page):
        play_xp_sound("klick.wav")
        self.history = self.history[: self.history_idx + 1]
        self.history.append(page)
        self.history_idx += 1
        self.render_current_page()

    def go_back(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.render_current_page()

    def go_forward(self):
        if self.history_idx + 1 < len(self.history):
            self.history_idx += 1
            self.render_current_page()

    def go_up(self):
        cur = self.history[self.history_idx]
        if cur.startswith("cat:"):
            self.navigate("configuratiescherm")
        elif cur == "configuratiescherm":
            self.navigate("computer")

    def toggle_cp_mode(self):
        cur = self.history[self.history_idx]
        if cur == "computer":
            self.navigate("configuratiescherm")
        else:
            self.cp_classic = not self.cp_classic
            if cur.startswith("cat:"):
                self.navigate("configuratiescherm")
            else:
                self.render_current_page()

    def on_address_go(self, *_):
        txt = self.addr_entry.get_text().strip()
        low = txt.lower()
        if low in ("deze computer", "my computer", "computer"):
            self.navigate("computer")
        elif low in ("configuratiescherm", "control panel"):
            self.navigate("configuratiescherm")
        elif os.path.isdir(os.path.expanduser(txt)):
            open_in_dolphin(os.path.expanduser(txt))

    def execute_action(self, cmd):
        if cmd == "__SYSTEEM__":
            dlg = SystemPropertiesDialog(self)
            dlg.show_all()
        elif cmd == "__BEELDSCHERM__":
            dlg = DisplayPropertiesDialog(self)
            dlg.show_all()
        elif cmd == "__TAAKBALK__":
            dlg = TaskbarPropertiesDialog(self, initial_tab=0)
            dlg.show_all()
        elif cmd == "__LOGON__":
            dlg = TaskbarPropertiesDialog(self, initial_tab=2)
            dlg.show_all()
        else:
            run_cmd(cmd)

    def render_current_page(self):
        for child in self.sidebar_box.get_children():
            self.sidebar_box.remove(child)
        for child in self.content_holder.get_children():
            self.content_holder.remove(child)

        self.btn_back.set_sensitive(self.history_idx > 0)
        self.btn_fwd.set_sensitive(self.history_idx + 1 < len(self.history))

        cur = self.history[self.history_idx]
        if cur == "computer":
            self._render_my_computer()
        elif cur == "configuratiescherm":
            self._render_control_panel()
        elif cur.startswith("cat:"):
            idx = int(cur.split(":", 1)[1])
            self._render_category_detail(idx)

        self.sidebar_box.show_all()
        self.content_holder.show_all()

    def _render_my_computer(self):
        self.set_title("My Computer")
        pb = load_pixbuf("computer.svg", 24)
        if pb:
            self.set_icon(pb)
        self.addr_icon.set_from_pixbuf(load_pixbuf("computer.svg", 16))
        self.addr_entry.set_text("My Computer")
        self.status_lbl.set_text("6 objects  |  My Computer")

        # Left sidebar cards (System Tasks, Other Places, Details)
        self.sidebar_box.pack_start(
            self._make_card(
                "System Tasks",
                [
                    ("cp-admin.svg", "View system information", lambda: self.execute_action("__SYSTEEM__")),
                    ("cat-software.svg", "Add or remove programs", lambda: run_cmd("bazaar || konsole -e ujust update")),
                    ("controlpanel.svg", "Change a setting", lambda: self.navigate("configuratiescherm")),
                ],
            ),
            False,
            False,
            0,
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "Other Places",
                [
                    ("cp-network.svg", "My Network Places", lambda: open_in_dolphin("remote:/")),
                    ("docs.svg", "My Documents", lambda: open_in_dolphin(os.path.expanduser("~/Documenten"))),
                    ("folder-shared.svg", "Shared Documents", lambda: open_in_dolphin(os.path.expanduser("~/Openbaar"))),
                    ("controlpanel.svg", "Control Panel", lambda: self.navigate("configuratiescherm")),
                ],
            ),
            False,
            False,
            0,
        )
        self.details_card = self._make_card(
            "Details",
            [("My Computer", True), ("System Folder", False)],
        )
        self.sidebar_box.pack_start(self.details_card, False, False, 0)

        # Right white view
        view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        view.get_style_context().add_class("xp-white-view")
        view.set_vexpand(True)

        user_full = GLib.get_real_name() or "King Geoffrey"
        if user_full == "Unknown":
            user_full = "King Geoffrey"

        sections = [
            (
                "Files Stored on This Computer",
                [
                    ("folder-shared.svg", "Shared Documents", os.path.expanduser("~/Openbaar"), "System Folder"),
                    ("docs.svg", f"{user_full}'s Documents", os.path.expanduser("~/Documenten"), "System Folder"),
                ],
            ),
            (
                "Hard Disk Drives",
                [
                    ("hdd.svg", "Local Disk (C:)", "/var/home/king", "Local Disk (Btrfs)\n" + get_disk_usage_str("/var/home/king")),
                    ("hdd.svg", "1TB SSD (D:)", "/var/mnt/schijven/1TB SSD", "Local Disk (Ext4)\n" + get_disk_usage_str("/var/mnt/schijven/1TB SSD")),
                    ("hdd.svg", "Data Disk (E:)", "/var/mnt/6A441A2F4419FE8F", "Local Disk (NTFS)\n" + get_disk_usage_str("/var/mnt/6A441A2F4419FE8F")),
                ],
            ),
            (
                "Devices with Removable Storage",
                [
                    ("cdrom.svg", "CD Drive (F:)", "/run/media/king", "CD-ROM Drive"),
                ],
            ),
        ]

        for sec_title, items in sections:
            st = Gtk.Label(label=sec_title, xalign=0)
            st.get_style_context().add_class("xp-section-title")
            view.pack_start(st, False, False, 0)

            sline = Gtk.Box()
            sline.get_style_context().add_class("xp-section-line")
            view.pack_start(sline, False, False, 0)

            flow = Gtk.FlowBox()
            flow.set_max_children_per_line(3)
            flow.set_min_children_per_line(2)
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_margin_start(14)
            flow.set_margin_bottom(8)

            for ic_name, label_txt, target_path, detail_info in items:
                btn = Gtk.Button()
                btn.get_style_context().add_class("xp-item-btn")
                btn.set_size_request(250, 56)
                hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                hb.pack_start(make_icon(ic_name, 42), False, False, 0)
                lbl = Gtk.Label(label=label_txt, xalign=0)
                hb.pack_start(lbl, True, True, 0)
                btn.add(hb)

                def on_click(_, p=target_path, t=label_txt, d=detail_info):
                    self.status_lbl.set_text(f"{t}  —  {d.replace(chr(10), ' | ')}")
                    open_in_dolphin(p)

                btn.connect("clicked", on_click)
                flow.add(btn)

            view.pack_start(flow, False, False, 0)

        self.content_holder.pack_start(view, True, True, 0)

    def _render_control_panel(self):
        self.set_title("Control Panel")
        pb = load_pixbuf("controlpanel.svg", 24)
        if pb:
            self.set_icon(pb)
        self.addr_icon.set_from_pixbuf(load_pixbuf("controlpanel.svg", 16))
        self.addr_entry.set_text("Control Panel")

        switch_label = (
            "Switch to Category View"
            if self.cp_classic
            else "Switch to Classic View"
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "Control Panel",
                [("controlpanel.svg", switch_label, self.toggle_cp_mode)],
                dark_header=True,
                header_icon="controlpanel.svg",
            ),
            False,
            False,
            0,
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "See Also",
                [
                    ("cp-updates.svg", "Windows Update", lambda: run_cmd("bazaar || konsole -e ujust update")),
                    ("help.svg", "Help and Support", lambda: run_cmd("khelpcenter")),
                    ("controlpanel.svg", "KDE System Settings", lambda: run_cmd([REAL_SYSTEMSETTINGS])),
                ],
            ),
            False,
            False,
            0,
        )

        if self.cp_classic:
            self.status_lbl.set_text(f"{len(CLASSIC_ITEMS)} objects  |  Control Panel (Classic View)")
            view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            view.get_style_context().add_class("xp-white-view")
            view.set_vexpand(True)

            flow = Gtk.FlowBox()
            flow.set_max_children_per_line(6)
            flow.set_min_children_per_line(4)
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_margin_top(14)
            flow.set_margin_start(14)
            flow.set_margin_end(14)
            flow.set_row_spacing(10)
            flow.set_column_spacing(8)

            for title, ic_name, cmd in CLASSIC_ITEMS:
                btn = Gtk.Button()
                btn.get_style_context().add_class("xp-classic-btn")
                btn.set_size_request(100, 86)
                vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
                vb.set_halign(Gtk.Align.CENTER)
                vb.pack_start(make_icon(ic_name, 42), False, False, 0)
                lbl = Gtk.Label(label=title, justify=Gtk.Justification.CENTER)
                lbl.set_line_wrap(True)
                lbl.set_max_width_chars(15)
                vb.pack_start(lbl, False, False, 0)
                btn.add(vb)
                btn.connect("clicked", lambda _, c=cmd: self.execute_action(c))
                flow.add(btn)

            view.pack_start(flow, False, False, 0)
            self.content_holder.pack_start(view, True, True, 0)
        else:
            self.status_lbl.set_text("Control Panel  |  Category View")
            view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            view.get_style_context().add_class("xp-cat-view")
            view.set_vexpand(True)

            heading = Gtk.Label(label="Pick a category", xalign=0)
            heading.get_style_context().add_class("xp-cat-heading")
            view.pack_start(heading, False, False, 0)

            grid = Gtk.Grid()
            grid.set_margin_start(22)
            grid.set_margin_end(22)
            grid.set_margin_bottom(20)
            grid.set_row_spacing(12)
            grid.set_column_spacing(22)

            for idx, (cat_title, cat_icon, cat_desc, _) in enumerate(CATEGORIES):
                btn = Gtk.Button()
                btn.get_style_context().add_class("xp-cat-btn")
                btn.set_hexpand(True)

                hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
                hb.set_valign(Gtk.Align.CENTER)
                hb.pack_start(make_icon(cat_icon, 48), False, False, 0)

                tb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                tb.set_valign(Gtk.Align.CENTER)
                t_lbl = Gtk.Label(label=cat_title, xalign=0)
                t_lbl.get_style_context().add_class("xp-cat-title")
                d_lbl = Gtk.Label(label=cat_desc, xalign=0)
                d_lbl.get_style_context().add_class("xp-cat-desc")
                d_lbl.set_line_wrap(True)
                d_lbl.set_max_width_chars(32)
                tb.pack_start(t_lbl, False, False, 0)
                tb.pack_start(d_lbl, False, False, 0)

                hb.pack_start(tb, True, True, 0)
                btn.add(hb)
                btn.connect("clicked", lambda _, i=idx: self.navigate(f"cat:{i}"))

                col = idx % 2
                row = idx // 2
                grid.attach(btn, col, row, 1, 1)

            view.pack_start(grid, False, False, 0)
            self.content_holder.pack_start(view, True, True, 0)

    def _render_category_detail(self, idx):
        cat_title, cat_icon, cat_desc, subitems = CATEGORIES[idx]
        self.set_title(cat_title)
        self.addr_icon.set_from_pixbuf(load_pixbuf(cat_icon, 16))
        self.addr_entry.set_text(f"Control Panel\\{cat_title}")
        self.status_lbl.set_text(cat_desc)

        self.sidebar_box.pack_start(
            self._make_card(
                "Control Panel",
                [
                    ("controlpanel.svg", "Control Panel Home", lambda: self.navigate("configuratiescherm")),
                    ("controlpanel.svg", "Switch to Classic View", self.toggle_cp_mode),
                ],
                dark_header=True,
                header_icon="controlpanel.svg",
            ),
            False,
            False,
            0,
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "See Also",
                [
                    ("cp-updates.svg", "Windows Update", lambda: run_cmd("bazaar || konsole -e ujust update")),
                    ("help.svg", "Help and Support", lambda: run_cmd("khelpcenter")),
                ],
            ),
            False,
            False,
            0,
        )

        view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        view.get_style_context().add_class("xp-cat-view")
        view.set_vexpand(True)

        heading = Gtk.Label(label=cat_title, xalign=0)
        heading.get_style_context().add_class("xp-cat-heading")
        view.pack_start(heading, False, False, 0)

        subhead = Gtk.Label(label="or pick a Control Panel icon", xalign=0)
        subhead.get_style_context().add_class("xp-cat-subhead")
        view.pack_start(subhead, False, False, 0)

        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        list_box.set_margin_start(24)
        list_box.set_margin_end(24)
        list_box.set_margin_top(6)

        for item_title, item_icon, item_cmd in subitems:
            btn = Gtk.Button()
            btn.get_style_context().add_class("xp-cat-btn")
            hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            hb.pack_start(make_icon(item_icon, 32), False, False, 0)
            lbl = Gtk.Label(label=item_title, xalign=0)
            lbl.get_style_context().add_class("xp-cat-title")
            hb.pack_start(lbl, True, True, 0)
            btn.add(hb)
            btn.connect("clicked", lambda _, c=item_cmd: self.execute_action(c))
            list_box.pack_start(btn, False, False, 0)

        view.pack_start(list_box, False, False, 0)
        self.content_holder.pack_start(view, True, True, 0)


def _sni_get_prop(bus, svc, path, prop, timeout_ms=300):
    try:
        r = bus.call_sync(
            svc,
            path,
            "org.freedesktop.DBus.Properties",
            "Get",
            GLib.Variant("(ss)", ("org.kde.StatusNotifierItem", prop)),
            GLib.VariantType("(v)"),
            Gio.DBusCallFlags.NONE,
            timeout_ms,
            None,
        )
        return r.unpack()[0]
    except Exception:
        return None


def sni_list():
    os.makedirs("/tmp/xp-sni-icons", exist_ok=True)
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        res = bus.call_sync(
            "org.kde.StatusNotifierWatcher",
            "/StatusNotifierWatcher",
            "org.freedesktop.DBus.Properties",
            "Get",
            GLib.Variant("(ss)", ("org.kde.StatusNotifierWatcher", "RegisteredStatusNotifierItems")),
            GLib.VariantType("(v)"),
            Gio.DBusCallFlags.NONE,
            500,
            None,
        )
        items = res.unpack()[0]
    except Exception:
        print("[]")
        return

    out = []
    for item in items:
        if "/" not in item:
            continue
        svc, path = item.split("/", 1)
        path = "/" + path
        status = _sni_get_prop(bus, svc, path, "Status") or "Active"
        if status == "Passive":
            continue
        item_id = _sni_get_prop(bus, svc, path, "Id") or svc
        title = _sni_get_prop(bus, svc, path, "Title") or ""
        icon_name = _sni_get_prop(bus, svc, path, "IconName") or ""
        menu_path = _sni_get_prop(bus, svc, path, "Menu") or "/com/canonical/dbusmenu"

        # Leesbare tooltipnaam bepalen
        nice_title = title.strip()
        if not nice_title:
            low_id = item_id.lower()
            if "discord" in low_id:
                nice_title = "Discord"
            elif "unityhub" in low_id:
                nice_title = "Unity Hub"
            elif "chrome" in low_id:
                nice_title = "Achtergrond-app (Chromium)"
            elif "steam" in low_id:
                nice_title = "Steam"
            else:
                nice_title = item_id

        safe = "".join(c if c.isalnum() else "_" for c in item_id)
        png_path = f"/tmp/xp-sni-icons/{safe}.png"
        if not icon_name and not os.path.exists(png_path):
            pixmaps = _sni_get_prop(bus, svc, path, "IconPixmap", timeout_ms=1200) or []
            if pixmaps:
                try:
                    w, h, argb = min(pixmaps, key=lambda p: abs(p[0] - 32))
                    rgba = bytearray(len(argb))
                    rgba[0::4] = argb[1::4]
                    rgba[1::4] = argb[2::4]
                    rgba[2::4] = argb[3::4]
                    rgba[3::4] = argb[0::4]
                    pb = GdkPixbuf.Pixbuf.new_from_bytes(
                        GLib.Bytes.new(rgba), GdkPixbuf.Colorspace.RGB, True, 8, w, h, w * 4
                    )
                    if w > 48:
                        pb = pb.scale_simple(32, 32, GdkPixbuf.InterpType.BILINEAR)
                    pb.savev(png_path, "png", [], [])
                except Exception:
                    pass

        icon_val = f"file://{png_path}" if os.path.exists(png_path) else icon_name
        if not os.path.exists(png_path) and icon_name:
            base_icon = icon_name.replace("-off-symbolic", "").replace("-symbolic", "")
            for search_dir in (
                "/var/lib/flatpak/exports/share/icons/hicolor/scalable/apps",
                "/var/lib/flatpak/exports/share/icons/hicolor/64x64/apps",
                "/usr/share/icons/hicolor/scalable/apps",
                "/usr/share/icons/hicolor/48x48/apps",
            ):
                for ext in (".svg", ".png"):
                    cand = os.path.join(search_dir, base_icon + ext)
                    if os.path.exists(cand):
                        icon_val = f"file://{cand}"
                        break
                if icon_val.startswith("file://"):
                    break

        out.append(
            {
                "service": svc,
                "path": path,
                "id": item_id,
                "title": nice_title,
                "icon": icon_val,
                "menu": str(menu_path),
            }
        )
    print(json.dumps(out))


def _sni_get_dbusmenu_items(bus, svc, menu_path):
    try:
        bus.call_sync(
            svc,
            menu_path,
            "com.canonical.dbusmenu",
            "AboutToShow",
            GLib.Variant("(i)", (0,)),
            None,
            Gio.DBusCallFlags.NONE,
            400,
            None,
        )
    except Exception:
        pass
    try:
        res = bus.call_sync(
            svc,
            menu_path,
            "com.canonical.dbusmenu",
            "GetLayout",
            GLib.Variant("(iias)", (0, -1, [])),
            GLib.VariantType("(u(ia{sv}av))"),
            Gio.DBusCallFlags.NONE,
            600,
            None,
        )
        _, layout = res.unpack()
        _, _, children = layout
        parsed = []
        for child in children:
            cid, cprops, _ = child
            if not cprops or cprops.get("type") == "separator":
                parsed.append({"id": cid, "separator": True})
            elif cprops.get("visible", True):
                lbl = (cprops.get("label") or "").replace("_", "")
                enabled = cprops.get("enabled", True)
                if lbl:
                    parsed.append({"id": cid, "label": lbl, "enabled": enabled, "separator": False})
        return parsed
    except Exception:
        return []


def _sni_trigger_dbusmenu_item(bus, svc, menu_path, item_id):
    try:
        bus.call_sync(
            svc,
            menu_path,
            "com.canonical.dbusmenu",
            "Event",
            GLib.Variant("(isvu)", (int(item_id), "clicked", GLib.Variant("i", 0), 0)),
            None,
            Gio.DBusCallFlags.NONE,
            500,
            None,
        )
    except Exception:
        pass


def sni_activate(svc, path, menu_path="/com/canonical/dbusmenu"):
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    except Exception:
        return
    # 1. Probeer standaard StatusNotifierItem.Activate
    try:
        bus.call_sync(
            svc,
            path,
            "org.kde.StatusNotifierItem",
            "Activate",
            GLib.Variant("(ii)", (0, 0)),
            None,
            Gio.DBusCallFlags.NONE,
            400,
            None,
        )
    except Exception:
        pass
    # 2. Voor Electron/libappindicator apps (zoals Discord & Unity Hub): activeer ook "Open ..." in DBusMenu
    items = _sni_get_dbusmenu_items(bus, svc, menu_path)
    for it in items:
        if not it.get("separator") and it.get("enabled", True):
            low = it.get("label", "").lower()
            if low.startswith("open") or low.startswith("show") or low.startswith("toon") or low.startswith("weergeven"):
                _sni_trigger_dbusmenu_item(bus, svc, menu_path, it["id"])
                return


def sni_menu(svc, path, menu_path="/com/canonical/dbusmenu", target_x=None, target_y=None):
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    except Exception:
        return
    items = _sni_get_dbusmenu_items(bus, svc, menu_path)
    if not items:
        try:
            bus.call_sync(
                svc,
                path,
                "org.kde.StatusNotifierItem",
                "ContextMenu",
                GLib.Variant("(ii)", (0, 0)),
                None,
                Gio.DBusCallFlags.NONE,
                400,
                None,
            )
        except Exception:
            pass
        return

    provider = Gtk.CssProvider()
    provider.load_from_data(XP_CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    win.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
    win.set_title("StatusNotifierMenu")
    win.set_decorated(False)
    win.set_resizable(False)
    win.set_skip_taskbar_hint(True)
    win.set_skip_pager_hint(True)
    win.set_keep_above(True)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    box.get_style_context().add_class("xp-popup-menu")

    for it in items:
        if it.get("separator"):
            sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            sep.get_style_context().add_class("xp-popup-sep")
            box.pack_start(sep, False, False, 2)
        else:
            btn = Gtk.Button(label=it["label"])
            btn.get_style_context().add_class("xp-popup-item")
            btn.get_child().set_xalign(0.0)
            btn.set_sensitive(bool(it.get("enabled", True)))
            cid = it["id"]

            def on_item_click(_, item_id=cid):
                _sni_trigger_dbusmenu_item(bus, svc, menu_path, item_id)
                Gtk.main_quit()

            btn.connect("clicked", on_item_click)
            box.pack_start(btn, False, False, 0)

    win.add(box)
    win.connect("focus-out-event", lambda *_: Gtk.main_quit())
    win.connect("key-press-event", lambda _, ev: Gtk.main_quit() if ev.keyval == Gdk.KEY_Escape else False)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    # Position cleanly in bottom-right corner at tray icon
    if target_x is None or target_y is None:
        try:
            seat = Gdk.Display.get_default().get_default_seat()
            screen, cx, cy = seat.get_pointer().get_position()
            target_x, target_y = cx, cy
        except Exception:
            target_x, target_y = 1800, 1000

    alloc = win.get_allocation()
    w = max(175, alloc.width)
    h = max(35, alloc.height)
    screen = Gdk.Screen.get_default()
    sw = screen.get_width() if screen else 1920
    sh = screen.get_height() if screen else 1080

    px = min(max(4, target_x - w + 20), sw - w - 4)
    py = max(4, target_y - h - 6)
    if py < 4:
        py = min(target_y + 16, sh - h - 4)

    win.move(px, py)
    win.present()
    Gtk.main()


class XpLogoffDialog(Gtk.Window):
    """Authentic Windows XP 'Log Off Windows' dialog (Switch User / Log Off)."""

    def __init__(self):
        super().__init__(title="Log Off Windows")
        self.set_default_size(340, 200)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(False)

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(outer)

        # Dark blue XP bar at top with Windows XP flag
        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        top.set_size_request(-1, 44)
        top.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.19, 0.61, 1.0))
        lbl_top = Gtk.Label()
        lbl_top.set_markup("<span foreground='white' font_desc='Tahoma Bold 12'>  Log Off Windows</span>")
        lbl_top.set_xalign(0.0)
        top.pack_start(lbl_top, True, True, 8)
        top.pack_end(make_icon("xp-flag.svg", 28), False, False, 12)
        outer.pack_start(top, False, False, 0)

        # Orange highlight line
        sep = Gtk.Box()
        sep.set_size_request(-1, 2)
        sep.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.60, 0.20, 1.0))
        outer.pack_start(sep, False, False, 0)

        # Center blue area with Switch User & Log Off buttons
        mid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=36)
        mid.set_halign(Gtk.Align.CENTER)
        mid.set_valign(Gtk.Align.CENTER)
        mid.set_margin_top(22)
        mid.set_margin_bottom(22)
        mid_wrap = Gtk.EventBox()
        mid_wrap.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.35, 0.49, 0.86, 1.0))
        mid_wrap.add(mid)
        outer.pack_start(mid_wrap, True, True, 0)

        def make_choice(icon_file, title_str, cb):
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            btn = Gtk.Button()
            btn.set_size_request(44, 44)
            btn.add(make_icon(icon_file, 32))
            btn.connect("clicked", cb)
            lbl = Gtk.Label()
            lbl.set_markup(f"<span foreground='white' font_desc='Tahoma Bold 9.5'>{title_str}</span>")
            col.pack_start(btn, False, False, 0)
            col.pack_start(lbl, False, False, 0)
            return col

        def on_switch_user(_):
            play_xp_sound("klick.wav")
            run_cmd(["loginctl", "lock-session"])
            Gtk.main_quit()

        def on_logoff(_):
            play_xp_sound("klick.wav")
            run_cmd(["qdbus-qt6", "org.kde.Shutdown", "/Shutdown", "logout"])
            Gtk.main_quit()

        mid.pack_start(make_choice("cat-users.svg", "Switch User", on_switch_user), False, False, 0)
        mid.pack_start(make_choice("logout.svg", "Log Off", on_logoff), False, False, 0)

        # Bottom bar with Cancel button
        bot = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        bot.set_size_request(-1, 42)
        bot.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.19, 0.61, 1.0))
        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.get_style_context().add_class("xp-push-btn")
        cancel_btn.set_margin_end(14)
        cancel_btn.set_margin_top(8)
        cancel_btn.set_margin_bottom(8)
        cancel_btn.connect("clicked", lambda *_: Gtk.main_quit())
        bot.pack_end(cancel_btn, False, False, 0)
        outer.pack_start(bot, False, False, 0)


class XpTurnOffDialog(Gtk.Window):
    """Authentic Windows XP 'Turn off computer' dialog (Stand By / Turn Off / Restart)."""

    def __init__(self):
        super().__init__(title="Turn off computer")
        self.set_default_size(320, 204)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(box)

        # 1. Top bar (#001961)
        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        top.set_size_request(-1, 38)
        top.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.19, 0.61, 1.0))
        lbl_title = Gtk.Label()
        lbl_title.set_markup("<span foreground='white' font_desc='Tahoma Bold 13'> Turn off computer</span>")
        lbl_title.set_xalign(0.0)
        top.pack_start(lbl_title, True, True, 12)

        flag = make_icon("xp-flag.svg", 28)
        flag.set_margin_end(10)
        top.pack_end(flag, False, False, 0)
        box.pack_start(top, False, False, 0)

        # 2. Middle band (Luna gradient + 3 buttons)
        mid_da = Gtk.DrawingArea()
        mid_da.set_size_request(320, 126)
        mid_da.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)

        self.hover_btn = -1
        self.pressed_btn = -1

        centers_x = [62, 160, 258]
        btn_y = 20
        btn_size = 38
        rad = 6

        def draw_mid(widget, cr):
            w = widget.get_allocated_width()
            h = widget.get_allocated_height()

            # Luna gradient exactly from original XP
            pat = cairo.LinearGradient(0, 0, 0, h)
            pat.add_color_stop_rgb(0.0, 0.44, 0.60, 0.88)
            pat.add_color_stop_rgb(0.4, 0.53, 0.68, 0.93)
            pat.add_color_stop_rgb(1.0, 0.38, 0.53, 0.82)
            cr.set_source(pat)
            cr.rectangle(0, 0, w, h)
            cr.fill()

            # Top white highlight line
            cr.set_source_rgba(1, 1, 1, 0.45)
            cr.set_line_width(1)
            cr.move_to(0, 0.5); cr.line_to(w, 0.5); cr.stroke()

            # Bottom dark shadow line
            cr.set_source_rgba(0, 0.1, 0.4, 0.4)
            cr.move_to(0, h - 0.5); cr.line_to(w, h - 0.5); cr.stroke()

            btns = [
                ("Stand By", (1.0, 0.88, 0.35), (0.98, 0.62, 0.0), (0.80, 0.42, 0.0), "standby"),
                ("Turn Off", (1.0, 0.46, 0.40), (0.90, 0.18, 0.10), (0.70, 0.08, 0.04), "turnoff"),
                ("Restart", (0.50, 0.90, 0.35), (0.24, 0.74, 0.12), (0.12, 0.52, 0.06), "restart"),
            ]

            for idx, (lbl, col_top, col_mid, col_bot, btype) in enumerate(btns):
                cx = centers_x[idx]
                bx = cx - btn_size // 2
                by = btn_y
                is_hov = (self.hover_btn == idx)
                is_prs = (self.pressed_btn == idx)

                # Soft drop shadow
                for s_off, s_alpha in [(3, 0.08), (2, 0.15), (1, 0.25)]:
                    cr.new_sub_path()
                    cr.arc(bx + rad, by + rad + s_off, rad, 3.14, 4.71)
                    cr.arc(bx + btn_size - rad, by + rad + s_off, rad, 4.71, 6.28)
                    cr.arc(bx + btn_size - rad, by + btn_size - rad + s_off, rad, 0, 1.57)
                    cr.arc(bx + rad, by + btn_size - rad + s_off, rad, 1.57, 3.14)
                    cr.close_path()
                    cr.set_source_rgba(0, 0.08, 0.3, s_alpha)
                    cr.fill()

                # Button body
                cr.new_sub_path()
                cr.arc(bx + rad, by + rad, rad, 3.14, 4.71)
                cr.arc(bx + btn_size - rad, by + rad, rad, 4.71, 6.28)
                cr.arc(bx + btn_size - rad, by + btn_size - rad, rad, 0, 1.57)
                cr.arc(bx + rad, by + btn_size - rad, rad, 1.57, 3.14)
                cr.close_path()

                b_pat = cairo.LinearGradient(bx, by, bx, by + btn_size)
                if is_prs:
                    b_pat.add_color_stop_rgb(0.0, *col_bot)
                    b_pat.add_color_stop_rgb(0.5, *col_mid)
                    b_pat.add_color_stop_rgb(1.0, *col_top)
                elif is_hov:
                    b_pat.add_color_stop_rgb(0.0, min(1.0, col_top[0]+0.1), min(1.0, col_top[1]+0.1), min(1.0, col_top[2]+0.1))
                    b_pat.add_color_stop_rgb(0.48, *col_mid)
                    b_pat.add_color_stop_rgb(1.0, *col_bot)
                else:
                    b_pat.add_color_stop_rgb(0.0, *col_top)
                    b_pat.add_color_stop_rgb(0.48, *col_mid)
                    b_pat.add_color_stop_rgb(1.0, *col_bot)
                cr.set_source(b_pat)
                cr.fill_preserve()

                # Outer crisp white/light bevel border
                cr.set_source_rgba(1, 1, 1, 0.95 if is_hov else 0.85)
                cr.set_line_width(1.2 if is_hov else 1.0)
                cr.stroke()

                # Top glossy highlight
                cr.save()
                cr.new_sub_path()
                cr.arc(bx + rad + 0.5, by + rad + 0.5, rad - 0.5, 3.14, 4.71)
                cr.arc(bx + btn_size - rad - 0.5, by + rad + 0.5, rad - 0.5, 4.71, 6.28)
                cr.line_to(bx + btn_size - 1.5, by + btn_size * 0.45)
                cr.curve_to(bx + btn_size * 0.5, by + btn_size * 0.35, bx + btn_size * 0.5, by + btn_size * 0.35, bx + 1.5, by + btn_size * 0.45)
                cr.close_path()
                cr.set_source_rgba(1, 1, 1, 0.45)
                cr.fill()
                cr.restore()

                # Inner symbols in pure white
                cr.set_source_rgb(1, 1, 1)
                cr.set_line_width(2.8)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)

                if btype == "standby":
                    cr.arc(cx, by + btn_size // 2 + 1, 8.5, 5.2, 4.2)
                    cr.stroke()
                    cr.move_to(cx, by + 10)
                    cr.line_to(cx, by + 19)
                    cr.stroke()
                elif btype == "turnoff":
                    cr.arc(cx, by + btn_size // 2, 8.5, 0, 6.28)
                    cr.stroke()
                    cr.move_to(cx, by + 11)
                    cr.line_to(cx, by + btn_size - 11)
                    cr.stroke()
                elif btype == "restart":
                    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                        import math
                        rad_a = math.radians(angle)
                        x1 = cx + math.cos(rad_a) * 3.5
                        y1 = by + btn_size // 2 + math.sin(rad_a) * 3.5
                        x2 = cx + math.cos(rad_a) * 9.5
                        y2 = by + btn_size // 2 + math.sin(rad_a) * 9.5
                        cr.move_to(x1, y1)
                        cr.line_to(x2, y2)
                        cr.stroke()

                # Label below
                cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size(11)
                ext = cr.text_extents(lbl)
                lx = cx - ext.width / 2
                ly = by + btn_size + 24
                # Drop shadow
                cr.set_source_rgba(0, 0.1, 0.35, 0.8)
                cr.move_to(lx + 1, ly + 1); cr.show_text(lbl)
                # Text
                cr.set_source_rgb(1, 1, 1)
                cr.move_to(lx, ly); cr.show_text(lbl)

            return False

        def on_motion(w, ev):
            idx = -1
            for i, cx in enumerate(centers_x):
                if abs(ev.x - cx) <= btn_size // 2 + 4 and abs(ev.y - (btn_y + btn_size // 2)) <= btn_size // 2 + 4:
                    idx = i
                    break
            if idx != self.hover_btn:
                self.hover_btn = idx
                w.queue_draw()

        def on_leave(w, _):
            if self.hover_btn != -1:
                self.hover_btn = -1
                w.queue_draw()

        def on_btn_press(w, ev):
            if ev.button == 1 and self.hover_btn != -1:
                self.pressed_btn = self.hover_btn
                w.queue_draw()

        def on_btn_release(w, ev):
            if ev.button == 1 and self.pressed_btn != -1:
                act = self.pressed_btn
                self.pressed_btn = -1
                w.queue_draw()
                play_xp_sound("klick.wav")
                if act == 0:  # Stand By
                    run_cmd(["systemctl", "suspend"])
                    Gtk.main_quit()
                elif act == 1:  # Turn Off
                    run_cmd(["qdbus-qt6", "org.kde.Shutdown", "/Shutdown", "logoutAndShutdown"])
                    Gtk.main_quit()
                elif act == 2:  # Restart
                    run_cmd(["qdbus-qt6", "org.kde.Shutdown", "/Shutdown", "logoutAndReboot"])
                    Gtk.main_quit()

        mid_da.connect("draw", draw_mid)
        mid_da.connect("motion-notify-event", on_motion)
        mid_da.connect("leave-notify-event", on_leave)
        mid_da.connect("button-press-event", on_btn_press)
        mid_da.connect("button-release-event", on_btn_release)
        box.pack_start(mid_da, True, True, 0)

        # 3. Bottom bar (#001961) with authentic XP Cancel button
        bot_da = Gtk.DrawingArea()
        bot_da.set_size_request(320, 40)
        bot_da.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)

        def draw_bot(widget, cr):
            w = widget.get_allocated_width()
            h = widget.get_allocated_height()
            cr.set_source_rgb(0.0, 0.19, 0.61)
            cr.rectangle(0, 0, w, h)
            cr.fill()

            bx = w - 75 - 12
            by = 9
            bw = 75
            bh = 22

            cr.set_source_rgb(0.0, 0.23, 0.45)
            cr.rectangle(bx, by, bw, bh)
            cr.fill()

            cr.set_source_rgb(0.925, 0.914, 0.847)
            cr.rectangle(bx + 1, by + 1, bw - 2, bh - 2)
            cr.fill()

            cr.set_source_rgb(1, 1, 1)
            cr.move_to(bx + 1, by + bh - 2); cr.line_to(bx + 1, by + 1); cr.line_to(bx + bw - 2, by + 1)
            cr.stroke()

            cr.set_source_rgb(0.55, 0.55, 0.52)
            cr.move_to(bx + bw - 2, by + 2); cr.line_to(bx + bw - 2, by + bh - 2); cr.line_to(bx + 2, by + bh - 2)
            cr.stroke()

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(11)
            cr.set_source_rgb(0, 0, 0)
            ext = cr.text_extents("Cancel")
            cr.move_to(bx + (bw - ext.width) / 2, by + (bh + ext.height) / 2 - 1)
            cr.show_text("Cancel")
            return False

        def on_bot_click(w, ev):
            bx = 320 - 75 - 12
            if bx <= ev.x <= bx + 75 and 9 <= ev.y <= 31:
                play_xp_sound("klick.wav")
                Gtk.main_quit()

        bot_da.connect("draw", draw_bot)
        bot_da.connect("button-press-event", on_bot_click)
        box.pack_start(bot_da, False, False, 0)

        self.connect("key-press-event", lambda _, ev: Gtk.main_quit() if ev.keyval == Gdk.KEY_Escape else False)


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "computer"
    if mode == "sni-list":
        sni_list()
        return
    if mode == "sni-activate" and len(sys.argv) >= 4:
        sni_activate(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) >= 5 else "/com/canonical/dbusmenu")
        return
    if mode == "sni-menu" and len(sys.argv) >= 4:
        tx = int(sys.argv[5]) if len(sys.argv) >= 7 and sys.argv[5].isdigit() else None
        ty = int(sys.argv[6]) if len(sys.argv) >= 7 and sys.argv[6].isdigit() else None
        sni_menu(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) >= 5 else "/com/canonical/dbusmenu", tx, ty)
        return

    provider = Gtk.CssProvider()
    provider.load_from_data(XP_CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "computer"
    if mode in ("systeem", "sysdm.cpl"):
        win = SystemPropertiesDialog()
    elif mode in ("beeldscherm", "desk.cpl", "display", "vormgeving"):
        win = DisplayPropertiesDialog()
    elif mode in ("taakbalk", "eigenschappen", "taskbar"):
        win = TaskbarPropertiesDialog(initial_tab=0)
    elif mode in ("startmenu", "menu-start"):
        win = TaskbarPropertiesDialog(initial_tab=1)
    elif mode in ("logon", "aanmelden", "gebruikersaccounts"):
        win = TaskbarPropertiesDialog(initial_tab=2)
    elif mode in ("taakbeheer", "taskmgr", "taskmanager", "taskmgr-perf", "taskmgr-proc"):
        initial_tab = 2 if mode == "taskmgr-perf" else (1 if mode == "taskmgr-proc" else 0)
        win = TaskManagerWindow(initial_tab=initial_tab)
    elif mode in ("msn", "messenger"):
        msn_script = os.path.join(BASE_DIR, "xp-msn.py")
        if not os.path.exists(msn_script):
            msn_script = os.path.expanduser("~/.local/share/xp-startknop/xp-msn.py")
        subprocess.Popen([sys.executable, msn_script] + sys.argv[2:])
        return
    elif mode in ("uitvoeren", "run"):
        win = RunDialog()
    elif mode in ("afmelden", "logoff"):
        win = XpLogoffDialog()
    elif mode in ("shutdown", "turnoff", "afsluiten"):
        win = XpTurnOffDialog()
    elif mode in ("configuratiescherm", "control", "instellingen"):
        win = XpExplorerWindow("configuratiescherm")
    elif mode in ("klassiek", "classic"):
        win = XpExplorerWindow("klassiek")
    else:
        win = XpExplorerWindow("computer")

    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    if hasattr(win, "initial_tab") and win.initial_tab > 0:
        win.notebook.set_current_page(win.initial_tab)
    Gtk.main()


if __name__ == "__main__":
    main()
