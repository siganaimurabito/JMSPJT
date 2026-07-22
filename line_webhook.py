from sync_service import (
    send_line_to_discord_threadsafe
)

send_line_to_discord_threadsafe(
    discord_client=discord_client,
    message_id=event.message.id,
    channel_id=row.discord_channel_id,
    sender_name=event.source.user_id,
    content=event.message.text,
)
