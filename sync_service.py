# sync_service.py

import asyncio
import discord

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

from config import (
    LINE_CHANNEL_ACCESS_TOKEN,
)

from database import (
    add_message,
    message_exists,
    log_error,
)

# ==========================================
# LINE API
# ==========================================

line_config = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)

# ==========================================
# Discord → LINE
# ==========================================

def send_discord_to_line(
    message_id: str,
    group_id: str,
    author: str,
    content: str,
):
    try:

        if message_exists(message_id):
            return

        text = f"{author}\n{content}"

        with ApiClient(line_config) as api_client:

            api = MessagingApi(api_client)

            api.push_message(
                PushMessageRequest(
                    to=group_id,
                    messages=[
                        TextMessage(text=text)
                    ]
                )
            )

        add_message(
            message_id=message_id,
            platform="discord"
        )

    except Exception as e:

        log_error(
            "discord_to_line",
            e
        )

# ==========================================
# LINE → Discord
# ==========================================

async def send_line_to_discord(
    discord_client: discord.Client,
    message_id: str,
    channel_id: str,
    sender_name: str,
    content: str,
):
    try:

        if message_exists(message_id):
            return

        channel = discord_client.get_channel(
            int(channel_id)
        )

        if channel is None:
            return

        await channel.send(
            f"[LINE] {sender_name}\n{content}"
        )

        add_message(
            message_id=message_id,
            platform="line"
        )

    except Exception as e:

        log_error(
            "line_to_discord",
            e
        )

# ==========================================
# Thread Safe Wrapper
# ==========================================

def send_line_to_discord_threadsafe(
    discord_client: discord.Client,
    message_id: str,
    channel_id: str,
    sender_name: str,
    content: str,
):

    future = asyncio.run_coroutine_threadsafe(
        send_line_to_discord(
            discord_client,
            message_id,
            channel_id,
            sender_name,
            content,
        ),
        discord_client.loop
    )

    return future

# ==========================================
# Attachment Formatter
# ==========================================

def format_attachment_message(
    sender: str,
    file_type: str,
    url: str,
):

    return (
        f"{sender}\n"
        f"[{file_type}]\n"
        f"{url}"
    )

# ==========================================
# Utility
# ==========================================

def make_discord_text(
    author: str,
    content: str,
):

    return f"{author}\n{content}"


def make_line_text(
    author: str,
    content: str,
):

    return f"{author}\n{content}"
