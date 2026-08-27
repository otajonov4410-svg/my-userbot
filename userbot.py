import asyncio
from telethon import TelegramClient, events

API_ID = 35865950
API_HASH = 'fcfd2a182ee4408ff03c04f05dfd87bd'

client = TelegramClient('userbot_session', API_ID, API_HASH)

ignored_chats = set()
chat_timers = {}

AUTO_REPLY_TEXT = (
    "Salom! Men hozir bandman yoki xabaringizni ko'rmadim.\n"
    "Tez orada javob beraman. Bu avtomatik xabar."
)

@client.on(events.NewMessage(incoming=True))
async def handle_incoming(event):
    if not event.is_private:
        return

    chat_id = event.chat_id

    if chat_id in ignored_chats:
        return

    if chat_id in chat_timers:
        chat_timers[chat_id].cancel()

    async def delayed_reply():
        await asyncio.sleep(30)
        await event.reply(AUTO_REPLY_TEXT)
        chat_timers.pop(chat_id, None)

    chat_timers[chat_id] = asyncio.create_task(delayed_reply())

@client.on(events.NewMessage(outgoing=True))
async def handle_outgoing(event):
    if event.is_private:
        chat_id = event.chat_id
        if chat_id in chat_timers:
            chat_timers[chat_id].cancel()
            chat_timers.pop(chat_id, None)
        ignored_chats.add(chat_id)

async def main():
    print("Userbot muvaffaqiyatli ishga tushdi!")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())