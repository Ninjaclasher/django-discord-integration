import json
from typing import Any, Dict
from urllib import request

from django.core.exceptions import ImproperlyConfigured

from discord_integration.models import DiscordIntegration

__all__ = ['discord_message']


def discord_message(message: Dict[str, Any]) -> None:
    data = DiscordIntegration.get_solo()

    if not data.webhook_url:
        raise ImproperlyConfigured('Discord Webhook URL is not configured')

    if data.bot_name and 'username' not in message:
        message['username'] = data.bot_name

    if data.avatar_url and 'avatar_url' not in message:
        message['avatar_url'] = data.avatar_url

    request.urlopen(
        request.Request(
            data.webhook_url,
            data=json.dumps(message).encode('utf-8'),
            headers={'User-Agent': 'Python/3', 'Content-Type': 'application/json'},
        ),
    )
