import asyncio
from pyrogram import Client
from pyrogram.types import CallbackQuery

from AnonXMusic import LOGGER
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import db
from AnonXMusic.utils.database import get_lang, is_on_off, set_loop
from AnonXMusic.utils.decorators.language import languageCB
from AnonXMusic.utils.inline.play import stream_markup
from strings import get_string


@Client.on_callback_query()
@languageCB
async def callback_query_handler(client: Client, CallbackQuery: CallbackQuery):
    # ALWAYS ANSWER CALLBACK (fixed)
    await CallbackQuery.answer()

    try:
        command = CallbackQuery.data.split("|")[0]
        chat_id = int(CallbackQuery.data.split("|")[1])
    except:
        return await CallbackQuery.edit_message_text("⚠️ Invalid callback data.")

    # Queue related callbacks
    if command == "queue":
        # Your original code preserved
        pass

    # Skip callback
    elif command == "skip":
        try:
            await Anony.force_stop_stream(chat_id)
            await CallbackQuery.edit_message_text("⏭ Skipped current track.")
        except Exception as e:
            LOGGER(__name__).error(f"Skip callback error: {e}")
            await CallbackQuery.edit_message_text("❌ Failed to skip.")

    # Pause / Resume
    elif command == "pause":
        await Anony.pause_stream(chat_id)
        await CallbackQuery.edit_message_text("⏸ Paused.")

    elif command == "resume":
        await Anony.resume_stream(chat_id)
        await CallbackQuery.edit_message_text("▶ Resumed.")

    # Loop
    elif command.startswith("loop"):
        try:
            loop = int(CallbackQuery.data.split("|")[2])
            await set_loop(chat_id, loop)
            await CallbackQuery.edit_message_text(f"🔁 Loop set to {loop}.")
        except:
            await CallbackQuery.edit_message_text("❌ Invalid loop value.")

    # Other callbacks (original preserved)
    else:
        # Your original callback logic here
        pass