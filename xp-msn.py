#!/usr/bin/env python3
"""
MSN Messenger (2003/2004/2006 Retro Suite) for Windows XP on Bazzite KDE.
Authentic multi-window MSN Messenger client with Discord/Vesktop live integration.

Features:
- Authentic Startup / Login screen with 3D buddy avatar, status selector, and Luna 3D buttons
- Standalone Contactpersonenlijst venster (Buddy List) with user profile card, status, personal message,
  live Discord sync indicator, and categorized groups (Online, Away, Busy, Offline)
- Authentic Multi-Window Conversation experience matching media_1793540755051_35913dea.jpg:
  - Title: Luna Blue with "[Contact] - Conversation"
  - Menubar: File, Edit, Actions, Tools, Help
  - Action Toolbar: Invite, Send Files, Webcam, Audio, Fun & Games, plus circular action buttons and MSN butterfly logo
  - Header: "To: [Contact]" with security alert banner
  - Chat history with "[Contact] says:" formatting and color-coded tags
  - Dual avatar boxes on the right (Contact avatar on top, User avatar on bottom) with drawer toggle tabs
  - Formatting toolbar with "A Font", "😊" Emoticon picker, "Backgrounds ▾", and "⚡ Nudge!"
  - Text input area with classic Luna "Send" button
  - MSN Audio chimes (online.wav, msg.wav, nudge.wav)
  - Legendary window vibration/shake on Nudge!
- Live Discord / Vesktop Integration via Chrome DevTools Protocol (CDP) WebSocket on port 9222:
  - Pulls live friends and DMs with real usernames, avatars, presence statuses, and activities
  - Synchronizes sending and receiving of live messages in real time
  - Real-time slide-up MSN Toast notifications in bottom-right corner
  - Fallback to full autonomous simulation mode when offline
"""

import os
import sys
import json
import math
import time
import random
import subprocess
import threading
import urllib.request
import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib

try:
    import websockets
    import asyncio
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
if not os.path.isdir(SOUNDS_DIR):
    SOUNDS_DIR = os.path.expanduser("~/.local/share/xp-startknop/sounds")

AVATARS_DIR = os.path.join(BASE_DIR, "avatars")
if not os.path.isdir(AVATARS_DIR):
    AVATARS_DIR = os.path.expanduser("~/.local/share/xp-startknop/avatars")

