
from sync_service import send_discord_to_line

send_discord_to_line(
    message_id=str(message.id),
    group_id=sync.line_group_id,
    author=message.author.display_name,
    content=message.content
)
