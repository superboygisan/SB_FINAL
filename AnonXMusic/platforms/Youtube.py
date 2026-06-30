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
            async with session.get(f"{self.api_base}{endpoint}", params=params, timeout=30) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"success": False, "error": f"HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            print(f"YouTubeAPI Error: {e}")
            return {"success": False, "error": str(e)}

    async def url(self, message):
        """Message se URL ya query extract karne ke liye"""
        try:
            if message.text and message.text.startswith("http"):
                return message.text.strip()
            else:
                query = message.text.replace("/play", "").strip() if message.text else ""
                return query
        except:
            return ""

    async def search(self, query: str) -> list:
        try:
            data = await self._request("/search", {"query": query, "limit": 15})
            if data.get("success") and data.get("results"):
                return data["results"]
            return []
        except:
            return []

    async def video(self, video_id: str) -> Tuple[bool, Any]:
        try:
            data = await self._request(f"/video/{video_id}")
            if data.get("success"):
                return True, data
            return False, None
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
            data = await self._request(f"/next/{video_id}")
            return data
        except:
            return {}

    async def close(self):
        if self.session:
            await self.session.close()

# Error fix
cookie_txt_file = None