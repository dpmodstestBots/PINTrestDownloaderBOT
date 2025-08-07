import asyncio
import aiohttp
from config import PING_INTERVAL

async def keep_alive():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get("https://your-render-url.onrender.com")
        except Exception:
            pass
        await asyncio.sleep(PING_INTERVAL)