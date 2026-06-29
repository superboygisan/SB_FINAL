import asyncio
import glob
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Union
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from ytSearch import VideosSearch, Playlist
from AnonXMusic import LOGGER
from AnonXMusic.utils.database import is_on_off
from AnonXMusic.utils.formatters import time_to_seconds
from config import YT_API_KEY

logger = LOGGER(__name__)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        self.dl_stats = {"total": 0, "success": 0, "fail": 0}
        self.lock = asyncio.Lock()

    # ... (other methods unchanged until download)

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        **kwargs,
    ) -> str:
        if videoid:
            vid_id = link
            link = self.base + link

        async with self.lock:
            self.dl_stats["total"] += 1

        try:
            # Primary: yt-dlp (reliable)
            ydl_opts = {
                'format': 'bestaudio/best' if not video else 'best[height<=720]',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'retries': 5,
                'fragment_retries': 5,
                'continuedl': True,
            }

            def sync_download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    return ydl.prepare_filename(info)

            loop = asyncio.get_running_loop()
            file_path = await loop.run_in_executor(None, sync_download)

            async with self.lock:
                self.dl_stats["success"] += 1
            return file_path

        except Exception as e:
            logger.warning(f"yt-dlp failed for {link}, error: {e}")
            # Fallback logic (if needed)
            async with self.lock:
                self.dl_stats["fail"] += 1
            raise