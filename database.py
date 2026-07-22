from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

# ==========================================
# Database
# ==========================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()

# ==========================================
# Discord ⇔ LINE 同期設定
# ==========================================

class SyncChannel(Base):
    __tablename__ = "sync_channels"

    id = Column(Integer, primary_key=True)

    discord_guild_id = Column(String(64), nullable=False)

    discord_channel_id = Column(String(64), nullable=False)

    line_group_id = Column(String(128), nullable=False)

    enabled = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ==========================================
# ループ防止
# ==========================================

class MessageCache(Base):
    __tablename__ = "message_cache"

    id = Column(Integer, primary_key=True)

    platform = Column(String(20))

    message_id = Column(String(200), unique=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ==========================================
# LINEグループ情報
# ==========================================

class LineGroup(Base):
    __tablename__ = "line_groups"

    id = Column(Integer, primary_key=True)

    group_id = Column(
        String(128),
        unique=True
    )

    group_name = Column(String(200))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ==========================================
# Discordチャンネル情報
# ==========================================

class DiscordChannel(Base):
    __tablename__ = "discord_channels"

    id = Column(Integer, primary_key=True)

    guild_id = Column(String(64))

    channel_id = Column(
        String(64),
        unique=True
    )

    channel_name = Column(String(200))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ==========================================
# Bot設定
# ==========================================

class BotSetting(Base):
    __tablename__ = "bot_settings"

    id = Column(Integer, primary_key=True)

    key = Column(
        String(100),
        unique=True
    )

    value = Column(Text)

# ==========================================
# エラーログ
# ==========================================

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True)

    platform = Column(String(30))

    error = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ==========================================
# Session
# ==========================================

def get_session():
    return SessionLocal()

# ==========================================
# 初期化
# ==========================================

def init_db():
    Base.metadata.create_all(engine)

# ==========================================
# Sync設定
# ==========================================

def add_sync_channel(
    guild_id: str,
    channel_id: str,
    group_id: str
):
    db = get_session()

    row = SyncChannel(
        discord_guild_id=guild_id,
        discord_channel_id=channel_id,
        line_group_id=group_id
    )

    db.add(row)
    db.commit()
    db.close()

def get_sync_channel(channel_id: str):
    db = get_session()

    row = (
        db.query(SyncChannel)
        .filter_by(
            discord_channel_id=channel_id,
            enabled=True
        )
        .first()
    )

    db.close()
    return row

# ==========================================
# Loop Prevention
# ==========================================

def message_exists(message_id: str):

    db = get_session()

    exists = (
        db.query(MessageCache)
        .filter_by(message_id=message_id)
        .first()
    )

    db.close()

    return exists is not None

def add_message(message_id: str, platform: str):

    db = get_session()

    db.add(
        MessageCache(
            message_id=message_id,
            platform=platform
        )
    )

    db.commit()
    db.close()

# ==========================================
# Settings
# ==========================================

def get_setting(key):

    db = get_session()

    row = (
        db.query(BotSetting)
        .filter_by(key=key)
        .first()
    )

    db.close()

    if row:
        return row.value

    return None

def set_setting(key, value):

    db = get_session()

    row = (
        db.query(BotSetting)
        .filter_by(key=key)
        .first()
    )

    if row:
        row.value = value

    else:
        db.add(
            BotSetting(
                key=key,
                value=value
            )
        )

    db.commit()
    db.close()

# ==========================================
# Error Log
# ==========================================

def log_error(platform, error):

    db = get_session()

    db.add(
        ErrorLog(
            platform=platform,
            error=str(error)
        )
    )

    db.commit()
    db.close()

# ==========================================
# Main
# ==========================================

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
