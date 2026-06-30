import aiohttp
import asyncio
from typing import Dict, Any, Optional, Tuple

class YouTubeAPI:
    def __init__(self):
        self.api_base = "https://innertube-api-1.onrender.com/api"
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        session = await self.get_session()
        try:
            async with session.get(f"{self.api_base}{endpoint}", params=params, timeout=40) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    text = await resp.text()
                    print(f"API Error: {resp.status} - {text[:200]}")
                    return {"success": False}
        except Exception as e:
            print(f"Request Error: {e}")
            return {"success": False}

    async def url(self, message):
        try:
            if message.text and "http" in message.text:
                return message.text.strip()
            else:
                return message.text.replace("/play", "").strip() if message.text else ""
        except:
            return ""

    async def exists(self, url: str) -> bool:
        return True  # Simple fallback

    async def search(self, query: str) -> list:
        try:
                async def search(self, query: str) -> list:
        try:
            data = await self._request("/search", {"query": query, "limit": 10})
            if data.get("success") and data.get("results"):
                results = []
                for item in data["results"][:5]:  # Sirf 5 best results
                    results.append({
                        "id": item.get("video_id"),
                        "title": item.get("title"),
                        "duration": item.get("duration", "N/A"),
                        "views": item.get("view_count_text", ""),
                        "channel": item.get("channel", {}).get("name", ""),
                    })
                return results
            return []
        except Exception as e:
            print(f"Search Error: {e}")
            return []
        try:
            data = await self._request(f"/video/{video_id}")
            return data.get("success", False), data
        except:
            return False, None

    async def player(self, video_id: str) -> Dict:
        try:
            data = await self._request(f"/player/{video_id}")
            return data
        except:
            return {}

    async def next(self, video_id: str) -> Dict:
        try:
            return await self._request(f"/next/{video_id}")
        except:
            return {}

    async def download(self, *args, **kwargs):
        return None, False

    async def close(self):
        if self.session:
            await self.session.close()

cookie_txt_file = None