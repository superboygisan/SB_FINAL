import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall
from ntgcalls import TelegramServerError, FFmpegError
from pytgcalls.types import Update, StreamEnded
from pytgcalls import filters as fl
from pytgcalls.types import AudioQuality, VideoQuality, MediaStream, ChatUpdate
from pytgcalls.types.calls import GroupCallConfig

import config
from config import autoclean
from AnonXMusic import LOGGER, YouTube, app
from AnonXMusic.misc import db
from AnonXMusic.utils.database import (
    add_active_chat, add_active_video_chat, get_lang, get_loop,
    group_assistant, is_autoend, music_on, remove_active_chat,
    remove_active_video_chat, set_loop,
)
from AnonXMusic.utils.exceptions import AssistantErr
from AnonXMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from AnonXMusic.utils.inline.play import stream_markup
from AnonXMusic.utils.thumbnails import get_thumb
from strings import get_string

# Global locks for safety
QUEUE_LOCKS = {}
BACKGROUND_TASKS = set()

async def _clear_(chat_id):
    async with QUEUE_LOCKS.setdefault(chat_id, asyncio.Lock()):
        if chat_id in db:
            db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

class Call(PyTgCalls):
    # ... (baaki pura code same rahega jaise pehle diya tha)

    async def change_stream(self, client, chat_id):
        async with QUEUE_LOCKS.setdefault(chat_id, asyncio.Lock()):
            check = db.get(chat_id)
            if not check:
                await _clear_(chat_id)
                return
            # ... rest same (pop, loop etc.)

    # Better shutdown
    async def stop(self):
        for task in list(BACKGROUND_TASKS):
            if not task.done():
                task.cancel()
        await asyncio.gather(*BACKGROUND_TASKS, return_exceptions=True)
        # original leave calls