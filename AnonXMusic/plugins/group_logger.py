from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from config import LOGGER_ID


@app.on_message(filters.new_chat_members, group=-1)
async def bot_added(client, message: Message):
    for member in message.new_chat_members:
        if member.id == app.me.id:
            try:
                count = await client.get_chat_members_count(message.chat.id)
            except:
                count = "Unknown"

            await app.send_message(
                LOGGER_ID,
                f"""✅ **Bot Added To New Group**

🏷 **Group:** {message.chat.title}
🆔 **Group ID:** `{message.chat.id}`
👥 **Members:** {count}
👤 **Added By:** {message.from_user.mention if message.from_user else 'Unknown'}"""
            )


@app.on_message(filters.left_chat_member, group=-1)
async def bot_left(client, message: Message):
    if message.left_chat_member.id == app.me.id:
        await app.send_message(
            LOGGER_ID,
            f"""❌ **Bot Removed From Group**

🏷 **Group:** {message.chat.title}
🆔 **Group ID:** `{message.chat.id}`"""
        )