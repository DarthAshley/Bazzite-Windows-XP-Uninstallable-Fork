#!/usr/bin/env python3
"""
MSN Messenger (2003/2004/2006 Retro Suite) for Windows XP on Bazzite KDE.
Authentic replica of MSN Messenger 6.0/7.0 & Windows Live Messenger:
- Authentic Startup / Login screen with 3D buddy avatar, status selector, remember me, and Luna 3D buttons
- Main Buddy List window with user profile card, custom personal messages, searchable contacts, and collapsible groups
- Full Conversation / Chat window with action toolbar (Invite, Send Files, Video, Voice, Activities, Games), buddy avatars, emoticon picker, interactive simulated chatter, and the iconic NUDGE feature with sound and screen shaking!
- MSN Toast notifications sliding up in the bottom-right corner
- Classic MSN Messenger audio chimes (online, incoming message, nudge buzz)
"""

import os
import sys
import json
import math
import time
import random
import subprocess
import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
if not os.path.isdir(SOUNDS_DIR):
    SOUNDS_DIR = os.path.expanduser("~/.local/share/xp-startknop/sounds")

CONFIG_PATH = os.path.expanduser("~/.config/xp-msn.json")

def play_sound(filename):
    """Play authentic MSN Messenger audio chime."""
    path = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(path):
        for player in ("pw-play", "paplay", "aplay", "canberra-gtk-play"):
            if subprocess.run(["which", player], capture_output=True).returncode == 0:
                try:
                    subprocess.Popen([player, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
                except Exception:
                    pass

DEFAULT_CONFIG = {
    "email": "KingGeoffrey@hotmail.com",
    "display_name": "King Geoffrey",
    "status": "Online",
    "personal_message": "listening 2 music ♫",
    "avatar": "flower",
    "remember_me": True,
    "remember_password": True,
    "auto_login": False,
    "contacts": [
        {"name": "xXstar_girlXx", "email": "xXstar_girlXx@hotmail.com", "group": "Online", "status": "Online", "pmsg": "brb", "avatar": "star"},
        {"name": "sk8rboy_07", "email": "sk8r_07@msn.com", "group": "Online", "status": "Online", "pmsg": "at school", "avatar": "skater"},
        {"name": "sweetpea_04", "email": "sweetpea_04@hotmail.com", "group": "Online", "status": "Online", "pmsg": "listening 2 music ♫", "avatar": "flower"},
        {"name": "soccorkid24", "email": "soccor24@passport.com", "group": "Online", "status": "Online", "pmsg": "practice at 5", "avatar": "soccer"},
        {"name": "xboxking", "email": "xbox_king@live.com", "group": "Online", "status": "Online", "pmsg": "call me", "avatar": "controller"},
        {"name": "pinkprincess07", "email": "princess_07@hotmail.com", "group": "Online", "status": "Online", "pmsg": "dont wanna go tomorrow", "avatar": "crown"},
        {"name": "redfan_05", "email": "redfan@msn.com", "group": "Away", "status": "Away", "pmsg": "be back later", "avatar": "car"},
        {"name": "lil_miss_angel", "email": "angel_girl@hotmail.com", "group": "Away", "status": "Away", "pmsg": "shopping :)", "avatar": "angel"},
        {"name": "crazydan98", "email": "crazydan@live.com", "group": "Busy", "status": "Busy", "pmsg": "\"Life's a game...\"", "avatar": "flames"},
        {"name": "jennifer_xo", "email": "jenny@hotmail.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "butterfly"},
        {"name": "matt732", "email": "matt@msn.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "guitar"},
        {"name": "cooldude101", "email": "dude101@hotmail.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "rocket"},
        {"name": "babygirl_03", "email": "bgirl@live.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "heart"},
        {"name": "skaterchick14", "email": "sk8rchick@hotmail.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "skater"}
    ]
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                c = json.load(f)
                return {**DEFAULT_CONFIG, **c}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

MSN_CSS = """
/* Authentic Windows XP Luna Window & Fonts */
* {
    font-family: 'Tahoma', 'Segoe UI', sans-serif;
}

window {
    background-color: #ece9d8;
    color: #000000;
}

.xp-msn-menubar {
    background-color: #ece9d8;
    border-bottom: 1px solid #d8d2bd;
    padding: 1px 2px;
}

.xp-msn-menubar-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 0px;
    padding: 3px 6px;
    font-size: 11px;
    color: #000000;
    box-shadow: none;
}
.xp-msn-menubar-btn:hover {
    background-color: #316ac5;
    color: #ffffff;
}

.xp-msn-body {
    background: linear-gradient(to bottom, #ffffff 0%, #eef3fb 45%, #dce7f7 100%);
    border: 1px solid #7f9db9;
}

.xp-login-card {
    background: #ffffff;
    border: 1px solid #7f9db9;
    border-radius: 6px;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.15);
}

.xp-btn-signin {
    background-image: linear-gradient(to bottom, #ffffff 0%, #ece9d8 50%, #d8d2bd 100%);
    border: 1px solid #003c74;
    border-radius: 3px;
    color: #000000;
    font-weight: bold;
    font-size: 12px;
    padding: 5px 24px;
    box-shadow: inset 1px 1px 0px #ffffff, 1px 1px 2px rgba(0,0,0,0.2);
}
.xp-btn-signin:hover {
    background-image: linear-gradient(to bottom, #fff5cc 0%, #ffe085 50%, #ffc947 100%);
    border-color: #e5a000;
}
.xp-btn-signin:active {
    background-image: linear-gradient(to bottom, #d8d2bd 0%, #ece9d8 100%);
    box-shadow: inset 1px 1px 2px rgba(0,0,0,0.3);
}

.xp-btn-luna {
    background-image: linear-gradient(to bottom, #ffffff 0%, #ece9d8 50%, #d8d2bd 100%);
    border: 1px solid #7f9db9;
    border-radius: 3px;
    color: #000000;
    font-size: 11px;
    padding: 3px 12px;
    box-shadow: inset 1px 1px 0px #ffffff;
}
.xp-btn-luna:hover {
    background-image: linear-gradient(to bottom, #fff5cc 0%, #ffe085 50%, #ffc947 100%);
    border-color: #e5a000;
}

.xp-entry {
    background-color: #ffffff;
    border: 1px solid #7f9db9;
    border-radius: 0px;
    padding: 3px 6px;
    font-size: 11px;
    color: #000000;
}
.xp-entry:focus {
    border-color: #316ac5;
}

.xp-link {
    color: #0a246a;
    font-size: 11px;
    text-decoration: underline;
    background: transparent;
    border: none;
    padding: 2px 0px;
}
.xp-link:hover {
    color: #316ac5;
}

.xp-group-header {
    background: linear-gradient(to right, #e2ecf7 0%, #f4f8fd 100%);
    border-bottom: 1px solid #c2d5eb;
    font-weight: bold;
    font-size: 11px;
    color: #0a246a;
    padding: 3px 6px;
}

.xp-contact-row {
    background: transparent;
    border: 1px solid transparent;
    padding: 3px 6px;
}
.xp-contact-row:hover {
    background-color: #e5eef9;
    border-color: #b5d1f2;
}
.xp-contact-row:selected {
    background-color: #316ac5;
    color: #ffffff;
}

.xp-chat-toolbar {
    background: linear-gradient(to bottom, #f7f9fd 0%, #e5eef9 100%);
    border-top: 1px solid #ffffff;
    border-bottom: 1px solid #b5d1f2;
    padding: 3px 6px;
}

.xp-chat-toolbtn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 2px;
    padding: 3px 8px;
    font-size: 11px;
    color: #000000;
    box-shadow: none;
}
.xp-chat-toolbtn:hover {
    background: linear-gradient(to bottom, #fff9e6, #ffdf88);
    border-color: #e5a000;
}

.xp-chat-log {
    background-color: #ffffff;
    border: 1px solid #7f9db9;
    padding: 8px;
    font-size: 11px;
}

.xp-chat-input {
    background-color: #ffffff;
    border: 1px solid #7f9db9;
    padding: 4px;
    font-size: 11px;
}

.xp-toast-box {
    background: linear-gradient(to bottom, #f2f7fd 0%, #d8e6f8 100%);
    border: 1px solid #316ac5;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.35);
    padding: 8px 12px;
}
"""

def draw_msn_butterfly(cr, x, y, size=24):
    """Draw authentic 4-color MSN butterfly wings with gradient."""
    cr.save()
    cr.translate(x, y)
    s = size / 24.0
    cr.scale(s, s)

    # 1. Top left wing: Green
    cr.set_source_rgb(0.32, 0.72, 0.15)
    cr.move_to(11, 11)
    cr.curve_to(7, 3, 2, 4, 3, 10)
    cr.curve_to(4, 13, 8, 14, 11, 11)
    cr.fill()

    # 2. Top right wing: Blue
    cr.set_source_rgb(0.08, 0.48, 0.88)
    cr.move_to(13, 11)
    cr.curve_to(17, 2, 22, 5, 20, 11)
    cr.curve_to(19, 14, 15, 14, 13, 11)
    cr.fill()

    # 3. Bottom left wing: Orange
    cr.set_source_rgb(0.95, 0.55, 0.05)
    cr.move_to(11, 13)
    cr.curve_to(5, 15, 4, 20, 9, 21)
    cr.curve_to(12, 21, 12, 17, 11, 13)
    cr.fill()

    # 4. Bottom right wing: Red/Magenta
    cr.set_source_rgb(0.92, 0.16, 0.28)
    cr.move_to(13, 13)
    cr.curve_to(17, 16, 20, 18, 17, 21)
    cr.curve_to(14, 22, 12, 18, 13, 13)
    cr.fill()

    # Body
    cr.set_source_rgb(0.15, 0.35, 0.65)
    cr.move_to(12, 8); cr.line_to(12, 18)
    cr.set_line_width(1.8)
    cr.stroke()

    cr.restore()

def draw_3d_buddy_avatar(cr, cx, cy, radius=32):
    """Draw the authentic 3D MSN green buddy avatar with shoulder wings."""
    cr.save()
    # Buddy Head
    head_grad = cairo_create_radial_gradient(cr, cx - radius * 0.3, cy - radius * 0.4, 2, cx, cy - radius * 0.3, radius * 0.5)
    head_grad.add_color_stop_rgb(0.0, 0.65, 0.95, 0.65)
    head_grad.add_color_stop_rgb(0.4, 0.22, 0.72, 0.52)
    head_grad.add_color_stop_rgb(1.0, 0.05, 0.35, 0.32)
    cr.set_source(head_grad)
    cr.arc(cx, cy - radius * 0.25, radius * 0.42, 0, 2 * math.pi)
    cr.fill()

    # Buddy Body
    body_grad = cairo_create_radial_gradient(cr, cx - radius * 0.3, cy + radius * 0.3, 4, cx, cy + radius * 0.5, radius * 0.75)
    body_grad.add_color_stop_rgb(0.0, 0.62, 0.92, 0.62)
    body_grad.add_color_stop_rgb(0.5, 0.18, 0.65, 0.48)
    body_grad.add_color_stop_rgb(1.0, 0.04, 0.28, 0.25)
    cr.set_source(body_grad)
    cr.move_to(cx - radius * 0.65, cy + radius * 0.75)
    cr.curve_to(cx - radius * 0.6, cy + radius * 0.2, cx + radius * 0.6, cy + radius * 0.2, cx + radius * 0.65, cy + radius * 0.75)
    cr.close_path()
    cr.fill()

    # Butterfly wing on shoulder
    draw_msn_butterfly(cr, cx + radius * 0.12, cy - radius * 0.1, size=radius * 0.85)

    cr.restore()

def cairo_create_radial_gradient(cr, cx0, cy0, r0, cx1, cy1, r1):
    import cairo
    return cairo.RadialGradient(cx0, cy0, r0, cx1, cy1, r1)


class XpMsnLoginWindow(Gtk.Window):
    """Authentic MSN Messenger 6.0/7.0 Login Window."""

    def __init__(self, on_login_success=None):
        super().__init__(title="MSN Messenger")
        self.set_default_size(320, 540)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.on_login_success = on_login_success
        self.cfg = load_config()

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # 1. Menubar
        mbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        mbar.get_style_context().add_class("xp-msn-menubar")
        for m in ("File", "Contacts", "Actions", "Tools", "Help"):
            b = Gtk.Button(label=m)
            b.get_style_context().add_class("xp-msn-menubar-btn")
            if m == "Help":
                b.connect("clicked", lambda *_: subprocess.Popen(["xdg-open", "https://escargot.chat"]))
            elif m == "File":
                b.connect("clicked", lambda *_: Gtk.main_quit())
            mbar.pack_start(b, False, False, 0)
        main_box.pack_start(mbar, False, False, 0)

        # 2. Main Body with Watermark & Gradient
        body_da = Gtk.DrawingArea()
        body_da.set_size_request(320, 480)

        overlay = Gtk.Overlay()
        overlay.add(body_da)

        # Content Box over body
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content.set_margin_start(24)
        content.set_margin_end(24)
        content.set_margin_top(12)
        content.set_margin_bottom(12)

        # Header: back arrow + msn. Messenger
        hdr_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hdr_da = Gtk.DrawingArea()
        hdr_da.set_size_request(180, 28)
        def draw_hdr(w, cr):
            # Back circle icon
            cr.set_source_rgb(0.75, 0.85, 0.95)
            cr.arc(12, 14, 10, 0, 6.28)
            cr.fill()
            cr.set_source_rgb(0.3, 0.5, 0.7)
            cr.set_line_width(1.2)
            cr.arc(12, 14, 10, 0, 6.28)
            cr.stroke()
            # Arrow
            cr.set_source_rgb(0.1, 0.3, 0.6)
            cr.move_to(15, 10); cr.line_to(9, 14); cr.line_to(15, 18)
            cr.set_line_width(1.6); cr.stroke()

            # msn. text
            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(15)
            cr.set_source_rgb(0.0, 0.22, 0.55)
            cr.move_to(28, 19)
            cr.show_text("msn")

            draw_msn_butterfly(cr, 62, 5, 18)

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(14)
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.move_to(88, 19)
            cr.show_text("Messenger")
            return False

        hdr_da.connect("draw", draw_hdr)
        hdr_row.pack_start(hdr_da, False, False, 0)
        content.pack_start(hdr_row, False, False, 0)

        # Avatar card with 3D buddy
        card_da = Gtk.DrawingArea()
        card_da.set_size_request(100, 100)
        card_da.set_halign(Gtk.Align.CENTER)
        def draw_card(w, cr):
            bw, bh = 96, 96
            bx, by = 2, 2
            # Rounded rect card background with border
            cr.set_source_rgb(1, 1, 1)
            cr.new_sub_path()
            cr.arc(bx + 8, by + 8, 6, 3.14, 4.71)
            cr.arc(bx + bw - 8, by + 8, 6, 4.71, 6.28)
            cr.arc(bx + bw - 8, by + bh - 8, 6, 0, 1.57)
            cr.arc(bx + 8, by + bh - 8, 6, 1.57, 3.14)
            cr.close_path()
            cr.fill_preserve()
            cr.set_source_rgb(0.6, 0.72, 0.88)
            cr.set_line_width(1.5)
            cr.stroke()

            # 3D buddy inside
            draw_3d_buddy_avatar(cr, bx + bw / 2, by + bh / 2, radius=34)
            return False

        card_da.connect("draw", draw_card)
        content.pack_start(card_da, False, False, 4)

        # Form fields
        lbl_email = Gtk.Label(label="E-mail address:", xalign=0.0)
        lbl_email.get_style_context().add_class("xp-link")
        content.pack_start(lbl_email, False, False, 0)

        self.cb_email = Gtk.ComboBoxText.new_with_entry()
        self.cb_email.append_text(self.cfg.get("email", "KingGeoffrey@hotmail.com"))
        self.cb_email.append_text("sweetpea_04@hotmail.com")
        self.cb_email.append_text("person@passport.com")
        self.cb_email.set_active(0)
        self.cb_email.get_child().get_style_context().add_class("xp-entry")
        content.pack_start(self.cb_email, False, False, 0)

        lbl_pwd = Gtk.Label(label="Password:", xalign=0.0)
        lbl_pwd.get_style_context().add_class("xp-link")
        content.pack_start(lbl_pwd, False, False, 0)

        self.ent_pwd = Gtk.Entry()
        self.ent_pwd.set_visibility(False)
        self.ent_pwd.set_text("••••••••••••")
        self.ent_pwd.get_style_context().add_class("xp-entry")
        content.pack_start(self.ent_pwd, False, False, 0)

        # Status row
        status_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        status_lbl = Gtk.Label(label="Status:", xalign=0.0)
        status_row.pack_start(status_lbl, False, False, 0)

        self.cb_status = Gtk.ComboBoxText()
        for s in ("Online", "Busy", "Be Right Back", "Away", "On The Phone", "Out To Lunch", "Appear Offline"):
            self.cb_status.append_text(s)
        self.cb_status.set_active(0)
        status_row.pack_start(self.cb_status, True, True, 0)
        content.pack_start(status_row, False, False, 0)

        # Checkboxes
        self.chk_rem = Gtk.CheckButton(label="Remember Me  (Forget Me)")
        self.chk_rem.set_active(self.cfg.get("remember_me", True))
        content.pack_start(self.chk_rem, False, False, 0)

        self.chk_pwd = Gtk.CheckButton(label="Remember my Password")
        self.chk_pwd.set_active(self.cfg.get("remember_password", True))
        content.pack_start(self.chk_pwd, False, False, 0)

        self.chk_auto = Gtk.CheckButton(label="Sign me in automatically")
        self.chk_auto.set_active(self.cfg.get("auto_login", False))
        content.pack_start(self.chk_auto, False, False, 0)

        # Sign In Button
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_box.set_halign(Gtk.Align.CENTER)
        self.btn_signin = Gtk.Button(label="Sign In")
        self.btn_signin.get_style_context().add_class("xp-btn-signin")
        self.btn_signin.connect("clicked", self.on_sign_in_clicked)
        btn_box.pack_start(self.btn_signin, False, False, 0)
        content.pack_start(btn_box, False, False, 6)

        # Links
        links_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        links_box.set_margin_top(4)
        for l_txt, url in [
            ("Forgot your password?", "https://account.live.com"),
            ("Service Status", "https://status.live.com"),
            ("Get a new account", "https://signup.live.com")
        ]:
            b_l = Gtk.Button(label=l_txt)
            b_l.get_style_context().add_class("xp-link")
            b_l.get_child().set_xalign(0.0)
            b_l.connect("clicked", lambda _, u=url: subprocess.Popen(["xdg-open", u]))
            links_box.pack_start(b_l, False, False, 0)
        content.pack_start(links_box, False, False, 0)

        # Footer: Microsoft Passport Network
        ftr_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ftr_row.set_margin_top(12)
        ftr_da = Gtk.DrawingArea()
        ftr_da.set_size_request(220, 24)
        def draw_ftr(w, cr):
            # Passport arrow
            cr.set_source_rgb(0.2, 0.45, 0.8)
            cr.rectangle(2, 4, 14, 14); cr.fill()
            cr.set_source_rgb(1, 1, 1)
            cr.move_to(5, 11); cr.line_to(11, 11); cr.line_to(9, 8)
            cr.move_to(11, 11); cr.line_to(9, 14); cr.stroke()

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(10)
            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.move_to(22, 15)
            cr.show_text("Microsoft Passport Network")
            return False
        ftr_da.connect("draw", draw_ftr)
        ftr_row.pack_start(ftr_da, False, False, 0)
        content.pack_start(ftr_row, False, False, 0)

        overlay.add_overlay(content)
        main_box.pack_start(overlay, True, True, 0)

        def draw_bg(widget, cr):
            import cairo
            w = widget.get_allocated_width()
            h = widget.get_allocated_height()
            pat = cairo.LinearGradient(0, 0, 0, h)
            pat.add_color_stop_rgb(0.0, 1.0, 1.0, 1.0)
            pat.add_color_stop_rgb(0.4, 0.93, 0.96, 0.99)
            pat.add_color_stop_rgb(1.0, 0.84, 0.90, 0.97)
            cr.set_source(pat)
            cr.rectangle(0, 0, w, h)
            cr.fill()

            # Watermark MSN buddies in lower right
            cr.save()
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.45)
            draw_3d_buddy_avatar(cr, w - 45, h - 55, radius=38)
            draw_3d_buddy_avatar(cr, w - 85, h - 35, radius=24)
            cr.restore()
            return False

        body_da.connect("draw", draw_bg)
        self.connect("destroy", Gtk.main_quit)

    def on_sign_in_clicked(self, btn):
        play_sound("online.wav")
        self.btn_signin.set_label("Signing In...")
        self.btn_signin.set_sensitive(False)

        # Update saved email
        email = self.cb_email.get_child().get_text().strip()
        status = self.cb_status.get_active_text() or "Online"
        self.cfg["email"] = email
        self.cfg["status"] = status
        self.cfg["remember_me"] = self.chk_rem.get_active()
        self.cfg["remember_password"] = self.chk_pwd.get_active()
        self.cfg["auto_login"] = self.chk_auto.get_active()
        save_config(self.cfg)

        def open_main():
            self.destroy()
            if self.on_login_success:
                self.on_login_success(self.cfg)
            else:
                w = XpMsnContactListWindow(self.cfg)
                w.show_all()
            return False

        GLib.timeout_add(650, open_main)


class XpMsnContactListWindow(Gtk.Window):
    """Authentic MSN Messenger / Windows Live Messenger Buddy List."""

    def __init__(self, cfg=None):
        super().__init__(title="MSN Messenger")
        self.set_default_size(300, 650)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.cfg = cfg or load_config()
        self.chat_windows = {}

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        # 1. Menubar
        mbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        mbar.get_style_context().add_class("xp-msn-menubar")
        for m in ("File", "Contacts", "Actions", "Tools", "Help"):
            b = Gtk.Button(label=m)
            b.get_style_context().add_class("xp-msn-menubar-btn")
            if m == "File":
                b.connect("clicked", lambda *_: Gtk.main_quit())
            elif m == "Help":
                b.connect("clicked", lambda *_: subprocess.Popen(["xdg-open", "https://escargot.chat"]))
            mbar.pack_start(b, False, False, 0)
        vbox.pack_start(mbar, False, False, 0)

        # 2. User Profile Card
        card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        card.set_margin_start(8); card.set_margin_end(8)
        card.set_margin_top(8); card.set_margin_bottom(6)

        # Avatar DA
        self.avatar_da = Gtk.DrawingArea()
        self.avatar_da.set_size_request(56, 56)
        def draw_usr_avatar(w, cr):
            cr.set_source_rgb(0.9, 0.94, 0.98)
            cr.rectangle(0, 0, 56, 56); cr.fill()
            cr.set_source_rgb(0.5, 0.7, 0.9)
            cr.set_line_width(1.5); cr.rectangle(0, 0, 56, 56); cr.stroke()
            draw_3d_buddy_avatar(cr, 28, 28, radius=20)
            return False
        self.avatar_da.connect("draw", draw_usr_avatar)
        card.pack_start(self.avatar_da, False, False, 0)

        # User details column
        ucol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.lbl_name = Gtk.Label(label=f"<b>{self.cfg.get('display_name', 'King Geoffrey')}</b> (Online)", use_markup=True, xalign=0.0)
        name_row.pack_start(self.lbl_name, False, False, 0)
        ucol.pack_start(name_row, False, False, 0)

        # Personal message (clickable)
        self.ent_pmsg = Gtk.Entry()
        self.ent_pmsg.set_text(self.cfg.get("personal_message", "listening 2 music ♫"))
        self.ent_pmsg.get_style_context().add_class("xp-entry")
        self.ent_pmsg.connect("changed", self.on_pmsg_changed)
        ucol.pack_start(self.ent_pmsg, False, False, 0)

        card.pack_start(ucol, True, True, 0)
        vbox.pack_start(card, False, False, 0)

        # 3. Subtoolbar (Mail, Call, Search)
        stoolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        stoolbar.set_margin_start(10); stoolbar.set_margin_end(10); stoolbar.set_margin_bottom(4)
        for icon_lbl, tip, act in [
            ("✉ (0)", "Go to Hotmail Inbox", lambda: subprocess.Popen(["xdg-open", "https://mail.live.com"])),
            ("📞 Call", "Make a phone or voice call", lambda: play_sound("klick.wav")),
            ("🔍 Search", "Search the web", lambda: subprocess.Popen(["xdg-open", "https://www.google.com"]))
        ]:
            s_btn = Gtk.Button(label=icon_lbl)
            s_btn.set_tooltip_text(tip)
            s_btn.get_style_context().add_class("xp-msn-menubar-btn")
            s_btn.connect("clicked", lambda _, a=act: a())
            stoolbar.pack_start(s_btn, False, False, 0)
        vbox.pack_start(stoolbar, False, False, 0)

        # 4. Search contacts bar
        sbar_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        sbar_row.set_margin_start(8); sbar_row.set_margin_end(8); sbar_row.set_margin_bottom(4)
        self.search_ent = Gtk.SearchEntry()
        self.search_ent.set_placeholder_text("Find a contact or number...")
        self.search_ent.get_style_context().add_class("xp-entry")
        self.search_ent.connect("search-changed", self.on_search_changed)
        sbar_row.pack_start(self.search_ent, True, True, 0)
        vbox.pack_start(sbar_row, False, False, 0)

        # 5. Buddy List Scrolled Window
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.contacts_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.contacts_vbox.set_margin_start(2); self.contacts_vbox.set_margin_end(2)
        scroller.add(self.contacts_vbox)
        vbox.pack_start(scroller, True, True, 0)

        self.rebuild_contact_list()

        # 6. Action row: Add Contact / Send Instant Message
        act_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        act_row.set_margin_start(10); act_row.set_margin_end(10)
        act_row.set_margin_top(4); act_row.set_margin_bottom(4)

        btn_add = Gtk.Button(label="+ Add a Contact")
        btn_add.get_style_context().add_class("xp-link")
        btn_add.connect("clicked", self.on_add_contact_dialog)
        act_row.pack_start(btn_add, False, False, 0)

        btn_im = Gtk.Button(label="✉ Send Message")
        btn_im.get_style_context().add_class("xp-link")
        btn_im.connect("clicked", lambda *_: self.open_chat(self.cfg["contacts"][0]))
        act_row.pack_end(btn_im, False, False, 0)
        vbox.pack_start(act_row, False, False, 0)

        # 7. Bottom MSN .NET Ad Banner
        banner_da = Gtk.DrawingArea()
        banner_da.set_size_request(300, 48)
        def draw_banner(w, cr):
            import cairo
            bw = w.get_allocated_width()
            bh = w.get_allocated_height()
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(0, 0, bw, bh); cr.fill()
            cr.set_source_rgb(0.8, 0.85, 0.92)
            cr.set_line_width(1.0); cr.rectangle(0, 0, bw, bh); cr.stroke()

            # Watermark buddies on left
            cr.set_source_rgba(0.2, 0.45, 0.8, 0.25)
            draw_3d_buddy_avatar(cr, 24, 24, radius=16)

            # msn text & butterfly
            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(16)
            cr.set_source_rgb(0.0, 0.22, 0.55)
            cr.move_to(54, 30); cr.show_text("msn")

            draw_msn_butterfly(cr, 88, 14, 20)

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(15)
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.move_to(116, 30); cr.show_text("Messenger")

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(11)
            cr.set_source_rgb(0.35, 0.35, 0.35)
            cr.move_to(200, 34); cr.show_text(".net")
            return False

        banner_da.connect("draw", draw_banner)
        vbox.pack_start(banner_da, False, False, 0)

        self.connect("destroy", Gtk.main_quit)

        # Trigger simulated incoming toast after 2 seconds
        GLib.timeout_add(2200, self.trigger_welcome_toast)

    def on_pmsg_changed(self, ent):
        self.cfg["personal_message"] = ent.get_text()
        save_config(self.cfg)

    def trigger_welcome_toast(self):
        c = self.cfg["contacts"][0]
        toast = XpMsnToast(c["name"], "has just signed in.")
        toast.show_all()
        play_sound("online.wav")
        return False

    def on_search_changed(self, ent):
        self.rebuild_contact_list(filter_txt=ent.get_text().strip().lower())

    def rebuild_contact_list(self, filter_txt=""):
        for child in self.contacts_vbox.get_children():
            self.contacts_vbox.remove(child)

        contacts = self.cfg.get("contacts", [])
        groups = {}
        for c in contacts:
            g = c.get("group", "Offline")
            groups.setdefault(g, []).append(c)

        for gname in ("Online", "Away", "Busy", "Offline"):
            clist = groups.get(gname, [])
            if filter_txt:
                clist = [c for c in clist if filter_txt in c["name"].lower() or filter_txt in c.get("pmsg", "").lower()]

            # Group header
            hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            hdr.get_style_context().add_class("xp-group-header")
            hlbl = Gtk.Label(label=f"▾ {gname} ({len(clist)})", xalign=0.0)
            hdr.pack_start(hlbl, True, True, 2)
            self.contacts_vbox.pack_start(hdr, False, False, 0)

            for c in clist:
                row = Gtk.EventBox()
                row.get_style_context().add_class("xp-contact-row")
                rbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                rbox.set_margin_start(12); rbox.set_margin_end(6)
                rbox.set_margin_top(2); rbox.set_margin_bottom(2)

                # Status icon DA
                icon_da = Gtk.DrawingArea()
                icon_da.set_size_request(16, 16)
                st = c.get("status", "Online")
                def draw_st(w, cr, status=st):
                    if status == "Online":
                        # Green Buddy
                        cr.set_source_rgb(0.2, 0.75, 0.2)
                        cr.arc(8, 5, 3.5, 0, 6.28); cr.fill()
                        cr.arc(8, 13, 5, 3.14, 6.28); cr.fill()
                    elif status == "Away":
                        # Orange clock
                        cr.set_source_rgb(0.95, 0.6, 0.1)
                        cr.arc(8, 8, 6, 0, 6.28); cr.fill()
                        cr.set_source_rgb(1, 1, 1)
                        cr.move_to(8, 4); cr.line_to(8, 8); cr.line_to(11, 8)
                        cr.set_line_width(1.4); cr.stroke()
                    elif status == "Busy":
                        # Red minus
                        cr.set_source_rgb(0.9, 0.2, 0.2)
                        cr.arc(8, 8, 6, 0, 6.28); cr.fill()
                        cr.set_source_rgb(1, 1, 1)
                        cr.move_to(4, 8); cr.line_to(12, 8)
                        cr.set_line_width(2.0); cr.stroke()
                    else:
                        # Gray offline
                        cr.set_source_rgb(0.65, 0.65, 0.65)
                        cr.arc(8, 5, 3.5, 0, 6.28); cr.stroke()
                        cr.arc(8, 13, 5, 3.14, 6.28); cr.stroke()
                    return False
                icon_da.connect("draw", draw_st)
                rbox.pack_start(icon_da, False, False, 0)

                # Name & Personal message
                txt_col = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
                lbl_cname = Gtk.Label(label=c["name"], xalign=0.0)
                txt_col.pack_start(lbl_cname, False, False, 0)
                if c.get("pmsg"):
                    lbl_cpmsg = Gtk.Label(label=f"- <span color='#666666'>{c['pmsg']}</span>", use_markup=True, xalign=0.0)
                    txt_col.pack_start(lbl_cpmsg, False, False, 0)
                rbox.pack_start(txt_col, True, True, 0)

                row.add(rbox)
                row.connect("button-press-event", lambda _, ev, target=c: self.open_chat(target) if ev.type == Gdk.EventType._2BUTTON_PRESS else False)
                self.contacts_vbox.pack_start(row, False, False, 0)

        self.contacts_vbox.show_all()

    def open_chat(self, contact):
        cname = contact["name"]
        if cname in self.chat_windows:
            self.chat_windows[cname].present()
        else:
            chat = XpMsnChatWindow(contact, self.cfg)
            self.chat_windows[cname] = chat
            chat.connect("destroy", lambda *_: self.chat_windows.pop(cname, None))
            chat.show_all()

    def on_add_contact_dialog(self, _):
        dlg = Gtk.Dialog(title="Add a Contact", parent=self, flags=0)
        dlg.set_default_size(300, 140)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Add", Gtk.ResponseType.OK)

        box = dlg.get_content_area()
        box.set_margin_start(16); box.set_margin_end(16); box.set_margin_top(12)
        lbl = Gtk.Label(label="Please type your contact's Windows Live or Hotmail address:", xalign=0.0)
        box.pack_start(lbl, False, False, 4)
        ent = Gtk.Entry()
        ent.set_placeholder_text("friend@hotmail.com")
        ent.get_style_context().add_class("xp-entry")
        box.pack_start(ent, False, False, 4)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.OK:
            val = ent.get_text().strip()
            if val:
                cname = val.split("@")[0]
                self.cfg.setdefault("contacts", []).insert(0, {
                    "name": cname, "email": val, "group": "Online", "status": "Online", "pmsg": "Hey there!", "avatar": "star"
                })
                save_config(self.cfg)
                self.rebuild_contact_list()
        dlg.destroy()


class XpMsnChatWindow(Gtk.Window):
    """Authentic MSN Messenger 2003/2004 Conversation Window."""

    def __init__(self, contact, user_cfg):
        cname = contact["name"]
        super().__init__(title=f"{cname} - Conversation")
        self.set_default_size(540, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.contact = contact
        self.user_cfg = user_cfg
        self.my_name = user_cfg.get("display_name", "King Geoffrey")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        # 1. Menubar
        mbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        mbar.get_style_context().add_class("xp-msn-menubar")
        for m in ("File", "Edit", "Actions", "Tools", "Help"):
            b = Gtk.Button(label=m)
            b.get_style_context().add_class("xp-msn-menubar-btn")
            if m == "File":
                b.connect("clicked", lambda *_: self.destroy())
            mbar.pack_start(b, False, False, 0)
        vbox.pack_start(mbar, False, False, 0)

        # 2. Action Toolbar (Invite, Send Files, Video, Voice, Activities, Games, Block)
        act_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        act_bar.get_style_context().add_class("xp-chat-toolbar")
        for label, tip in [
            ("👥 Invite", "Invite someone to this conversation"),
            ("📁 Send Files", "Send a file or photo"),
            ("📹 Video", "Start video call"),
            ("🎤 Voice", "Start audio conversation"),
            ("🎯 Activities", "Start MSN activity"),
            ("🎮 Games", "Play Tic-Tac-Toe, Minesweeper or Checkers"),
            ("🚫 Block", "Block this contact")
        ]:
            tb = Gtk.Button(label=label)
            tb.set_tooltip_text(tip)
            tb.get_style_context().add_class("xp-chat-toolbtn")
            tb.connect("clicked", lambda _, t=tip: play_sound("klick.wav"))
            act_bar.pack_start(tb, False, False, 0)
        vbox.pack_start(act_bar, False, False, 0)

        # 3. Info & Security Banner
        info_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_row.set_margin_start(10); info_row.set_margin_end(10); info_row.set_margin_top(6); info_row.set_margin_bottom(4)
        to_lbl = Gtk.Label(label=f"<b>To: {cname} &lt;{contact.get('email', '')}&gt;</b>", use_markup=True, xalign=0.0)
        sec_lbl = Gtk.Label(label="<span color='#666666'>ℹ Never give out your password or credit card number in an instant message conversation.</span>", use_markup=True, xalign=0.0)
        info_row.pack_start(to_lbl, False, False, 0)
        info_row.pack_start(sec_lbl, False, False, 0)
        vbox.pack_start(info_row, False, False, 0)

        # 4. Middle Section: Chat history on left, Buddy avatars on right
        mid_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        mid_row.set_margin_start(8); mid_row.set_margin_end(8)

        # Chat history view
        chat_scroll = Gtk.ScrolledWindow()
        chat_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.chat_view = Gtk.TextView()
        self.chat_view.set_editable(False)
        self.chat_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.chat_view.get_style_context().add_class("xp-chat-log")
        self.chat_buf = self.chat_view.get_buffer()

        # Define text tags for authentic MSN chat rendering
        self.tag_contact = self.chat_buf.create_tag("contact_nick", foreground="#001961", weight=Pango.Weight.BOLD)
        self.tag_user = self.chat_buf.create_tag("user_nick", foreground="#b04000", weight=Pango.Weight.BOLD)
        self.tag_nudge = self.chat_buf.create_tag("nudge", foreground="#990000", weight=Pango.Weight.BOLD)
        self.tag_system = self.chat_buf.create_tag("system", foreground="#808080", style=Pango.Style.ITALIC)

        chat_scroll.add(self.chat_view)
        mid_row.pack_start(chat_scroll, True, True, 0)

        # Right avatars panel (Buddy on top, User on bottom)
        side_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        side_panel.set_size_request(86, -1)

        # Buddy Avatar DA
        buddy_da = Gtk.DrawingArea()
        buddy_da.set_size_request(80, 80)
        def draw_b_avatar(w, cr):
            cr.set_source_rgb(0.92, 0.95, 0.99)
            cr.rectangle(0, 0, 80, 80); cr.fill()
            cr.set_source_rgb(0.5, 0.7, 0.9)
            cr.set_line_width(1.5); cr.rectangle(0, 0, 80, 80); cr.stroke()
            draw_3d_buddy_avatar(cr, 40, 40, radius=28)
            return False
        buddy_da.connect("draw", draw_b_avatar)
        side_panel.pack_start(buddy_da, False, False, 0)

        # Spacer
        side_panel.pack_start(Gtk.Box(), True, True, 0)

        # User Avatar DA
        usr_da = Gtk.DrawingArea()
        usr_da.set_size_request(80, 80)
        def draw_u_avatar(w, cr):
            cr.set_source_rgb(0.98, 0.95, 0.92)
            cr.rectangle(0, 0, 80, 80); cr.fill()
            cr.set_source_rgb(0.9, 0.6, 0.4)
            cr.set_line_width(1.5); cr.rectangle(0, 0, 80, 80); cr.stroke()
            # Draw cute dog avatar / smiley
            cr.set_source_rgb(0.85, 0.65, 0.45)
            cr.arc(40, 40, 26, 0, 6.28); cr.fill()
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.arc(32, 36, 3, 0, 6.28); cr.fill()
            cr.arc(48, 36, 3, 0, 6.28); cr.fill()
            cr.arc(40, 44, 4.5, 0, 6.28); cr.fill()
            return False
        usr_da.connect("draw", draw_u_avatar)
        side_panel.pack_end(usr_da, False, False, 0)

        mid_row.pack_start(side_panel, False, False, 0)
        vbox.pack_start(mid_row, True, True, 4)

        # 5. Formatting Toolbar (Font, Emoticons, Voice Clip, NUDGE!)
        fmt_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        fmt_bar.get_style_context().add_class("xp-chat-toolbar")
        fmt_bar.set_margin_start(8); fmt_bar.set_margin_end(8)

        btn_font = Gtk.Button(label="A")
        btn_font.get_style_context().add_class("xp-chat-toolbtn")
        fmt_bar.pack_start(btn_font, False, False, 0)

        btn_emo = Gtk.Button(label="😊 ▾")
        btn_emo.get_style_context().add_class("xp-chat-toolbtn")
        btn_emo.connect("clicked", self.on_emoticon_picker)
        fmt_bar.pack_start(btn_emo, False, False, 0)

        btn_voice = Gtk.Button(label="🎤 Voice Clip")
        btn_voice.get_style_context().add_class("xp-chat-toolbtn")
        fmt_bar.pack_start(btn_voice, False, False, 0)

        # THE LEGENDARY MSN NUDGE BUTTON!
        btn_nudge = Gtk.Button(label="⚡ Nudge!")
        btn_nudge.set_tooltip_text("Send a nudge to shake the conversation window!")
        btn_nudge.get_style_context().add_class("xp-chat-toolbtn")
        btn_nudge.connect("clicked", self.on_nudge_clicked)
        fmt_bar.pack_start(btn_nudge, False, False, 0)

        vbox.pack_start(fmt_bar, False, False, 0)

        # 6. Text input & Send button row
        bot_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        bot_row.set_margin_start(8); bot_row.set_margin_end(8)
        bot_row.set_margin_top(4); bot_row.set_margin_bottom(6)

        inp_scroll = Gtk.ScrolledWindow()
        inp_scroll.set_size_request(-1, 60)
        inp_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.inp_view = Gtk.TextView()
        self.inp_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.inp_view.get_style_context().add_class("xp-chat-input")
        self.inp_buf = self.inp_view.get_buffer()
        self.inp_view.connect("key-press-event", self.on_input_key)
        inp_scroll.add(self.inp_view)
        bot_row.pack_start(inp_scroll, True, True, 0)

        btn_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        btn_send = Gtk.Button(label="Send")
        btn_send.get_style_context().add_class("xp-btn-signin")
        btn_send.connect("clicked", lambda *_: self.send_message())
        btn_col.pack_start(btn_send, True, True, 0)

        btn_search = Gtk.Button(label="Search")
        btn_search.get_style_context().add_class("xp-btn-luna")
        btn_col.pack_start(btn_search, False, False, 0)
        bot_row.pack_start(btn_col, False, False, 0)

        vbox.pack_start(bot_row, False, False, 0)

        # 7. Status bar
        now_str = time.strftime("%I:%M %p")
        self.lbl_status = Gtk.Label(label=f"Last message received at {now_str}.", xalign=0.0)
        self.lbl_status.set_margin_start(10); self.lbl_status.set_margin_bottom(4)
        self.lbl_status.get_style_context().add_class("xp-system")
        vbox.pack_start(self.lbl_status, False, False, 0)

        # Initial nostalgic message from contact
        self.append_message(cname, "yo u on?", is_user=False)

    def append_message(self, author, text, is_user=False):
        t_str = time.strftime("%I:%M %p")
        end_iter = self.chat_buf.get_end_iter()
        tag = self.tag_user if is_user else self.tag_contact
        self.chat_buf.insert_with_tags(end_iter, f"{author} says ({t_str}):\n", tag)
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert(end_iter, f"  {text}\n\n")

        # Auto scroll to bottom
        mark = self.chat_buf.create_mark(None, self.chat_buf.get_end_iter(), False)
        self.chat_view.scroll_to_mark(mark, 0.05, False, 0.0, 0.0)

    def on_input_key(self, w, ev):
        if ev.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter) and not (ev.state & Gdk.ModifierType.SHIFT_MASK):
            self.send_message()
            return True
        return False

    def send_message(self):
        start = self.inp_buf.get_start_iter()
        end = self.inp_buf.get_end_iter()
        txt = self.inp_buf.get_text(start, end, False).strip()
        if not txt:
            return
        self.inp_buf.set_text("")
        self.append_message(self.my_name, txt, is_user=True)
        play_sound("klick.wav")

        # Simulate intelligent contact response after delay
        GLib.timeout_add(1400, lambda: self.simulate_reply(txt))

    def simulate_reply(self, user_txt):
        low = user_txt.lower()
        if "wanna get on" in low or "later" in low:
            reply = "kk :D"
        elif "music" in low or "playing" in low:
            reply = "omg love that song!!"
        elif "halo" in low or "game" in low:
            reply = "yeah invite me on xbox live later!"
        elif "nudge" in low:
            reply = "hey dont nudge me lol!"
        elif "hi" in low or "hey" in low:
            reply = "heyy what r u doing? :P"
        else:
            replies = [
                "yeah lol",
                "haha nice!",
                "brb getting some water",
                "did u see the bulletin on myspace?",
                "awesome :D",
                "ttyl mom is calling me for dinner"
            ]
            reply = random.choice(replies)

        self.append_message(self.contact["name"], reply, is_user=False)
        play_sound("msg.wav")
        return False

    def on_nudge_clicked(self, _):
        """Execute authentic MSN Messenger window vibration & nudge sound."""
        play_sound("nudge.wav")
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert_with_tags(end_iter, "--- You have just sent a nudge! ---\n\n", self.tag_nudge)

        # Shake window across screen
        orig_x, orig_y = self.get_position()
        offsets = [(10, 0), (-12, 6), (8, -8), (-10, -4), (12, 8), (-8, 4), (0, 0)]
        for i, (dx, dy) in enumerate(offsets):
            GLib.timeout_add(i * 35, lambda x=orig_x + dx, y=orig_y + dy: self.move(x, y))

        # Contact nudges back or replies
        GLib.timeout_add(2800, self.simulate_contact_nudge)

    def simulate_contact_nudge(self):
        play_sound("nudge.wav")
        cname = self.contact["name"]
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert_with_tags(end_iter, f"--- {cname} has just sent you a nudge! ---\n\n", self.tag_nudge)
        orig_x, orig_y = self.get_position()
        offsets = [(10, -4), (-12, 6), (8, -6), (-10, 4), (0, 0)]
        for i, (dx, dy) in enumerate(offsets):
            GLib.timeout_add(i * 35, lambda x=orig_x + dx, y=orig_y + dy: self.move(x, y))
        return False

    def on_emoticon_picker(self, btn):
        menu = Gtk.Menu()
        emojis = [
            (":) Smile", ":)"), (":D Laugh", ":-D"), (":P Tongue", ":-P"),
            (":O Surprise", ":-O"), (";) Wink", ";)"), (":| Disappointed", ":-|"),
            ("(H) Cool", "(H)"), ("(L) Love", "(L)"), ("(Y) Thumbs up", "(Y)"),
            ("(N) Thumbs down", "(N)"), ("(B) Beer", "(B)"), ("(D) Drink", "(D)")
        ]
        for label, code in emojis:
            it = Gtk.MenuItem(label=f"{label}  [{code}]")
            def on_pick(_, c=code):
                self.inp_buf.insert_at_cursor(f" {c} ")
            it.connect("activate", on_pick)
            menu.append(it)
        menu.show_all()
        menu.popup_at_widget(btn, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None)


class XpMsnToast(Gtk.Window):
    """Authentic MSN Messenger slide-up Toast Notification in bottom-right corner."""

    def __init__(self, contact_name, msg_text="has just signed in."):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("MSN Messenger")
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.get_style_context().add_class("xp-toast-box")

        # Buddy Icon DA
        icon_da = Gtk.DrawingArea()
        icon_da.set_size_request(40, 40)
        def draw_t_buddy(w, cr):
            draw_3d_buddy_avatar(cr, 20, 20, radius=18)
            return False
        icon_da.connect("draw", draw_t_buddy)
        box.pack_start(icon_da, False, False, 0)

        # Text column
        tcol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        thdr = Gtk.Label(label="<b>MSN Messenger</b>", use_markup=True, xalign=0.0)
        tmsg = Gtk.Label(label=f"<b>{contact_name}</b> {msg_text}", use_markup=True, xalign=0.0)
        tcol.pack_start(thdr, False, False, 0)
        tcol.pack_start(tmsg, False, False, 0)
        box.pack_start(tcol, True, True, 0)

        # Close X
        btn_x = Gtk.Button(label="×")
        btn_x.get_style_context().add_class("xp-chat-toolbtn")
        btn_x.connect("clicked", lambda *_: self.destroy())
        box.pack_end(btn_x, False, False, 0)

        self.add(box)

        # Position at bottom right corner above taskbar
        screen = Gdk.Screen.get_default()
        sw = screen.get_width() if screen else 1920
        sh = screen.get_height() if screen else 1080
        self.set_default_size(240, 75)
        self.move(sw - 260, sh - 120)

        # Auto close after 5 seconds
        GLib.timeout_add_seconds(5, self.destroy)


def main():
    # Force X11 backend if running on Wayland for smooth popup and toast positioning
    if os.environ.get("GDK_BACKEND") != "x11":
        os.environ["GDK_BACKEND"] = "x11"
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception:
            pass

    provider = Gtk.CssProvider()
    provider.load_from_data(MSN_CSS.encode())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "login"

    if mode in ("login", "start"):
        win = XpMsnLoginWindow()
    elif mode in ("contacts", "buddies"):
        win = XpMsnContactListWindow()
    elif mode in ("chat", "conversation"):
        cfg = load_config()
        win = XpMsnChatWindow(cfg["contacts"][0], cfg)
    elif mode == "toast":
        cname = sys.argv[2] if len(sys.argv) > 2 else "xXstar_girlXx"
        win = XpMsnToast(cname)
    else:
        win = XpMsnLoginWindow()

    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
