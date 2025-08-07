import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGODB_URI = os.getenv("MONGODB_URI")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")  # e.g., "@YourChannel"
BRANDING = os.getenv("BRANDING", "Bot by DPMods")
PING_INTERVAL = int(os.getenv("PING", 300))