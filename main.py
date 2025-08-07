from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from downloader import download_pinterest_video
from database import add_user, users
from keep_alive import keep_alive
import asyncio

app = Client("pinterest_bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user.id
    add_user(user)

    if FORCE_SUB_CHANNEL:
        try:
            member = await app.get_chat_member(FORCE_SUB_CHANNEL, user)
            if member.status not in ["member", "administrator", "creator"]:
                raise Exception("Not joined")
        except:
            await message.reply_text(
                "Please join our channel first to use this bot!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.strip('@')}")],
                    [InlineKeyboardButton("Refresh", callback_data="refresh")]
                ])
            )
            return

    await message.reply_text(
        f"👋 Hello! Send me a Pinterest video URL to download.\n\n{BRANDING}"
    )

@app.on_callback_query(filters.regex("refresh"))
async def refresh(client, callback_query):
    user = callback_query.from_user.id
    try:
        member = await app.get_chat_member(FORCE_SUB_CHANNEL, user)
        if member.status in ["member", "administrator", "creator"]:
            await callback_query.message.edit("✅ You're verified! Now send your Pinterest link.")
        else:
            raise Exception("Not joined")
    except:
        await callback_query.answer("You're not in the channel yet!", show_alert=True)

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_url(client, message):
    url = message.text.strip()

    if "pinterest" not in url:
        return await message.reply("❌ Invalid Pinterest URL.")

    msg = await message.reply("🔄 Processing...")
    video_url = await download_pinterest_video(url)

    if video_url:
        await msg.edit("✅ Downloading...")
        await app.send_video(message.chat.id, video=video_url, caption=BRANDING)
    else:
        await msg.edit("❌ Failed to get video. Try a different link.")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")

    count = 0
    for user in users.find():
        try:
            await message.reply_to_message.copy(user["_id"])
            count += 1
        except:
            pass
    await message.reply(f"✅ Broadcast sent to {count} users.")

async def main():
    await app.start()
    asyncio.create_task(keep_alive())
    print("Bot running...")
    await idle()

from pyrogram import idle

if __name__ == "__main__":
    async def runner():
        await app.start()
        asyncio.create_task(keep_alive())  # self-pinger
        print("Bot is running...")
        await idle()
        await app.stop()

    asyncio.run(runner())

