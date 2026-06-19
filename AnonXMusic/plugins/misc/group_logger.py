import random

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import LOGGER_ID as LOG_GROUP_ID
from AnonXMusic import app
from AnonXMusic.utils.database import get_assistant


PHOTO = [
    "https://te.legra.ph/file/758a5cf4598f061f25963.jpg",
    "https://te.legra.ph/file/30a1dc870bd1a485e3567.jpg",
    "https://te.legra.ph/file/d585beb2a6b3f553299d2.jpg",
    "https://te.legra.ph/file/7df9e128dd261de2afd6b.jpg",
    "https://te.legra.ph/file/f60ebb75ad6f2786efa4e.jpg",
]


@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message: Message):
    for member in message.new_chat_members:
        if not member.is_self:
            continue

        try:
            count = await app.get_chat_members_count(message.chat.id)
        except:
            count = "Unknown"

        username = message.chat.username or "Private Group"

        try:
            await app.send_photo(
                LOG_GROUP_ID,
                photo=random.choice(PHOTO),
                caption=(
                    f"📝𝐌ᴜsɪᴄ 𝐁ᴏᴛ 𝐀ᴅᴅᴇᴅ 𝐈ɴ 𝐀 #𝐍ᴇᴡ_𝐆ʀᴏᴜᴘ**\n\n"
                    f"📌𝐂ʜᴀᴛ 𝐍ᴀᴍᴇ: {message.chat.title}\n"
                    f"🍂𝐂ʜᴀᴛ 𝐈ᴅ: `{message.chat.id}`\n"
                    f"🔐𝐂ʜᴀᴛ 𝐔sᴇʀɴᴀᴍᴇ: @{username if message.chat.username else 'None'}\n"
                    f"📈𝐆ʀᴏᴜᴘ 𝐌ᴇᴍʙᴇʀs: {count}\n"
                    f"🤔𝐀ᴅᴅᴇᴅ 𝐁ʏ: {message.from_user.mention if message.from_user else 'Unknown'}"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "👤 Added By",
                                url=f"tg://user?id={message.from_user.id}"
                                if message.from_user
                                else "https://telegram.org",
                            )
                        ]
                    ]
                ),
            )
        except Exception as e:
            print(e)

        if message.chat.username:
            try:
                assistant = await get_assistant(message.chat.id)
                await assistant.join_chat(message.chat.username)
            except Exception:
                pass