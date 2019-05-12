import datetime
import json

import requests

from django.core.exceptions import ImproperlyConfigured

from discord_integration.models import DiscordIntegration

__all__ = ['discord_message']


def timestamp():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) \
                            .replace(microsecond=0).isoformat()


def discord_message(message):
    data = DiscordIntegration.get_solo()

    if not data.webhook_url:
        return ImproperlyConfigured('Discord Webhook URL is not configured')

    if data.bot_name and 'username' not in message:
        message['username'] = data.bot_name

    if data.avatar_url and 'avatar_url' not in message:
        message['avatar_url'] = data.avatar_url

    if 'timestamp' not in message:
        message['timestamp'] = timestamp()

    requests.post(data.webhook_url, data=json.dumps(message),
                  headers={'Content-Type': 'application/json'})