AVATAR_CACHE_DIR = os.path.expanduser("~/.cache/xp-msn/avatars")
os.makedirs(AVATAR_CACHE_DIR, exist_ok=True)

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
    elif filename in ("klick.wav", "click.wav"):
        try:
            subprocess.Popen(["canberra-gtk-play", "-i", "button-pressed"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        {"name": "cooldude101", "email": "dude101@hotmail.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "duck"},
        {"name": "babygirl_03", "email": "bgirl@live.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "heart"},
        {"name": "skaterchick14", "email": "sk8rchick@hotmail.com", "group": "Offline", "status": "Offline", "pmsg": "", "avatar": "chess"}
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
    font-size: 11px;
    padding: 5px 18px;
    box-shadow: inset 1px 1px 0px #ffffff, 1px 1px 2px rgba(0,0,0,0.2);
}
.xp-btn-signin:hover {
    background-image: linear-gradient(to bottom, #fff5cc 0%, #ffe085 50%, #ffc947 100%);
    border-color: #e5a000;
    color: #000000;
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
    padding: 4px 14px;
    box-shadow: inset 1px 1px 0px #ffffff;
}
.xp-btn-luna:hover {
    background-image: linear-gradient(to bottom, #fff5cc 0%, #ffe085 50%, #ffc947 100%);
    border-color: #e5a000;
    color: #000000;
}

.xp-entry, .xp-entry text {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #7f9db9;
    border-radius: 0px;
    padding: 3px 6px;
    font-size: 11px;
}
.xp-entry:focus, .xp-entry text:focus {
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

.xp-contact-list-bg, .xp-contact-list-bg viewport {
    background-color: #ffffff;
    color: #000000;
}

.xp-contact-row {
    background: transparent;
    border: 1px solid transparent;
    padding: 2px 4px;
    color: #000000;
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
    background: linear-gradient(to bottom, #fcfdfe 0%, #ebf2fb 50%, #d8e5f7 100%);
    border-top: 1px solid #ffffff;
    border-bottom: 1px solid #b5d1f2;
    padding: 4px 8px;
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
    color: #000000;
}

.xp-chat-log, .xp-chat-log text {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #7f9db9;
    padding: 8px;
    font-size: 11px;
}

.xp-chat-input, .xp-chat-input text {
    background-color: #ffffff;
    color: #000000;
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

.xp-status-pill-online {
    background-color: #e1f5fe;
    border: 1px solid #81d4fa;
    color: #0277bd;
    font-size: 10px;
    font-weight: bold;
    padding: 1px 6px;
    border-radius: 8px;
}

.xp-status-pill-offline {
    background-color: #f5f5f5;
    border: 1px solid #cccccc;
    color: #777777;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 8px;
}
"""

def set_msn_window_icon(win):
    """Set authentic MSN Messenger icon on window titlebar and taskbar."""
    for icon_candidate in (
        os.path.join(AVATARS_DIR, "butterfly.png"),
        os.path.join(BASE_DIR, "package/contents/images/icons/msn.svg"),
        "/usr/share/icons/hicolor/32x32/apps/msn.png"
    ):
        if os.path.exists(icon_candidate):
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_candidate, 32, 32, True)
                win.set_icon(pb)
                return
            except Exception:
                pass

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
    head_grad = cairo.RadialGradient(cx - radius * 0.3, cy - radius * 0.4, 2, cx, cy - radius * 0.3, radius * 0.5)
    head_grad.add_color_stop_rgb(0.0, 0.65, 0.95, 0.65)
    head_grad.add_color_stop_rgb(0.4, 0.22, 0.72, 0.52)
    head_grad.add_color_stop_rgb(1.0, 0.05, 0.35, 0.32)
    cr.set_source(head_grad)
    cr.arc(cx, cy - radius * 0.25, radius * 0.42, 0, 2 * math.pi)
    cr.fill()

    body_grad = cairo.RadialGradient(cx - radius * 0.3, cy + radius * 0.3, 4, cx, cy + radius * 0.5, radius * 0.75)
    body_grad.add_color_stop_rgb(0.0, 0.62, 0.92, 0.62)
    body_grad.add_color_stop_rgb(0.5, 0.18, 0.65, 0.48)
    body_grad.add_color_stop_rgb(1.0, 0.04, 0.28, 0.25)
    cr.set_source(body_grad)
    cr.move_to(cx - radius * 0.65, cy + radius * 0.75)
    cr.curve_to(cx - radius * 0.6, cy + radius * 0.2, cx + radius * 0.6, cy + radius * 0.2, cx + radius * 0.65, cy + radius * 0.75)
    cr.close_path()
    cr.fill()

    draw_msn_butterfly(cr, cx + radius * 0.12, cy - radius * 0.1, size=radius * 0.85)
    cr.restore()


# ==============================================================================
# DISCORD CHROME DEVTOOLS PROTOCOL (CDP) BRIDGE
# ==============================================================================

class DiscordCdpBridge:
    """
    Connects to Vesktop / Discord via Chrome DevTools Protocol on ws://127.0.0.1:9222.
    Synchronizes users, statuses, DM channels, incoming/outgoing messages, and avatars.
    """

    def __init__(self, cdp_url="http://127.0.0.1:9222"):
        self.cdp_url = cdp_url
        self.loop = None
        self.ws = None
        self.is_connected = False
        self.current_user = None
        self.contacts = []
        self.on_user_updated = None
        self.on_contacts_updated = None
        self.on_message_received = None
        self.on_presence_updated = None
        self.req_id = 0
        self.pending_requests = {}
        self._thread = None
        self._running = False

    def start(self):
        if not HAS_WEBSOCKETS:
            print("websockets library not available. Running in standalone offline mode.")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

    def _run_event_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._worker_loop())

    async def _worker_loop(self):
        while self._running:
            try:
                # 1. Find the Discord target page
                req = urllib.request.Request(f"{self.cdp_url}/json", headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=2.5) as resp:
                    targets = json.loads(resp.read().decode())
                
                page = next((t for t in targets if t.get("type") == "page" and "Discord" in t.get("title", "")), None)
                if not page:
                    page = next((t for t in targets if t.get("type") == "page"), None)

                if page and page.get("webSocketDebuggerUrl"):
                    ws_url = page["webSocketDebuggerUrl"]
                    async with websockets.connect(ws_url) as ws:
                        self.ws = ws
                        self.is_connected = True
                        print("MSN -> Connected to Discord / Vesktop via CDP!")
                        await self._setup_discord_hooks()
                        
                        # Start background receiver and polling
                        receiver_task = asyncio.create_task(self._receive_messages())
                        poller_task = asyncio.create_task(self._poll_discord_state())
                        
                        done, pending = await asyncio.wait(
                            [receiver_task, poller_task],
                            return_when=asyncio.FIRST_EXCEPTION
                        )
                        for t in pending:
                            t.cancel()
            except Exception:
                pass

            self.is_connected = False
            self.ws = None
            await asyncio.sleep(3.0)

    async def _receive_messages(self):
        while self.is_connected and self.ws:
            try:
                raw = await self.ws.recv()
                data = json.loads(raw)
                rid = data.get("id")
                if rid in self.pending_requests:
                    fut = self.pending_requests.pop(rid)
                    if not fut.done():
                        res = data.get("result", {}).get("result", {}).get("value")
                        fut.set_result(res)
            except Exception:
                break

    async def _eval_js(self, js, await_promise=False):
        if not self.ws or not self.is_connected:
            return None
        self.req_id += 1
        rid = self.req_id
        fut = self.loop.create_future()
        self.pending_requests[rid] = fut
        msg = {
            "id": rid,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "returnByValue": True,
                "awaitPromise": await_promise
            }
        }
        await self.ws.send(json.dumps(msg))
        try:
            return await asyncio.wait_for(fut, timeout=6.0)
        except Exception:
            return None

    def evaluate_sync(self, js, await_promise=False):
        if not self.loop or not self.is_connected:
            return None
        fut = asyncio.run_coroutine_threadsafe(self._eval_js(js, await_promise), self.loop)
        try:
            return fut.result(timeout=5.0)
        except Exception:
            return None

    async def _setup_discord_hooks(self):
        """Inject event handlers into Discord via FluxDispatcher."""
        js = """(() => {
            if (!window.Vencord || !window.Vencord.Webpack) return false;
            const { Webpack } = window.Vencord;
            const dispatcher = Webpack.findByProps('dispatch', 'subscribe');
            window._xp_msn_inbox = window._xp_msn_inbox || [];
            window._xp_msn_presence = window._xp_msn_presence || [];

            if (dispatcher && !window._xp_msn_hooked) {
                dispatcher.subscribe('MESSAGE_CREATE', (e) => {
                    if (e && e.message) {
                        window._xp_msn_inbox.push({
                            channelId: e.message.channel_id,
                            id: e.message.id,
                            authorId: e.message.author?.id,
                            author: e.message.author?.username,
                            globalName: e.message.author?.global_name || e.message.author?.username,
                            content: e.message.content,
                            timestamp: e.message.timestamp
                        });
                    }
                });

                dispatcher.subscribe('PRESENCE_UPDATES', (e) => {
                    if (e && e.updates) {
                        for (const u of e.updates) {
                            window._xp_msn_presence.push({
                                userId: u.user?.id,
                                status: u.status
                            });
                        }
                    }
                });

                window._xp_msn_hooked = true;
            }
            return true;
        })()"""
        await self._eval_js(js)

    async def _poll_discord_state(self):
        """Periodically check for new messages, presence updates, and refresh contacts."""
        poll_count = 0
        while self.is_connected:
            try:
                # 1. Fetch user & contacts on initial run or every ~10s
                if poll_count % 10 == 0:
                    await self._fetch_user_and_contacts()

                # 2. Check incoming messages queue
                js_msgs = """(() => {
                    const msgs = window._xp_msn_inbox || [];
                    window._xp_msn_inbox = [];
                    return msgs;
                })()"""
                incoming = await self._eval_js(js_msgs)
                if incoming and isinstance(incoming, list):
                    for msg in incoming:
                        if self.on_message_received:
                            GLib.idle_add(self.on_message_received, msg["channelId"], msg)

                # 3. Check presence updates queue
                js_pres = """(() => {
                    const pres = window._xp_msn_presence || [];
                    window._xp_msn_presence = [];
                    return pres;
                })()"""
                pres_updates = await self._eval_js(js_pres)
                if pres_updates and isinstance(pres_updates, list):
                    for p in pres_updates:
                        if self.on_presence_updated:
                            GLib.idle_add(self.on_presence_updated, p["userId"], p["status"])

            except Exception:
                pass

            poll_count += 1
            await asyncio.sleep(0.6)

    async def _fetch_user_and_contacts(self):
        """Query Discord stores for current user and DM contacts."""
        js = """(() => {
            if (!window.Vencord || !window.Vencord.Webpack) return null;
            const { Webpack } = window.Vencord;
            const userStore = Webpack.findStore('UserStore');
            const chanStore = Webpack.findStore('ChannelStore');
            const presenceStore = Webpack.findStore('PresenceStore');
            if (!userStore || !chanStore) return null;

            const currentUser = userStore.getCurrentUser();
            const privateChans = chanStore.getMutablePrivateChannels ? chanStore.getMutablePrivateChannels() : {};
            
            const list = Object.values(privateChans)
                .filter(ch => ch.type === 1 || ch.type === 3)
                .map(ch => {
                    const recId = ch.recipients ? ch.recipients[0] : null;
                    const u = recId ? userStore.getUser(recId) : null;
                    const st = recId ? (presenceStore ? presenceStore.getStatus(recId) : 'offline') : 'offline';
                    
                    let pmsg = '';
                    if (recId && presenceStore) {
                        const acts = presenceStore.getActivities(recId) || [];
                        for (const a of acts) {
                            if (a.state) pmsg = a.state;
                            else if (a.name) pmsg = (a.type === 0 ? 'Playing ' : '') + a.name;
                        }
                    }

                    return {
                        channelId: ch.id,
                        type: ch.type,
                        userId: recId,
                        name: u ? (u.globalName || u.username) : (ch.name || 'Conversation'),
                        username: u ? u.username : null,
                        avatar: u?.avatar ? ('https://cdn.discordapp.com/avatars/' + recId + '/' + u.avatar + '.png?size=96') : null,
                        status: st || 'offline',
                        pmsg: pmsg,
                        lastMessageId: ch.lastMessageId
                    };
                })
                .sort((a, b) => (b.lastMessageId || '0').localeCompare(a.lastMessageId || '0'));

            return {
                user: currentUser ? {
                    id: currentUser.id,
                    username: currentUser.username,
                    globalName: currentUser.globalName,
                    avatar: currentUser.avatar ? ('https://cdn.discordapp.com/avatars/' + currentUser.id + '/' + currentUser.avatar + '.png?size=128') : null
                } : null,
                contacts: list
            };
        })()"""
        data = await self._eval_js(js)
        if data and isinstance(data, dict):
            u = data.get("user")
            if u:
                self.current_user = u
                if u.get("avatar"):
                    self.download_avatar_async(u["id"], u["avatar"])
                if self.on_user_updated:
                    GLib.idle_add(self.on_user_updated, u)

            cts = data.get("contacts")
            if cts is not None:
                self.contacts = cts
                # Trigger avatar downloads for top contacts
                for c in cts[:20]:
                    if c.get("userId") and c.get("avatar"):
                        self.download_avatar_async(c["userId"], c["avatar"])
                if self.on_contacts_updated:
                    GLib.idle_add(self.on_contacts_updated, cts)

    def download_avatar_async(self, uid, url):
        """Download remote avatar in background thread and cache locally."""
        def dl():
            dest = os.path.join(AVATAR_CACHE_DIR, f"{uid}.png")
            if not os.path.exists(dest):
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                    with urllib.request.urlopen(req, timeout=5) as r, open(dest, "wb") as f:
                        f.write(r.read())
                except Exception:
                    pass
        threading.Thread(target=dl, daemon=True).start()

    def send_message(self, channel_id, content):
        """Send message via Discord's internal sendMessage Webpack function."""
        if not self.is_connected:
            return False
        js = f"""(() => {{
            const {{ Webpack }} = window.Vencord;
            const actions = Webpack.findByProps('sendMessage');
            if (actions && actions.sendMessage) {{
                actions.sendMessage({json.dumps(channel_id)}, {{ content: {json.dumps(content)} }});
                return true;
            }}
            return false;
        }})()"""
        return self.evaluate_sync(js)

    def fetch_channel_history(self, channel_id, limit=20):
        """Fetch previous messages for channel from Discord MessageStore."""
        if not self.is_connected:
            return []
        js = f"""(async () => {{
            const {{ Webpack }} = window.Vencord;
            const messageActions = Webpack.findByProps('fetchMessages');
            const messageStore = Webpack.findStore('MessageStore');
            
            try {{
                if (messageActions && messageActions.fetchMessages) {{
                    await messageActions.fetchMessages({{ channelId: {json.dumps(channel_id)}, limit: {limit} }});
                }}
            }} catch(e) {{}}

            const ms = messageStore ? messageStore.getMessages({json.dumps(channel_id)}) : null;
            if (ms && ms.toArray) {{
                return ms.toArray().slice(-{limit}).map(m => ({{
                    id: m.id,
                    author: m.author?.username,
                    globalName: m.author?.globalName || m.author?.username,
                    isUser: m.author?.id === (Webpack.findStore('UserStore')?.getCurrentUser()?.id),
                    content: m.content,
                    timestamp: m.timestamp ? (m.timestamp.toISOString ? m.timestamp.toISOString() : String(m.timestamp)) : null
                }}));
            }}
            return [];
        }})()"""
        res = self.evaluate_sync(js, await_promise=True)
        return res if isinstance(res, list) else []


# Global bridge singleton
discord_bridge = DiscordCdpBridge()


def get_avatar_pixbuf(contact, size=96):
    """Retrieve or generate GdkPixbuf for a contact or current user."""
    # 1. Check cached Discord avatar by userId
    uid = contact.get("userId") or contact.get("id")
    if uid:
        cached_path = os.path.join(AVATAR_CACHE_DIR, f"{uid}.png")
        if os.path.exists(cached_path):
            try:
                return GdkPixbuf.Pixbuf.new_from_file_at_scale(cached_path, size, size, True)
            except Exception:
                pass

    # 2. Check named classic MSN avatars
    aname = contact.get("avatar", "soccer")
    for d in (AVATARS_DIR, os.path.join(BASE_DIR, "avatars")):
        target = os.path.join(d, f"{aname}.png")
        if os.path.exists(target):
            try:
                return GdkPixbuf.Pixbuf.new_from_file_at_scale(target, size, size, True)
            except Exception:
                pass

    # Default to soccer for contacts or chess for user
    default_pic = os.path.join(AVATARS_DIR, "soccer.png")
    if os.path.exists(default_pic):
        try:
            return GdkPixbuf.Pixbuf.new_from_file_at_scale(default_pic, size, size, True)
        except Exception:
            pass

    return None


# ==============================================================================
# AUTHENTIC LOGIN WINDOW
# ==============================================================================

class XpMsnLoginWindow(Gtk.Window):
    """Authentic MSN Messenger 6.0/7.0 Login Window."""

    def __init__(self, on_login_success=None):
        super().__init__(title="MSN Messenger")
        set_msn_window_icon(self)
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

        # Footer
        ftr_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ftr_row.set_margin_top(12)
        ftr_da = Gtk.DrawingArea()
        ftr_da.set_size_request(240, 24)
        def draw_ftr(w, cr):
            cr.set_source_rgb(0.2, 0.45, 0.8)
            cr.rectangle(2, 4, 14, 14); cr.fill()
            cr.set_source_rgb(1, 1, 1)
            cr.move_to(5, 11); cr.line_to(11, 11); cr.line_to(9, 8)
            cr.move_to(11, 11); cr.line_to(9, 14); cr.stroke()

            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(10)
            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.move_to(22, 15)
            cr.show_text("Microsoft .NET Messenger Service")
            return False
        ftr_da.connect("draw", draw_ftr)
        ftr_row.pack_start(ftr_da, False, False, 0)
        content.pack_start(ftr_row, False, False, 0)

        overlay.add_overlay(content)
        main_box.pack_start(overlay, True, True, 0)

        def draw_bg(widget, cr):
            w = widget.get_allocated_width()
            h = widget.get_allocated_height()
            pat = cairo.LinearGradient(0, 0, 0, h)
            pat.add_color_stop_rgb(0.0, 1.0, 1.0, 1.0)
            pat.add_color_stop_rgb(0.4, 0.93, 0.96, 0.99)
            pat.add_color_stop_rgb(1.0, 0.84, 0.90, 0.97)
            cr.set_source(pat)
            cr.rectangle(0, 0, w, h)
            cr.fill()

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


# ==============================================================================
# BUDDY LIST (CONTACTPERSONENLIJST) WINDOW
# ==============================================================================

class XpMsnContactListWindow(Gtk.Window):
    """
    Authentic MSN Messenger / Windows Live Messenger Buddy List.
    Multi-Window Controller: double-clicking contacts opens separate Conversation windows.
    """

    def __init__(self, cfg=None):
        super().__init__(title="MSN Messenger")
        set_msn_window_icon(self)
        self.set_default_size(320, 680)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.cfg = cfg or load_config()
        self.chat_windows = {}
        self.bridge = discord_bridge

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
        self.avatar_da.set_size_request(60, 60)
        def draw_usr_avatar(w, cr):
            # Frame
            cr.set_source_rgb(0.95, 0.97, 1.0)
            cr.rectangle(0, 0, 60, 60); cr.fill()
            cr.set_source_rgb(0.5, 0.7, 0.9)
            cr.set_line_width(1.5); cr.rectangle(0, 0, 60, 60); cr.stroke()

            # Try user avatar pixbuf
            u_info = getattr(self.bridge, "current_user", None) or self.cfg
            pb = get_avatar_pixbuf(u_info, size=56) if u_info else None
            if pb:
                Gdk.cairo_set_source_pixbuf(cr, pb, 2, 2)
                cr.paint()
            else:
                draw_3d_buddy_avatar(cr, 30, 30, radius=22)
            return False
        self.avatar_da.connect("draw", draw_usr_avatar)
        card.pack_start(self.avatar_da, False, False, 0)

        # User details column
        ucol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        
        dname = self.cfg.get("display_name", "King Geoffrey")
        self.lbl_name = Gtk.Label(label=f"<b>{dname}</b>", use_markup=True, xalign=0.0)
        name_row.pack_start(self.lbl_name, False, False, 0)

        # Status badge dropdown
        self.cb_my_status = Gtk.ComboBoxText()
        for s in ("(Online)", "(Busy)", "(Away)", "(Appear Offline)"):
            self.cb_my_status.append_text(s)
        self.cb_my_status.set_active(0)
        self.cb_my_status.connect("changed", self.on_my_status_changed)
        name_row.pack_start(self.cb_my_status, False, False, 0)
        ucol.pack_start(name_row, False, False, 0)

        # Personal message entry
        self.ent_pmsg = Gtk.Entry()
        self.ent_pmsg.set_text(self.cfg.get("personal_message", "listening 2 music ♫"))
        self.ent_pmsg.get_style_context().add_class("xp-entry")
        self.ent_pmsg.connect("changed", self.on_pmsg_changed)
        ucol.pack_start(self.ent_pmsg, False, False, 0)

        # Connection status pill
        self.lbl_conn = Gtk.Label(label="Checking Vesktop / Discord...", xalign=0.0)
        self.lbl_conn.get_style_context().add_class("xp-status-pill-offline")
        ucol.pack_start(self.lbl_conn, False, False, 0)

        card.pack_start(ucol, True, True, 0)
        vbox.pack_start(card, False, False, 0)

        # 3. Subtoolbar (Mail, Call, Search, Sync)
        stoolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        stoolbar.set_margin_start(8); stoolbar.set_margin_end(8); stoolbar.set_margin_bottom(4)
        for icon_lbl, tip, act in [
            ("✉ (0)", "Go to Hotmail Inbox", lambda: subprocess.Popen(["xdg-open", "https://mail.live.com"])),
            ("📞 Call", "Voice or phone call", lambda: play_sound("klick.wav")),
            ("🔍 Search", "Search the web", lambda: subprocess.Popen(["xdg-open", "https://www.google.com"])),
            ("🔄 Sync", "Sync with Discord / Vesktop", self.trigger_discord_sync)
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
        scroller.get_style_context().add_class("xp-contact-list-bg")
        self.contacts_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.contacts_vbox.set_margin_start(2); self.contacts_vbox.set_margin_end(2)
        scroller.add(self.contacts_vbox)
        vbox.pack_start(scroller, True, True, 0)

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
        btn_im.connect("clicked", self.open_first_contact_chat)
        act_row.pack_end(btn_im, False, False, 0)
        vbox.pack_start(act_row, False, False, 0)

        # 7. Bottom MSN .NET Ad Banner
        banner_da = Gtk.DrawingArea()
        banner_da.set_size_request(300, 48)
        def draw_banner(w, cr):
            bw = w.get_allocated_width()
            bh = w.get_allocated_height()
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(0, 0, bw, bh); cr.fill()
            cr.set_source_rgb(0.8, 0.85, 0.92)
            cr.set_line_width(1.0); cr.rectangle(0, 0, bw, bh); cr.stroke()

            cr.set_source_rgba(0.2, 0.45, 0.8, 0.25)
            draw_3d_buddy_avatar(cr, 24, 24, radius=16)

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

        # Hook up Discord Bridge callbacks
        self.bridge.on_user_updated = self.on_discord_user_updated
        self.bridge.on_contacts_updated = self.on_discord_contacts_updated
        self.bridge.on_message_received = self.on_discord_message_received
        self.bridge.on_presence_updated = self.on_discord_presence_updated

        # Start the background Discord CDP Bridge thread
        self.bridge.start()

        # Build initial list
        self.rebuild_contact_list()

        # Check bridge connection periodically
        GLib.timeout_add(1500, self.update_connection_status)

    def update_connection_status(self):
        if self.bridge.is_connected:
            self.lbl_conn.set_text("🟢 Connected to Discord (Vesktop)")
            self.lbl_conn.get_style_context().remove_class("xp-status-pill-offline")
            self.lbl_conn.get_style_context().add_class("xp-status-pill-online")
        else:
            self.lbl_conn.set_text("MSN .NET Service (Offline Mode)")
            self.lbl_conn.get_style_context().remove_class("xp-status-pill-online")
            self.lbl_conn.get_style_context().add_class("xp-status-pill-offline")
        return True

    def trigger_discord_sync(self):
        play_sound("klick.wav")
        if self.bridge.is_connected:
            threading.Thread(target=lambda: asyncio.run_coroutine_threadsafe(self.bridge._fetch_user_and_contacts(), self.bridge.loop), daemon=True).start()

    def on_discord_user_updated(self, u):
        if u:
            name = u.get("globalName") or u.get("username")
            self.lbl_name.set_markup(f"<b>{name}</b>")
            self.cfg["display_name"] = name
            self.avatar_da.queue_draw()

    def on_discord_contacts_updated(self, cts):
        if cts:
            self.rebuild_contact_list(filter_txt=self.search_ent.get_text().strip().lower())

    def on_discord_presence_updated(self, user_id, status):
        # Refresh contact status
        self.rebuild_contact_list(filter_txt=self.search_ent.get_text().strip().lower())

    def on_discord_message_received(self, channel_id, msg):
        """Handle incoming message: route to chat window or display Toast notification."""
        author = msg.get("globalName") or msg.get("author") or "Contact"
        content = msg.get("content", "")

        # Check if chat window for this channel is open
        if channel_id in self.chat_windows:
            win = self.chat_windows[channel_id]
            is_user = msg.get("authorId") == (self.bridge.current_user.get("id") if self.bridge.current_user else None)
            win.append_message(author, content, is_user=is_user)
            if "*NUDGE!*" in content or "*nudge*" in content.lower():
                win.trigger_incoming_nudge()
            else:
                play_sound("msg.wav")
        else:
            # Show authentic slide-up toast notification
            play_sound("msg.wav")
            toast = XpMsnToast(author, f"says:\n{content[:60]}", on_click=lambda: self.open_chat_by_channel(channel_id, author))
            toast.show_all()

    def open_chat_by_channel(self, channel_id, name):
        c = next((item for item in self.bridge.contacts if item.get("channelId") == channel_id), None)
        if not c:
            c = {"channelId": channel_id, "name": name, "status": "Online"}
        self.open_chat(c)

    def on_my_status_changed(self, cb):
        st = cb.get_active_text()
        if st:
            clean_st = st.replace("(", "").replace(")", "").strip()
            self.cfg["status"] = clean_st
            save_config(self.cfg)

    def on_pmsg_changed(self, ent):
        self.cfg["personal_message"] = ent.get_text()
        save_config(self.cfg)

    def on_search_changed(self, ent):
        self.rebuild_contact_list(filter_txt=ent.get_text().strip().lower())

    def open_first_contact_chat(self, *_):
        contacts = self.bridge.contacts if (self.bridge.is_connected and self.bridge.contacts) else self.cfg.get("contacts", [])
        if contacts:
            self.open_chat(contacts[0])

    def rebuild_contact_list(self, filter_txt=""):
        for child in self.contacts_vbox.get_children():
            self.contacts_vbox.remove(child)

        # Combine Discord contacts or offline config contacts
        if self.bridge.is_connected and self.bridge.contacts:
            contacts = self.bridge.contacts
        else:
            contacts = self.cfg.get("contacts", [])

        # Categorize into groups
        groups = {"Online": [], "Away": [], "Busy": [], "Offline": []}
        for c in contacts:
            st = (c.get("status") or "offline").lower()
            if st in ("online",):
                groups["Online"].append(c)
            elif st in ("idle", "away"):
                groups["Away"].append(c)
            elif st in ("dnd", "busy"):
                groups["Busy"].append(c)
            else:
                groups["Offline"].append(c)

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
                st = (c.get("status") or "offline").lower()
                def draw_st(w, cr, status=st):
                    if status == "online":
                        cr.set_source_rgb(0.2, 0.75, 0.2)
                        cr.arc(8, 5, 3.5, 0, 6.28); cr.fill()
                        cr.arc(8, 13, 5, 3.14, 6.28); cr.fill()
                    elif status in ("idle", "away"):
                        cr.set_source_rgb(0.95, 0.6, 0.1)
                        cr.arc(8, 8, 6, 0, 6.28); cr.fill()
                        cr.set_source_rgb(1, 1, 1)
                        cr.move_to(8, 4); cr.line_to(8, 8); cr.line_to(11, 8)
                        cr.set_line_width(1.4); cr.stroke()
                    elif status in ("dnd", "busy"):
                        cr.set_source_rgb(0.9, 0.2, 0.2)
                        cr.arc(8, 8, 6, 0, 6.28); cr.fill()
                        cr.set_source_rgb(1, 1, 1)
                        cr.move_to(4, 8); cr.line_to(12, 8)
                        cr.set_line_width(2.0); cr.stroke()
                    else:
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
                # Double-click opens conversation window
                row.connect("button-press-event", lambda _, ev, target=c: self.open_chat(target) if ev.type == Gdk.EventType._2BUTTON_PRESS else False)
                self.contacts_vbox.pack_start(row, False, False, 0)

        self.contacts_vbox.show_all()

    def open_chat(self, contact):
        """Open a dedicated, standalone Conversation window for this contact."""
        cid = contact.get("channelId") or contact.get("name")
        if cid in self.chat_windows:
            self.chat_windows[cid].present()
        else:
            chat = XpMsnChatWindow(contact, self.cfg, bridge=self.bridge)
            self.chat_windows[cid] = chat
            chat.connect("destroy", lambda *_: self.chat_windows.pop(cid, None))

            # Cascade window positioning so multiple conversation windows don't overlap
            count = len(self.chat_windows)
            cur_x, cur_y = self.get_position()
            offset_x = 340 + (count - 1) * 35
            offset_y = 50 + (count - 1) * 35
            chat.move(max(50, cur_x - offset_x), max(50, cur_y + offset_y))
            chat.show_all()

    def on_add_contact_dialog(self, _):
        dlg = Gtk.Dialog(title="Add a Contact", parent=self, flags=0)
        dlg.set_default_size(320, 140)
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
                    "name": cname, "email": val, "group": "Online", "status": "Online", "pmsg": "Hey there!", "avatar": "soccer"
                })
                save_config(self.cfg)
                self.rebuild_contact_list()
        dlg.destroy()


# ==============================================================================
# CONVERSATION / CHAT WINDOW (MATCHES media_1793540755051_35913dea.jpg)
# ==============================================================================

class XpMsnChatWindow(Gtk.Window):
    """
    Authentic MSN Messenger Conversation Window.
    Faithful recreation of media_1793540755051_35913dea.jpg:
    - Menubar: File, Edit, Actions, Tools, Help
    - Action Toolbar: Invite, Send Files, Webcam, Audio, Fun & Games, plus MSN logo
    - Info & Security Warning: "Never give out your password or credit card number..."
    - Dual Avatar Boxes: Contact on top, User on bottom, with drawer toggle tabs
    - Formatting Toolbar: Font, Emoticons, Backgrounds, and Nudge!
    - Multi-line text input with Luna Send button
    - Realistic window vibration on Nudge
    """

    def __init__(self, contact, user_cfg, bridge=None):
        self.cname = contact["name"]
        super().__init__(title=f"{self.cname} - Conversation")
        set_msn_window_icon(self)
        self.set_default_size(560, 520)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.contact = contact
        self.user_cfg = user_cfg
        self.bridge = bridge or discord_bridge
        self.my_name = (self.bridge.current_user.get("globalName") if (self.bridge and self.bridge.current_user) else None) or user_cfg.get("display_name", "King Geoffrey")
        self.channel_id = contact.get("channelId")

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_vbox)

        # 1. Menubar: File  Edit  Actions  Tools  Help
        mbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        mbar.get_style_context().add_class("xp-msn-menubar")
        for m in ("File", "Edit", "Actions", "Tools", "Help"):
            b = Gtk.Button(label=m)
            b.get_style_context().add_class("xp-msn-menubar-btn")
            if m == "File":
                b.connect("clicked", lambda *_: self.destroy())
            mbar.pack_start(b, False, False, 0)
        main_vbox.pack_start(mbar, False, False, 0)

        # 2. Action Toolbar: Invite | Send Files | Webcam | Audio | Fun & Games | Circular actions | MSN Logo
        act_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        act_bar.get_style_context().add_class("xp-chat-toolbar")

        # Left options circle
        btn_opt = Gtk.Button(label="⚙")
        btn_opt.get_style_context().add_class("xp-chat-toolbtn")
        act_bar.pack_start(btn_opt, False, False, 0)

        # Action items (icon + text below)
        actions = [
            ("👥 Invite", "Invite someone to this conversation"),
            ("📁 Send Files", "Send a file or photo"),
            ("📹 Webcam", "Start webcam video"),
            ("🎧 Audio", "Start voice conversation"),
            ("🎲 Fun & Games", "Play Tic-Tac-Toe, Minesweeper or Checkers")
        ]
        for label, tip in actions:
            tb = Gtk.Button(label=label)
            tb.set_tooltip_text(tip)
            tb.get_style_context().add_class("xp-chat-toolbtn")
            tb.connect("clicked", lambda _, t=tip: play_sound("klick.wav"))
            act_bar.pack_start(tb, False, False, 0)

        # Spacer to push MSN logo to far right
        spacer = Gtk.Box()
        act_bar.pack_start(spacer, True, True, 0)

        # Circular utility buttons
        for icon_s, tip_s in [("▶", "Play sound clip"), ("🚫", "Block contact")]:
            c_btn = Gtk.Button(label=icon_s)
            c_btn.set_tooltip_text(tip_s)
            c_btn.get_style_context().add_class("xp-chat-toolbtn")
            c_btn.connect("clicked", lambda *_: play_sound("klick.wav"))
            act_bar.pack_start(c_btn, False, False, 0)

        # MSN Logo DA
        msn_logo_da = Gtk.DrawingArea()
        msn_logo_da.set_size_request(68, 26)
        def draw_msn_logo(w, cr):
            cr.select_font_face("Tahoma", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(15)
            cr.set_source_rgb(0.0, 0.22, 0.55)
            cr.move_to(4, 18)
            cr.show_text("msn")
            draw_msn_butterfly(cr, 38, 4, 18)
            return False
        msn_logo_da.connect("draw", draw_msn_logo)
        act_bar.pack_start(msn_logo_da, False, False, 2)

        main_vbox.pack_start(act_bar, False, False, 0)

        # 3. Main Body Split: Left (Header + Chat Log + Input) vs Right (Dual Avatar Panels)
        body_hsplit = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        body_hsplit.set_margin_start(8); body_hsplit.set_margin_end(8)
        body_hsplit.set_margin_top(6); body_hsplit.set_margin_bottom(6)

        # --- LEFT PANE ---
        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        # Header: To + Security warning (exact match with media_1793540755051_35913dea.jpg)
        hdr_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        to_address = contact.get("email") or f"{self.cname} <@{contact.get('username', self.cname)}>"
        self.lbl_to = Gtk.Label(label=f"<b>To: {to_address}</b>", use_markup=True, xalign=0.0)
        self.lbl_sec = Gtk.Label(
            label="<span color='#555555'>👤 Never give out your password or credit card number in an instant message conversation.</span>",
            use_markup=True, xalign=0.0
        )
        hdr_box.pack_start(self.lbl_to, False, False, 0)
        hdr_box.pack_start(self.lbl_sec, False, False, 0)
        left_vbox.pack_start(hdr_box, False, False, 0)

        # Chat conversation log
        chat_scroll = Gtk.ScrolledWindow()
        chat_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.chat_view = Gtk.TextView()
        self.chat_view.set_editable(False)
        self.chat_view.set_cursor_visible(False)
        self.chat_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.chat_view.get_style_context().add_class("xp-chat-log")
        self.chat_buf = self.chat_view.get_buffer()

        # Text styles
        self.tag_contact = self.chat_buf.create_tag("contact_nick", foreground="#001961", weight=Pango.Weight.BOLD)
        self.tag_user = self.chat_buf.create_tag("user_nick", foreground="#b04000", weight=Pango.Weight.BOLD)
        self.tag_nudge = self.chat_buf.create_tag("nudge", foreground="#b00000", weight=Pango.Weight.BOLD)
        self.tag_system = self.chat_buf.create_tag("system", foreground="#707070", style=Pango.Style.ITALIC)

        chat_scroll.add(self.chat_view)
        left_vbox.pack_start(chat_scroll, True, True, 0)

        # Formatting Toolbar: A Font | 😊 | Backgrounds ▾ | ⚡ Nudge!
        fmt_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        fmt_bar.get_style_context().add_class("xp-chat-toolbar")

        btn_font = Gtk.Button(label="A Font")
        btn_font.get_style_context().add_class("xp-chat-toolbtn")
        btn_font.connect("clicked", lambda *_: play_sound("klick.wav"))
        fmt_bar.pack_start(btn_font, False, False, 0)

        btn_emo = Gtk.Button(label="😊 ▾")
        btn_emo.get_style_context().add_class("xp-chat-toolbtn")
        btn_emo.connect("clicked", self.on_emoticon_picker)
        fmt_bar.pack_start(btn_emo, False, False, 0)

        btn_bg = Gtk.Button(label="🖼️ Backgrounds ▾")
        btn_bg.get_style_context().add_class("xp-chat-toolbtn")
        btn_bg.connect("clicked", lambda *_: play_sound("klick.wav"))
        fmt_bar.pack_start(btn_bg, False, False, 0)

        btn_nudge = Gtk.Button(label="⚡ Nudge!")
        btn_nudge.set_tooltip_text("Send a nudge to shake the conversation window!")
        btn_nudge.get_style_context().add_class("xp-chat-toolbtn")
        btn_nudge.connect("clicked", self.on_nudge_clicked)
        fmt_bar.pack_start(btn_nudge, False, False, 0)

        left_vbox.pack_start(fmt_bar, False, False, 0)

        # Input box + Send Button
        input_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        inp_scroll = Gtk.ScrolledWindow()
        inp_scroll.set_size_request(-1, 64)
        inp_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.inp_view = Gtk.TextView()
        self.inp_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.inp_view.get_style_context().add_class("xp-chat-input")
        self.inp_buf = self.inp_view.get_buffer()
        self.inp_view.connect("key-press-event", self.on_input_key)
        inp_scroll.add(self.inp_view)
        input_row.pack_start(inp_scroll, True, True, 0)

        # Classic Windows XP Luna Send Button
        self.btn_send = Gtk.Button(label="Send")
        self.btn_send.get_style_context().add_class("xp-btn-signin")
        self.btn_send.set_size_request(68, -1)
        self.btn_send.connect("clicked", lambda *_: self.send_message())
        input_row.pack_start(self.btn_send, False, False, 0)

        left_vbox.pack_start(input_row, False, False, 0)

        body_hsplit.pack_start(left_vbox, True, True, 0)

        # --- RIGHT PANE (DUAL AVATARS) ---
        side_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        side_panel.set_size_request(118, -1)

        # 1. Contact Avatar Frame (Top - Soccer Ball or Discord avatar)
        self.contact_avatar_da = Gtk.DrawingArea()
        self.contact_avatar_da.set_size_request(116, 110)
        self.contact_avatar_da.connect("draw", self.draw_contact_avatar_box)
        side_panel.pack_start(self.contact_avatar_da, False, False, 0)

        # Spacer between top and bottom avatar
        side_panel.pack_start(Gtk.Box(), True, True, 0)

        # 2. User Avatar Frame (Bottom - Chess Pieces or Discord avatar)
        self.user_avatar_da = Gtk.DrawingArea()
        self.user_avatar_da.set_size_request(116, 110)
        self.user_avatar_da.connect("draw", self.draw_user_avatar_box)
        side_panel.pack_end(self.user_avatar_da, False, False, 0)

        body_hsplit.pack_start(side_panel, False, False, 0)
        main_vbox.pack_start(body_hsplit, True, True, 0)

        # 4. Status Bar
        now_str = time.strftime("%I:%M %p")
        self.lbl_status = Gtk.Label(label=f"Last message received at {now_str}.", xalign=0.0)
        self.lbl_status.set_margin_start(10); self.lbl_status.set_margin_bottom(4)
        main_vbox.pack_start(self.lbl_status, False, False, 0)

        # Load history or show initial message
        self.load_initial_history()

    def draw_contact_avatar_box(self, widget, cr):
        """Draw authentic rounded avatar box with drawer toggle tab on right edge."""
        fx, fy, fw, fh = 2, 2, 98, 98
        r = 6

        # Frame background & border
        cr.set_source_rgb(1, 1, 1)
        cr.new_sub_path()
        cr.arc(fx + r, fy + r, r, 3.14, 4.71)
        cr.arc(fx + fw - r, fy + r, r, 4.71, 6.28)
        cr.arc(fx + fw - r, fy + fh - r, r, 0, 1.57)
        cr.arc(fx + r, fy + fh - r, r, 1.57, 3.14)
        cr.close_path()
        cr.fill_preserve()
        cr.set_source_rgb(0.72, 0.80, 0.88)
        cr.set_line_width(1.5)
        cr.stroke()

        # Contact Avatar image
        pb = get_avatar_pixbuf(self.contact, size=90)
        if pb:
            Gdk.cairo_set_source_pixbuf(cr, pb, fx + 4, fy + 4)
            cr.paint()
        else:
            draw_3d_buddy_avatar(cr, fx + fw / 2, fy + fh / 2, radius=32)

        # Drawer toggle tab on right edge
        tx, ty, tw, th = fx + fw, fy + 32, 10, 32
        cr.set_source_rgb(0.88, 0.92, 0.96)
        cr.rectangle(tx, ty, tw, th); cr.fill_preserve()
        cr.set_source_rgb(0.72, 0.80, 0.88)
        cr.set_line_width(1.0); cr.stroke()

        # Arrow >
        cr.set_source_rgb(0.3, 0.45, 0.6)
        cr.move_to(tx + 3, ty + 12); cr.line_to(tx + 7, ty + 16); cr.line_to(tx + 3, ty + 20)
        cr.set_line_width(1.4); cr.stroke()
        return False

    def draw_user_avatar_box(self, widget, cr):
        """Draw authentic user avatar box (chess pieces or Discord avatar) with toggle tab."""
        fx, fy, fw, fh = 2, 2, 98, 98
        r = 6

        # Frame background & border
        cr.set_source_rgb(1, 1, 1)
        cr.new_sub_path()
        cr.arc(fx + r, fy + r, r, 3.14, 4.71)
        cr.arc(fx + fw - r, fy + r, r, 4.71, 6.28)
        cr.arc(fx + fw - r, fy + fh - r, r, 0, 1.57)
        cr.arc(fx + r, fy + fh - r, r, 1.57, 3.14)
        cr.close_path()
        cr.fill_preserve()
        cr.set_source_rgb(0.72, 0.80, 0.88)
        cr.set_line_width(1.5)
        cr.stroke()

        # User Avatar image (default chess pieces)
        u_info = getattr(self.bridge, "current_user", None) or {"avatar": "chess"}
        pb = get_avatar_pixbuf(u_info, size=90)
        if pb:
            Gdk.cairo_set_source_pixbuf(cr, pb, fx + 4, fy + 4)
            cr.paint()
        else:
            # Fallback to chess pieces
            chess_path = os.path.join(AVATARS_DIR, "chess.png")
            if os.path.exists(chess_path):
                cpb = GdkPixbuf.Pixbuf.new_from_file_at_scale(chess_path, 90, 90, True)
                Gdk.cairo_set_source_pixbuf(cr, cpb, fx + 4, fy + 4)
                cr.paint()
            else:
                draw_3d_buddy_avatar(cr, fx + fw / 2, fy + fh / 2, radius=32)

        # Drawer toggle tab on right edge
        tx, ty, tw, th = fx + fw, fy + 32, 10, 32
        cr.set_source_rgb(0.88, 0.92, 0.96)
        cr.rectangle(tx, ty, tw, th); cr.fill_preserve()
        cr.set_source_rgb(0.72, 0.80, 0.88)
        cr.set_line_width(1.0); cr.stroke()

        # Arrow >
        cr.set_source_rgb(0.3, 0.45, 0.6)
        cr.move_to(tx + 3, ty + 12); cr.line_to(tx + 7, ty + 16); cr.line_to(tx + 3, ty + 20)
        cr.set_line_width(1.4); cr.stroke()
        return False

    def load_initial_history(self):
        """Fetch channel history from Discord or show nostalgic sample message."""
        if self.channel_id and self.bridge and self.bridge.is_connected:
            def bg_load():
                history = self.bridge.fetch_channel_history(self.channel_id, limit=12)
                if history:
                    def insert_history():
                        for m in history:
                            author = m.get("globalName") or m.get("author") or "Contact"
                            self.append_message(author, m["content"], is_user=m.get("isUser", False))
                        return False
                    GLib.idle_add(insert_history)
                else:
                    GLib.idle_add(lambda: self.append_message(self.cname, "Hey, wanna come over today? 😊😄", is_user=False))
            threading.Thread(target=bg_load, daemon=True).start()
        else:
            # Nostalgic message matching reference photo
            self.append_message(self.cname, "Hey, wanna come over today? 😊😄", is_user=False)

    def append_message(self, author, text, is_user=False):
        """Append message in authentic MSN format: '[Author] says:' followed by indented body."""
        end_iter = self.chat_buf.get_end_iter()
        tag = self.tag_user if is_user else self.tag_contact
        self.chat_buf.insert_with_tags(end_iter, f"{author} says:\n", tag)
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert(end_iter, f"  {text}\n\n")

        # Update status
        now_str = time.strftime("%I:%M %p")
        self.lbl_status.set_text(f"Last message received at {now_str}.")

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

        # If connected to Discord, dispatch to real channel
        if self.channel_id and self.bridge and self.bridge.is_connected:
            threading.Thread(target=lambda: self.bridge.send_message(self.channel_id, txt), daemon=True).start()
        else:
            # Simulation reply after short delay
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

        self.append_message(self.cname, reply, is_user=False)
        play_sound("msg.wav")
        return False

    def on_nudge_clicked(self, _):
        """Execute authentic MSN Messenger window vibration & nudge sound."""
        play_sound("nudge.wav")
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert_with_tags(end_iter, "--- You have just sent a nudge! ---\n\n", self.tag_nudge)

        # Shake conversation window
        orig_x, orig_y = self.get_position()
        offsets = [(14, 0), (-16, 8), (12, -10), (-14, 6), (10, -6), (-8, 4), (6, -2), (0, 0)]
        for i, (dx, dy) in enumerate(offsets):
            GLib.timeout_add(i * 30, lambda x=orig_x + dx, y=orig_y + dy: self.move(x, y))

        # Send nudge to Discord if connected
        if self.channel_id and self.bridge and self.bridge.is_connected:
            threading.Thread(target=lambda: self.bridge.send_message(self.channel_id, "*NUDGE!*"), daemon=True).start()
        else:
            GLib.timeout_add(2800, self.simulate_contact_nudge)

    def trigger_incoming_nudge(self):
        """Incoming nudge handler (from Discord or simulation)."""
        play_sound("nudge.wav")
        end_iter = self.chat_buf.get_end_iter()
        self.chat_buf.insert_with_tags(end_iter, f"--- {self.cname} has just sent you a nudge! ---\n\n", self.tag_nudge)
        orig_x, orig_y = self.get_position()
        offsets = [(14, -6), (-16, 8), (12, -8), (-12, 6), (8, -4), (-6, 2), (0, 0)]
        for i, (dx, dy) in enumerate(offsets):
            GLib.timeout_add(i * 30, lambda x=orig_x + dx, y=orig_y + dy: self.move(x, y))

    def simulate_contact_nudge(self):
        self.trigger_incoming_nudge()
        return False

    def on_emoticon_picker(self, btn):
        menu = Gtk.Menu()
        emojis = [
            (":) Smile", ":)"), (":D Laugh", ":-D"), (":P Tongue", ":-P"),
            (":O Surprise", ":-O"), (";) Wink", ";)"), (":| Disappointed", ":-|"),
            ("(H) Cool", "(H)"), ("(L) Love", "(L)"), ("(Y) Thumbs up", "(Y)"),
            ("(N) Thumbs down", "(N)"), ("(B) Beer", "(B)"), ("(D) Drink", "(D)"),
            ("(K) Kiss", "(K)"), ("(G) Gift", "(G)"), ("(F) Flower", "(F)"), ("(S) Star", "(S)")
        ]
        for label, code in emojis:
            it = Gtk.MenuItem(label=f"{label}  [{code}]")
            def on_pick(_, c=code):
                self.inp_buf.insert_at_cursor(f" {c} ")
            it.connect("activate", on_pick)
            menu.append(it)
        menu.show_all()
        menu.popup_at_widget(btn, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None)


# ==============================================================================
# SLIDE-UP MSN TOAST NOTIFICATION
# ==============================================================================

class XpMsnToast(Gtk.Window):
    """Authentic MSN Messenger slide-up Toast Notification in bottom-right corner."""

    def __init__(self, contact_name, msg_text="has just signed in.", on_click=None):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("MSN Messenger")
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)
        self.on_click = on_click

        ebox = Gtk.EventBox()
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

        ebox.add(box)
        if on_click:
            ebox.connect("button-press-event", self._on_toast_clicked)
        self.add(ebox)

        # Position at bottom right corner above taskbar
        screen = Gdk.Screen.get_default()
        sw = screen.get_width() if screen else 1920
        sh = screen.get_height() if screen else 1080
        self.set_default_size(260, 75)
        self.move(sw - 280, sh - 130)

        # Auto close after 5 seconds
        GLib.timeout_add_seconds(5, self.destroy)

    def _on_toast_clicked(self, *args):
        self.destroy()
        if self.on_click:
            self.on_click()
        return True


# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================

def main():
    # Force X11 backend if running on Wayland for multi-window management and smooth shake
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

    if mode in ("contacts", "buddies", "main"):
        win = XpMsnContactListWindow()
    elif mode in ("chat", "conversation"):
        cfg = load_config()
        contact = cfg["contacts"][0]
        if len(sys.argv) > 2:
            contact["name"] = sys.argv[2]
        win = XpMsnChatWindow(contact, cfg)
    elif mode == "toast":
        cname = sys.argv[2] if len(sys.argv) > 2 else "William"
        win = XpMsnToast(cname)
    elif mode == "multi":
        # Launch Buddy List and open 2 separate sample Conversation windows
        cfg = load_config()
        bl = XpMsnContactListWindow(cfg)
        bl.move(120, 80)
        bl.show_all()
        c1 = cfg["contacts"][3] if len(cfg["contacts"]) > 3 else cfg["contacts"][0]
        c2 = cfg["contacts"][1] if len(cfg["contacts"]) > 1 else {"name": "sk8rboy_07", "status": "online"}
        bl.open_chat(c1)
        bl.open_chat(c2)
        k1 = c1.get("channelId") or c1.get("name")
        k2 = c2.get("channelId") or c2.get("name")
        if k1 in bl.chat_windows:
            bl.chat_windows[k1].move(480, 100)
        if k2 in bl.chat_windows:
            bl.chat_windows[k2].move(1080, 140)
        Gtk.main()
        return
    else:
        # Default: Login window or directly to contacts if auto_login enabled
        cfg = load_config()
        if cfg.get("auto_login"):
            win = XpMsnContactListWindow(cfg)
        else:
            win = XpMsnLoginWindow()

    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
