import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events

# --- Render uchun Web Server (Doimiy ishni ta'minlash uchun) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Userbot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# --- Telegram Userbot Sozlamalari ---
API_ID = 35865950
API_HASH = 'fcfd2a182ee4408ff03c04f05dfd87bd'

client = TelegramClient('userbot_session', API_ID, API_HASH)

Ignored_chats = set()
chat_timers = {}

# Siz so'ragan mukammal va to'liq avto-javob matni:
AUTO_REPLY_TEXT = (
    "Salom! Men hozir bandman, xabaringiz ko'rildi. Tez orada o'zim aloqaga chiqaman.\n\n"
    "Agar juda zarur bo'lsa, shu raqamga aloqaga chiqing: +998900579196\n\n"
    "Undan oldin ikkita kanalimga obuna bo'lib turing:\n"
    "1️⃣ 1-kanalim: https://t.me/ongosti_uz\n"
    "2️⃣ 2-kanalim: https://t.me/jahongirfootball"
)

@client.on(events.NewMessage(incoming=True))
async def handle_incoming(event):
    # Faqat shaxsiy (private) chatlarga ishlaydi
    if not event.is_private:
        return

    chat_id = event.chat_id

    if chat_id in Ignored_chats:
        return

    if chat_id in chat_timers:
        chat_timers[chat_id].cancel()

    async def delayed_reply():
        await asyncio.sleep(30) # 30 soniya kutish
        
        # 1. Matnli xabarni yuborish
        await event.respond(AUTO_REPLY_TEXT)
        
        # 2. Animatsiyali stiker yuborish (Telegramdagi tayyor animatsiyali stiker havolasi/fayli)
        try:
            # Bu yerga Telegramdagi istalgan animatsiyali stikerning to'g'ridan-to'g'ri havolasini qo'yish mumkin
            await client.send_file(event.chat_id, 'https://t.me/addstickers/AnimatedStickers') 
        except:
            pass
            
        chat_timers.pop(chat_id, None)

    chat_timers[chat_id] = asyncio.create_task(delayed_reply())

@client.on(events.NewMessage(outgoing=True))
async def handle_outgoing(event):
    # Agar siz o'zingiz xabar yozsangiz, taymer o'chadi (javob yuborilmaydi)
    if not event.is_private:
        return
    chat_id = event.chat_id
    if chat_id in chat_timers:
        chat_timers[chat_id].cancel()
        chat_timers.pop(chat_id, None)

client.start()
client.run_until_disconnected()
