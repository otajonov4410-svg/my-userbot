import asyncio
from telethon import TelegramClient, events

# O'zingizning api_id va api_hash ma'lumotlaringiz
api_id = 24718503
api_hash = '976865d1d6a67451994b633b4974f183'

client = TelegramClient('my_session', api_id, api_hash)

# Avto-javob matni
AUTO_REPLY_TEXT = (
    "Salom! Men hozir bandman, xabaringiz ko'rildi. Tez orada o'zim aloqaga chiqaman.\n\n"
    "Agar juda zarur bo'lsa, shu raqamga aloqaga chiqing: +998900579196\n\n"
    "Undan oldin ikkita kanalimga obuna bo'lib turing:\n"
    "1️⃣ 1-kanalim: https://t.me/ongosti_uz\n"
    "2️⃣ 2-kanalim: https://t.me/jahongirfootball"
)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    # 10 soniya kutish
    await asyncio.sleep(10)
    
    # Matnni yuborish
    await event.respond(AUTO_REPLY_TEXT)
    
    # Animatsiyali stiker yuborish
    await event.client.send_file(event.chat_id, 'https://t.me/addstickers/AnimatedStickersEmoji')

client.start()
client.run_until_disconnected()
