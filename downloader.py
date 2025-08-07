import re
import aiohttp

async def download_pinterest_video(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pinterest-video-download.com/download?url={url}") as resp:
            text = await resp.text()
            match = re.search(r'source src="([^"]+)"', text)
            return match.group(1) if match else None