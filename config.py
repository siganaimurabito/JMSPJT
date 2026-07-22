import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# .env 読み込み
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

# ==========================================
# 共通設定
# ==========================================

APP_NAME = "Discord-Line Sync Bot"
VERSION = "1.0.0"

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==========================================
# Discord
# ==========================================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))

DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ==========================================
# LINE
# ==========================================

LINE_CHANNEL_ACCESS_TOKEN = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN"
)

LINE_CHANNEL_SECRET = os.getenv(
    "LINE_CHANNEL_SECRET"
)

LINE_GROUP_ID = os.getenv("LINE_GROUP_ID")

# ==========================================
# Database
# ==========================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR/'database.db'}"
)

# ==========================================
# Media
# ==========================================

MEDIA_FOLDER = BASE_DIR / "media"
MEDIA_FOLDER.mkdir(exist_ok=True)

MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB

# ==========================================
# Security
# ==========================================

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

ALLOWED_IPS = [
    ip.strip()
    for ip in os.getenv("ALLOWED_IPS", "").split(",")
    if ip.strip()
]

# ==========================================
# Retry
# ==========================================

MAX_RETRY = 5

RETRY_DELAY = 2

# ==========================================
# Loop Prevention
# ==========================================

MESSAGE_CACHE_SIZE = 500

CACHE_EXPIRE_SECONDS = 300

# ==========================================
# Feature Flags
# ==========================================

ENABLE_IMAGE = True
ENABLE_VIDEO = True
ENABLE_AUDIO = True
ENABLE_FILE = True
ENABLE_STICKER = True

# ==========================================
# Validation
# ==========================================

_required = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "LINE_CHANNEL_ACCESS_TOKEN": LINE_CHANNEL_ACCESS_TOKEN,
    "LINE_CHANNEL_SECRET": LINE_CHANNEL_SECRET,
}

missing = [
    key
    for key, value in _required.items()
    if not value
]

if missing:
    raise RuntimeError(
        "Missing environment variables:\n"
        + "\n".join(missing)
    )
