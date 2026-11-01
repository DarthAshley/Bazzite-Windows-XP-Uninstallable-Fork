#!/usr/bin/env python3
"""
Windows XP Verkenner, Configuratiescherm, Systeemeigenschappen en Uitvoeren
voor Bazzite KDE (XP Start).
Gebruik:
  xp-verkenner.py [computer | configuratiescherm | klassiek | systeem | uitvoeren]
"""
import os
import sys
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
        return f"Totale grootte: {total_gb:.1f} GB\nBeschikbaar: {free_gb:.1f} GB"
    except Exception:
        return "Systeemmap"


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
"""

CLASSIC_ITEMS = [
    ("Beeldscherm", "cp-display.svg", "__BEELDSCHERM__"),
    ("Beveiligingscentrum", "xp-shield.svg", "kcmshell6 kcm_updates"),
    ("Bluetooth-apparaten", "tray-bt.svg", "kcmshell6 kcm_bluetooth"),
    ("Datum en tijd", "cat-datetime.svg", "kcmshell6 kcm_clock"),
    ("Energiebeheer", "cp-power.svg", "kcmshell6 kcm_powerdevilprofilesconfig"),
    ("Gebruikersaccounts", "cat-users.svg", "kcmshell6 kcm_users"),
    ("Geluiden en\naudioapparaten", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
    ("Geplande taken", "cp-updates.svg", "kcmshell6 kcm_autostart"),
    ("Internetopties", "cat-network.svg", "kcmshell6 kcm_proxy"),
    ("Kleur en\nvormgeving", "cat-appearance.svg", "__BEELDSCHERM__"),
    ("Landinstellingen", "defapps.svg", "kcmshell6 kcm_regionandlang"),
    ("Lettertypen", "cp-fonts.svg", "kcmshell6 kcm_fontinst"),
    ("Mapopties", "cp-folderopts.svg", "kcmshell6 kcm_filetypes"),
    ("Muis", "cp-mouse.svg", "kcmshell6 kcm_mouse"),
    ("Netwerk-\nverbindingen", "cp-network.svg", "kcmshell6 kcm_networkmanagement"),
    ("Printers en faxen", "printers.svg", "kcmshell6 kcm_printer_manager"),
    ("Programmatoegang\nen standaarden", "defapps.svg", "kcmshell6 kcm_componentchooser"),
    ("Scanners en\ncamera's", "pics.svg", "kcmshell6 kcm_kamera"),
    ("Software", "cat-software.svg", "flatpak run io.github.kolunmi.Bazaar || kcmshell6 kcm_updates"),
    ("Spelbesturingen", "cp-gamepad.svg", "kcmshell6 kcm_gamecontroller"),
    ("Spraak", "cp-speech.svg", "kcmshell6 kcm_soundtheme"),
    ("Systeem", "cp-system.svg", "__SYSTEEM__"),
    ("Systeembeheer", "cp-admin.svg", "plasma-systemmonitor"),
    ("Taakbalk en\nmenu Start", "cp-taskbar.svg", "__TAAKBALK__"),
    ("Toegankelijkheids-\nopties", "cat-access.svg", "kcmshell6 kcm_access"),
    ("Toetsenbord", "cp-keyboard.svg", "kcmshell6 kcm_keyboard"),
    ("Windows Firewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
    ("Draadloos netwerk\ninstellen", "cp-wireless.svg", "kcmshell6 kcm_networkmanagement"),
]

CATEGORIES = [
    (
        "Vormgeving en thema's",
        "cat-appearance.svg",
        "Het thema van de computer wijzigen, bureaubladachtergrond of schermresolutie aanpassen",
        [
            ("Het thema van de computer wijzigen", "cat-appearance.svg", "__BEELDSCHERM__"),
            ("De bureaubladachtergrond wijzigen", "cp-display.svg", "kcmshell6 kcm_wallpaper"),
            ("De schermresolutie aanpassen", "cp-display.svg", "kcmshell6 kcm_kscreen"),
            ("Beeldscherm", "cp-display.svg", "__BEELDSCHERM__"),
            ("Taakbalk en menu Start", "cp-taskbar.svg", "__TAAKBALK__"),
            ("Mapopties", "cp-folderopts.svg", "kcmshell6 kcm_filetypes"),
            ("Lettertypen", "cp-fonts.svg", "kcmshell6 kcm_fontinst"),
        ],
    ),
    (
        "Printers en andere hardware",
        "cat-printers.svg",
        "Printers, muis, toetsenbord, spelbesturingen en bluetooth-apparaten instellen",
        [
            ("Geïnstalleerde printers of faxprinters weergeven", "printers.svg", "kcmshell6 kcm_printer_manager"),
            ("Een printer toevoegen", "printers.svg", "kcmshell6 kcm_printer_manager"),
            ("Muis", "cp-mouse.svg", "kcmshell6 kcm_mouse"),
            ("Toetsenbord", "cp-keyboard.svg", "kcmshell6 kcm_keyboard"),
            ("Spelbesturingen", "cp-gamepad.svg", "kcmshell6 kcm_gamecontroller"),
            ("Bluetooth-apparaten", "tray-bt.svg", "kcmshell6 kcm_bluetooth"),
        ],
    ),
    (
        "Netwerk- en internetverbindingen",
        "cat-network.svg",
        "Verbinding met internet en thuisnetwerk maken, firewall en netwerkadapters configureren",
        [
            ("Een verbinding met internet instellen of wijzigen", "cat-network.svg", "kcmshell6 kcm_networkmanagement"),
            ("Netwerkverbindingen", "cp-network.svg", "kcmshell6 kcm_networkmanagement"),
            ("Draadloos netwerk instellen", "cp-wireless.svg", "kcmshell6 kcm_networkmanagement"),
            ("Windows Firewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
            ("Internetopties", "cat-network.svg", "kcmshell6 kcm_proxy"),
        ],
    ),
    (
        "Gebruikersaccounts",
        "cat-users.svg",
        "Gebruikersaccounts, wachtwoorden en aanmeldingsopties wijzigen",
        [
            ("Een account wijzigen", "cat-users.svg", "kcmshell6 kcm_users"),
            ("Een nieuwe account maken", "cat-users.svg", "kcmshell6 kcm_users"),
            ("Aanmeldingsbeheer (SDDM)", "cat-users.svg", "kcmshell6 kcm_plasmalogin"),
        ],
    ),
    (
        "Software",
        "cat-software.svg",
        "Programma's en onderdelen installeren, bijwerken of verwijderen",
        [
            ("Programma's wijzigen of verwijderen", "cat-software.svg", "flatpak run io.github.kolunmi.Bazaar || kcmshell6 kcm_updates"),
            ("Nieuwe programma's toevoegen", "cat-software.svg", "flatpak run io.github.kolunmi.Bazaar || kcmshell6 kcm_updates"),
            ("Programmatoegang en standaardinstellingen", "defapps.svg", "kcmshell6 kcm_componentchooser"),
        ],
    ),
    (
        "Datum, tijd, taal en landinstellingen",
        "cat-datetime.svg",
        "Datum, tijd, tijdzone, taal en getalnotatie wijzigen",
        [
            ("De datum en de tijd wijzigen", "cat-datetime.svg", "kcmshell6 kcm_clock"),
            ("De indeling van getallen, datums en tijden wijzigen", "defapps.svg", "kcmshell6 kcm_regionandlang"),
            ("Datum en tijd", "cat-datetime.svg", "kcmshell6 kcm_clock"),
            ("Landinstellingen", "defapps.svg", "kcmshell6 kcm_regionandlang"),
        ],
    ),
    (
        "Geluiden, spraak en audioapparaten",
        "cat-sound.svg",
        "Het geluidsvolume en het geluidsthema wijzigen, luidsprekers en microfoon instellen",
        [
            ("Het systeemvolume aanpassen", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
            ("Het geluidsthema wijzigen", "cp-speech.svg", "kcmshell6 kcm_soundtheme"),
            ("Geluiden en audioapparaten", "cp-sound.svg", "kcmshell6 kcm_pulseaudio"),
        ],
    ),
    (
        "Toegankelijkheidsopties",
        "cat-access.svg",
        "Het contrast, geluid en muisgedrag aanpassen voor beter zicht, gehoor en mobiliteit",
        [
            ("Toegankelijkheidsopties configureren", "cat-access.svg", "kcmshell6 kcm_access"),
            ("Schermkleur en nachtlicht aanpassen", "cp-display.svg", "kcmshell6 kcm_nightlight"),
        ],
    ),
    (
        "Prestaties en onderhoud",
        "cat-perf.svg",
        "Systeeminformatie bekijken, schijfruimte vrijmaken, energiebeheer en systeemtaken",
        [
            ("Basisinformatie over uw computer weergeven", "cp-system.svg", "__SYSTEEM__"),
            ("Visuele effecten aanpassen", "cat-appearance.svg", "kcmshell6 kcm_animations"),
            ("Schijfruimte vrijmaken / Systeemmonitor", "cp-clean.svg", "plasma-systemmonitor"),
            ("Systeem", "cp-system.svg", "__SYSTEEM__"),
            ("Energiebeheer", "cp-power.svg", "kcmshell6 kcm_powerdevilprofilesconfig"),
            ("Systeembeheer", "cp-admin.svg", "plasma-systemmonitor"),
        ],
    ),
    (
        "Beveiligingscentrum",
        "xp-shield.svg",
        "De status van uw beveiligingsinstellingen, firewall en automatische updates controleren",
        [
            ("Windows Firewall", "cp-firewall.svg", "kcmshell6 kcm_netpref"),
            ("Automatische updates", "cp-updates.svg", "kcmshell6 kcm_updates"),
            ("App-machtigingen", "xp-shield.svg", "kcmshell6 kcm_app-permissions"),
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
    """Exacte replica van het Windows XP 'Systeemeigenschappen' venster."""

    def __init__(self, parent=None):
        super().__init__(title="Systeemeigenschappen")
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
        for t in ["Systeemherstel", "Automatische updates", "Verbindingen van buitenaf"]:
            b = Gtk.Button(label=t)
            b.get_style_context().add_class("xp-tab-btn")
            b.set_hexpand(True)
            row1.pack_start(b, True, True, 0)
        vbox.pack_start(row1, False, False, 0)

        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        for idx, t in enumerate(["Algemeen", "Computernaam", "Hardware", "Geavanceerd"]):
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

        add_header("Systeem:")
        add_indent("Microsoft Windows XP")
        add_indent("Professional")
        add_indent("Versie 2002")
        add_indent("Service Pack 3")

        sep1 = Gtk.Box()
        sep1.set_size_request(-1, 8)
        right_col.pack_start(sep1, False, False, 0)

        add_header("Geregistreerd voor:")
        add_indent(user_name)
        add_indent("Steel Hull Studio")
        add_indent("76456-640-1803887-23173")

        sep2 = Gtk.Box()
        sep2.set_size_request(-1, 8)
        right_col.pack_start(sep2, False, False, 0)

        add_header("Computer:")
        add_indent(cpu_model)
        add_indent(f"3.70 GHz, {ram_gb}")
        add_indent("Extensie voor fysiek adres")

        page.pack_start(right_col, True, True, 0)

        # Bottom OK / Annuleren / Toepassen buttons
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)

        for label, close_win in [("OK", True), ("Annuleren", True), ("Toepassen", False)]:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("xp-push-btn")
            if not close_win:
                btn.set_sensitive(False)
            else:
                btn.connect("clicked", lambda *_: self.destroy())
            btn_row.pack_start(btn, False, False, 0)

        vbox.pack_start(btn_row, False, False, 0)


class DisplayPropertiesDialog(Gtk.Window):
    """Exacte replica van 'Eigenschappen voor Beeldscherm' (Display Properties)."""

    def __init__(self, parent=None):
        super().__init__(title="Eigenschappen voor Beeldscherm")
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
            ("Thema's", lambda: run_cmd("kcmshell6 kcm_lookandfeel")),
            ("Bureaublad", lambda: run_cmd("kcmshell6 kcm_wallpaper")),
            ("Schermbeveiliging", lambda: run_cmd("kcmshell6 kcm_screenlocker")),
            ("Vormgeving", None),
            ("Instellingen", lambda: run_cmd("kcmshell6 kcm_kscreen")),
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

        for label_txt, options in [
            ("Vensters en knoppen:", ["Windows XP-stijl", "Klassieke Windows-stijl"]),
            ("Kleurenschema:", ["Standaard (blauw)", "Olijfgroen", "Zilver"]),
            ("Tekengrootte:", ["Normaal", "Grote lettertypen", "Extra grote lettertypen"]),
        ]:
            lbl = Gtk.Label(label=label_txt, xalign=0)
            left_col.pack_start(lbl, False, False, 0)
            combo = Gtk.ComboBoxText()
            for opt in options:
                combo.append_text(opt)
            combo.set_active(0)
            left_col.pack_start(combo, False, False, 2)

        bottom_row.pack_start(left_col, True, True, 0)

        right_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        right_col.set_valign(Gtk.Align.END)

        btn_eff = Gtk.Button(label="Effecten...")
        btn_eff.get_style_context().add_class("xp-push-btn")
        btn_eff.connect("clicked", lambda *_: run_cmd("kcmshell6 kcm_animations"))

        btn_adv = Gtk.Button(label="Geavanceerd")
        btn_adv.get_style_context().add_class("xp-push-btn")
        btn_adv.connect("clicked", lambda *_: run_cmd("kcmshell6 kcm_colors"))

        right_col.pack_start(btn_eff, False, False, 0)
        right_col.pack_start(btn_adv, False, False, 0)
        bottom_row.pack_start(right_col, False, False, 0)

        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)
        for label, close_win in [("OK", True), ("Annuleren", True), ("Toepassen", False)]:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("xp-push-btn")
            if not close_win:
                btn.set_sensitive(False)
            else:
                btn.connect("clicked", lambda *_: self.destroy())
            btn_row.pack_start(btn, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)


class TaskbarPropertiesDialog(Gtk.Window):
    """Exacte replica van 'Eigenschappen voor Taakbalk en menu Start'."""

    def __init__(self, parent=None):
        super().__init__(title="Eigenschappen voor Taakbalk en menu Start")
        self.set_default_size(390, 420)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        if parent:
            self.set_transient_for(parent)
        icon_pb = load_pixbuf("cp-taskbar.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        self.add(vbox)

        tabs = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        for idx, t_label in enumerate(["Taakbalk", "Menu Start"]):
            b = Gtk.Button(label=t_label)
            b.get_style_context().add_class("xp-tab-btn")
            if idx == 0:
                b.get_style_context().add_class("xp-tab-active")
            tabs.pack_start(b, False, False, 0)
        vbox.pack_start(tabs, False, False, 0)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        page.get_style_context().add_class("xp-tab-page")
        vbox.pack_start(page, True, True, 0)

        grp1 = Gtk.Label(xalign=0)
        grp1.set_markup("<span foreground='#1f4fd5' weight='bold'>Vormgeving van de taakbalk</span>")
        page.pack_start(grp1, False, False, 2)

        for txt, checked in [
            ("De taakbalk vergrendelen", True),
            ("De taakbalk automatisch verbergen", False),
            ("De taakbalk altijd op de voorgrond weergeven", True),
            ("Gelijksoortige taakbalkknoppen groeperen", True),
            ("Werkbalk Snel starten weergeven", False),
        ]:
            chk = Gtk.CheckButton(label=txt)
            chk.set_active(checked)
            page.pack_start(chk, False, False, 0)

        sep = Gtk.Box()
        sep.set_size_request(-1, 8)
        page.pack_start(sep, False, False, 0)

        grp2 = Gtk.Label(xalign=0)
        grp2.set_markup("<span foreground='#1f4fd5' weight='bold'>Systeemvak</span>")
        page.pack_start(grp2, False, False, 2)

        for txt, checked in [
            ("De klok weergeven", True),
            ("Niet-actieve pictogrammen opruimen", True),
        ]:
            chk = Gtk.CheckButton(label=txt)
            chk.set_active(checked)
            page.pack_start(chk, False, False, 0)

        tip = Gtk.Label(
            label="Tip: u kunt het menu Start ook direct vergroten of verkleinen door aan de boven- of rechterrand van het menu Start te slepen.",
            xalign=0,
        )
        tip.set_line_wrap(True)
        tip.set_max_width_chars(46)
        page.pack_start(tip, False, False, 6)

        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_row.set_margin_top(8)
        btn_row.set_halign(Gtk.Align.END)
        for label in ["OK", "Annuleren", "Toepassen"]:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("xp-push-btn")
            btn.connect("clicked", lambda *_: self.destroy())
            btn_row.pack_start(btn, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)


class RunDialog(Gtk.Window):
    """Exacte replica van het Windows XP 'Uitvoeren' venster."""

    def __init__(self):
        super().__init__(title="Uitvoeren")
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
            label="Geef de naam van een programma, map, document of\ninternetbron op en Windows zal deze voor u openen.",
            xalign=0,
        )
        top.pack_start(desc, True, True, 0)
        vbox.pack_start(top, False, False, 0)

        mid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl = Gtk.Label(label="Openen:", xalign=0)
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

        cancel_btn = Gtk.Button(label="Annuleren")
        cancel_btn.get_style_context().add_class("xp-push-btn")
        cancel_btn.connect("clicked", lambda *_: Gtk.main_quit())

        browse_btn = Gtk.Button(label="Bladeren...")
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
    """Authentieke Windows XP 'Windows Taakbeheer' (Task Manager) met Toepassingen, Processen en groene Prestatie-grafieken."""

    def __init__(self):
        super().__init__(title="Windows Taakbeheer")
        self.set_default_size(435, 475)
        self.set_position(Gtk.WindowPosition.CENTER)
        icon_pb = load_pixbuf("cp-perf.svg", 24)
        if icon_pb:
            self.set_icon(icon_pb)

        self.cpu_history = [12] * 60
        self.mem_history = [35] * 60
        self.last_cpu_stat = self._read_cpu_stat()
        self.proc_count = 0
        self.cur_cpu_pct = 5
        self.cur_mem_mb = 2048
        self.total_mem_mb = 16384

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.get_style_context().add_class("xp-window")
        self.add(vbox)

        menubar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        menubar.get_style_context().add_class("xp-menubar")
        for m_txt in ("Bestand", "Opties", "Beeld", "Afsluiten", "Help"):
            mb = Gtk.Button(label=m_txt)
            mb.get_style_context().add_class("xp-menubar-btn")
            if m_txt == "Bestand":
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

        # Tab 1: Toepassingen
        app_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        app_tab.set_margin_start(8)
        app_tab.set_margin_end(8)
        app_tab.set_margin_top(8)
        app_tab.set_margin_bottom(8)

        self.app_store = Gtk.ListStore(str, str, int)
        app_tree = Gtk.TreeView(model=self.app_store)
        for idx, col_title in enumerate(("Taak", "Status")):
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
        new_task_btn = Gtk.Button(label="Nieuwe taak...")
        new_task_btn.set_size_request(105, 24)
        new_task_btn.connect("clicked", lambda *_: run_cmd([sys.executable, os.path.abspath(__file__), "uitvoeren"]))
        end_task_btn = Gtk.Button(label="Taak beëindigen")
        end_task_btn.set_size_request(115, 24)
        end_task_btn.connect("clicked", self._on_kill_selected_app)
        app_btn_row.pack_end(new_task_btn, False, False, 0)
        app_btn_row.pack_end(end_task_btn, False, False, 0)
        app_tab.pack_start(app_btn_row, False, False, 0)
        self.notebook.append_page(app_tab, Gtk.Label(label="Toepassingen"))

        # Tab 2: Processen
        proc_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        proc_tab.set_margin_start(8)
        proc_tab.set_margin_end(8)
        proc_tab.set_margin_top(8)
        proc_tab.set_margin_bottom(8)

        self.proc_store = Gtk.ListStore(str, str, str, str, int)
        proc_tree = Gtk.TreeView(model=self.proc_store)
        for idx, col_title in enumerate(("Procesnaam", "Gebruikersnaam", "CPU", "Geheugengebruik")):
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
        proc_chk = Gtk.CheckButton(label="Processen van alle gebruikers weergeven")
        proc_chk.set_active(True)
        proc_btn_row.pack_start(proc_chk, False, False, 0)
        end_proc_btn = Gtk.Button(label="Proces beëindigen")
        end_proc_btn.set_size_request(125, 24)
        end_proc_btn.connect("clicked", self._on_kill_selected_proc)
        proc_btn_row.pack_end(end_proc_btn, False, False, 0)
        proc_tab.pack_start(proc_btn_row, False, False, 0)
        self.notebook.append_page(proc_tab, Gtk.Label(label="Processen"))

        # Tab 3: Prestaties (met zwart/groene Windows XP grafieken)
        perf_tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        perf_tab.set_margin_start(8)
        perf_tab.set_margin_end(8)
        perf_tab.set_margin_top(8)
        perf_tab.set_margin_bottom(8)

        cpu_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cpu_gauge_frame = Gtk.Frame(label=" CPU-gebruik ")
        self.cpu_gauge_area = Gtk.DrawingArea()
        self.cpu_gauge_area.set_size_request(95, 86)
        self.cpu_gauge_area.connect("draw", self._draw_cpu_gauge)
        cpu_gauge_frame.add(self.cpu_gauge_area)
        cpu_row.pack_start(cpu_gauge_frame, False, False, 0)

        cpu_hist_frame = Gtk.Frame(label=" Geschiedenis van CPU-gebruik ")
        self.cpu_hist_area = Gtk.DrawingArea()
        self.cpu_hist_area.set_size_request(260, 86)
        self.cpu_hist_area.connect("draw", self._draw_cpu_hist)
        cpu_hist_frame.add(self.cpu_hist_area)
        cpu_row.pack_start(cpu_hist_frame, True, True, 0)
        perf_tab.pack_start(cpu_row, False, False, 0)

        mem_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        mem_gauge_frame = Gtk.Frame(label=" Wisselbestand ")
        self.mem_gauge_area = Gtk.DrawingArea()
        self.mem_gauge_area.set_size_request(95, 86)
        self.mem_gauge_area.connect("draw", self._draw_mem_gauge)
        mem_gauge_frame.add(self.mem_gauge_area)
        mem_row.pack_start(mem_gauge_frame, False, False, 0)

        mem_hist_frame = Gtk.Frame(label=" Geschiedenis van wisselbestandgebruik ")
        self.mem_hist_area = Gtk.DrawingArea()
        self.mem_hist_area.set_size_request(260, 86)
        self.mem_hist_area.connect("draw", self._draw_mem_hist)
        mem_hist_frame.add(self.mem_hist_area)
        mem_row.pack_start(mem_hist_frame, True, True, 0)
        perf_tab.pack_start(mem_row, False, False, 0)

        stats_grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        self.lbl_totals = Gtk.Label(label="Ingangen:  42180\nThreads:   1480\nProcessen: 215", xalign=0)
        self.lbl_phys = Gtk.Label(label="Totaal:      16384000\nBeschikbaar: 10240000\nSysteemcache: 4120000", xalign=0)
        for idx, (f_title, w_lbl) in enumerate(((" Totalen ", self.lbl_totals), (" Fysiek geheugen (kB) ", self.lbl_phys))):
            fr = Gtk.Frame(label=f_title)
            w_lbl.set_margin_start(6)
            w_lbl.set_margin_end(6)
            w_lbl.set_margin_top(4)
            w_lbl.set_margin_bottom(4)
            fr.add(w_lbl)
            fr.set_hexpand(True)
            stats_grid.attach(fr, idx, 0, 1, 1)
        perf_tab.pack_start(stats_grid, False, False, 0)
        self.notebook.append_page(perf_tab, Gtk.Label(label="Prestaties"))

        self.statusbar = Gtk.Label(label="Processen: --   |   CPU-gebruik: --%   |   Geheugengebruik: -- MB", xalign=0)
        self.statusbar.get_style_context().add_class("xp-statusbar")
        vbox.pack_start(self.statusbar, False, False, 0)

        self._refresh_stats()
        self._refresh_processes()
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
        pct = max(1, min(100, int(round(100.0 * (dt - didle) / dt))))
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
                f"Totaal:       {tot_kb}\nBeschikbaar:  {avail_kb}\nSysteemcache: {cached_kb}"
            )
        except Exception:
            pass

        self.lbl_totals.set_text(
            f"Ingangen:   {self.proc_count * 142}\nThreads:    {self.proc_count * 6}\nProcessen:  {self.proc_count}"
        )
        self.statusbar.set_text(
            f"Processen: {self.proc_count}     |     CPU-gebruik: {self.cur_cpu_pct}%     |     Geheugengebruik: {self.cur_mem_mb} MB / {self.total_mem_mb} MB"
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
                kb_str = f"{int(rss_s):,} kB".replace(",", ".")
                self.proc_store.append([comm, usr, f"{pcpu}%", kb_str, pid])
                if any(k in comm.lower() for k in gui_keywords):
                    self.app_store.append([comm, "Actief", pid])
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
    Windows XP Verkenner voor 'Deze computer' én 'Configuratiescherm'
    (Categorieweergave + Klassieke weergave).
    """

    def __init__(self, initial_page="computer"):
        super().__init__(title="Deze computer")
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
            ("Bestand", lambda: self.destroy()),
            ("Bewerken", None),
            ("Beeld", lambda: self.toggle_cp_mode()),
            ("Favorieten", lambda: open_in_dolphin(os.path.expanduser("~"))),
            ("Extra", lambda: run_cmd("kcmshell6 kcm_filetypes")),
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

        self.btn_back = self._make_toolbtn("back.svg", "Terug  ▾", self.go_back)
        self.btn_fwd = self._make_toolbtn("forward.svg", "▾", self.go_forward)
        self.btn_up = self._make_toolbtn("folder-up.svg", None, self.go_up)

        tbar.pack_start(self.btn_back, False, False, 0)
        tbar.pack_start(self.btn_fwd, False, False, 0)
        tbar.pack_start(self.btn_up, False, False, 0)
        tbar.pack_start(self._make_vsep(), False, False, 2)

        btn_search = self._make_toolbtn("search.svg", "Zoeken", lambda: run_cmd("krunner"))
        btn_folders = self._make_toolbtn(
            "folder.svg", "Mappen", lambda: open_in_dolphin(os.path.expanduser("~"))
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

        addr_lbl = Gtk.Label(label="Adres")
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
        go_row.pack_start(Gtk.Label(label="Ga naar"), False, False, 0)
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
        self.status_lbl = Gtk.Label(label="Deze computer", xalign=0)
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
            dlg = TaskbarPropertiesDialog(self)
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
        self.set_title("Deze computer")
        pb = load_pixbuf("computer.svg", 24)
        if pb:
            self.set_icon(pb)
        self.addr_icon.set_from_pixbuf(load_pixbuf("computer.svg", 16))
        self.addr_entry.set_text("Deze computer")
        self.status_lbl.set_text("6 objecten  |  Deze computer")

        # Left sidebar cards (Systeemtaken, Andere locaties, Details)
        self.sidebar_box.pack_start(
            self._make_card(
                "Systeemtaken",
                [
                    ("cp-admin.svg", "Systeeminformatie weergeven", lambda: self.execute_action("__SYSTEEM__")),
                    ("cat-software.svg", "Programma's installeren of verwijderen", lambda: run_cmd("flatpak run io.github.kolunmi.Bazaar || kcmshell6 kcm_updates")),
                    ("controlpanel.svg", "Een instelling wijzigen", lambda: self.navigate("configuratiescherm")),
                ],
            ),
            False,
            False,
            0,
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "Andere locaties",
                [
                    ("cp-network.svg", "Mijn netwerklocaties", lambda: open_in_dolphin("remote:/")),
                    ("docs.svg", "Mijn documenten", lambda: open_in_dolphin(os.path.expanduser("~/Documenten"))),
                    ("folder-shared.svg", "Gedeelde documenten", lambda: open_in_dolphin(os.path.expanduser("~/Openbaar"))),
                    ("controlpanel.svg", "Configuratiescherm", lambda: self.navigate("configuratiescherm")),
                ],
            ),
            False,
            False,
            0,
        )
        self.details_card = self._make_card(
            "Details",
            [("Deze computer", True), ("Systeemmap", False)],
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
                "Bestanden op deze computer",
                [
                    ("folder-shared.svg", "Gedeelde documenten", os.path.expanduser("~/Openbaar"), "Systeemmap"),
                    ("docs.svg", f"Documenten van {user_full}", os.path.expanduser("~/Documenten"), "Systeemmap"),
                ],
            ),
            (
                "Harde-schijfstations",
                [
                    ("hdd.svg", "Lokale schijf (C:)", "/var/home/king", "Lokaal station (Btrfs)\n" + get_disk_usage_str("/var/home/king")),
                    ("hdd.svg", "1TB SSD (D:)", "/var/mnt/schijven/1TB SSD", "Lokaal station (Ext4)\n" + get_disk_usage_str("/var/mnt/schijven/1TB SSD")),
                    ("hdd.svg", "Data Schijf (E:)", "/var/mnt/6A441A2F4419FE8F", "Lokaal station (NTFS)\n" + get_disk_usage_str("/var/mnt/6A441A2F4419FE8F")),
                ],
            ),
            (
                "Apparaten met verwisselbare opslag",
                [
                    ("cdrom.svg", "Dvd-rw-station (F:)", "/run/media/king", "Cd-rom-station"),
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
        self.set_title("Configuratiescherm")
        pb = load_pixbuf("controlpanel.svg", 24)
        if pb:
            self.set_icon(pb)
        self.addr_icon.set_from_pixbuf(load_pixbuf("controlpanel.svg", 16))
        self.addr_entry.set_text("Configuratiescherm")

        switch_label = (
            "Schakel over naar categorieweergave"
            if self.cp_classic
            else "Schakel over naar klassieke weergave"
        )
        self.sidebar_box.pack_start(
            self._make_card(
                "Configuratiescherm",
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
                "Zie ook",
                [
                    ("cp-updates.svg", "Windows Update", lambda: run_cmd("kcmshell6 kcm_updates")),
                    ("help.svg", "Help en ondersteuning", lambda: run_cmd("khelpcenter")),
                    ("controlpanel.svg", "KDE Systeeminstellingen", lambda: run_cmd([REAL_SYSTEMSETTINGS])),
                ],
            ),
            False,
            False,
            0,
        )

        if self.cp_classic:
            self.status_lbl.set_text(f"{len(CLASSIC_ITEMS)} objecten  |  Configuratiescherm (Klassieke weergave)")
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
            self.status_lbl.set_text("Configuratiescherm  |  Categorieweergave")
            view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            view.get_style_context().add_class("xp-cat-view")
            view.set_vexpand(True)

            heading = Gtk.Label(label="Kies een categorie", xalign=0)
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
        self.addr_entry.set_text(f"Configuratiescherm\\{cat_title}")
        self.status_lbl.set_text(cat_desc)

        self.sidebar_box.pack_start(
            self._make_card(
                "Configuratiescherm",
                [
                    ("controlpanel.svg", "Configuratiescherm (Overzicht)", lambda: self.navigate("configuratiescherm")),
                    ("controlpanel.svg", "Schakel over naar klassieke weergave", self.toggle_cp_mode),
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
                "Zie ook",
                [
                    ("cp-updates.svg", "Windows Update", lambda: run_cmd("kcmshell6 kcm_updates")),
                    ("help.svg", "Help en ondersteuning", lambda: run_cmd("khelpcenter")),
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

        subhead = Gtk.Label(label="Kies een taak of een onderdeel van het Configuratiescherm", xalign=0)
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


def sni_menu(svc, path, menu_path="/com/canonical/dbusmenu"):
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
    win.set_title("Menu")
    win.set_decorated(False)
    win.set_skip_taskbar_hint(True)
    win.set_skip_pager_hint(True)
    win.set_keep_above(True)
    win.set_position(Gtk.WindowPosition.MOUSE)

    frame = Gtk.Frame()
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
    vbox.set_margin_top(3)
    vbox.set_margin_bottom(3)
    vbox.set_margin_start(3)
    vbox.set_margin_end(3)

    for it in items:
        if it.get("separator"):
            sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            vbox.pack_start(sep, False, False, 2)
        else:
            btn = Gtk.Button(label=it["label"])
            btn.get_style_context().add_class("xp-menubar-btn")
            btn.get_child().set_xalign(0.0)
            btn.set_sensitive(bool(it.get("enabled", True)))
            cid = it["id"]

            def on_item_click(_, item_id=cid):
                _sni_trigger_dbusmenu_item(bus, svc, menu_path, item_id)
                Gtk.main_quit()

            btn.connect("clicked", on_item_click)
            vbox.pack_start(btn, False, False, 0)

    frame.add(vbox)
    win.add(frame)
    win.connect("focus-out-event", lambda *_: Gtk.main_quit())
    win.connect("key-press-event", lambda _, ev: Gtk.main_quit() if ev.keyval == Gdk.KEY_Escape else False)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "computer"
    if mode == "sni-list":
        sni_list()
        return
    if mode == "sni-activate" and len(sys.argv) >= 4:
        sni_activate(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) >= 5 else "/com/canonical/dbusmenu")
        return
    if mode == "sni-menu" and len(sys.argv) >= 4:
        sni_menu(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) >= 5 else "/com/canonical/dbusmenu")
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
        win = TaskbarPropertiesDialog()
    elif mode in ("taakbeheer", "taskmgr", "taskmanager"):
        win = TaskManagerWindow()
    elif mode in ("uitvoeren", "run"):
        win = RunDialog()
    elif mode in ("configuratiescherm", "control", "instellingen"):
        win = XpExplorerWindow("configuratiescherm")
    elif mode in ("klassiek", "classic"):
        win = XpExplorerWindow("klassiek")
    else:
        win = XpExplorerWindow("computer")

    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
