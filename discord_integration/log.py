import json
from logging import LogRecord
from typing import Any, Dict, Optional
from urllib import request

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.log import AdminEmailHandler

__all__ = ['DiscordMessageHandler', 'SimpleDiscordMessageHandler']


MESSAGE_LIMIT: int = getattr(settings, 'DISCORD_MESSAGE_LIMIT', 1000)

COLORS: Dict[str, int] = getattr(settings, 'DISCORD_COLORS', {
    'ERROR': 0xe74c3c,
    'WARNING': 0xe78c3c,
    'INFO': 0xe7ec3c,
})


class DiscordWebhook:
    def __init__(self, model_name: str) -> None:
        from discord_integration.models import DiscordIntegration

        self.model: Optional[DiscordIntegration]
        try:
            self.model = DiscordIntegration.objects.get(name=model_name)
        except DiscordIntegration.DoesNotExist:
            self.model = None

    def message(self, message: Dict[str, Any]) -> None:
        if self.model is None:
            raise ImproperlyConfigured('Discord integration model does not exist.')

        if self.model.bot_name and 'username' not in message:
            message['username'] = self.model.bot_name

        if self.model.avatar_url and 'avatar_url' not in message:
            message['avatar_url'] = self.model.avatar_url

        req = request.Request(
            self.model.webhook_url,
            data=json.dumps(message).encode('utf-8'),
            headers={'User-Agent': 'Python/3', 'Content-Type': 'application/json'},
        )
        request.urlopen(req)

    @staticmethod
    def escape(text: str) -> str:
        escape_chars = ('*', '_', '~', '`', '|')
        for ch in escape_chars:
            text = text.replace(ch, '\\' + ch)
        return text


class DiscordMessageHandler(AdminEmailHandler):
    def __init__(self, model_name: str = 'default', **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.model_name = model_name

    def emit(self, record: LogRecord) -> None:
        self.__level = record.levelname
        return super().emit(record)

    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        webhook = DiscordWebhook(self.model_name)

        webhook.message({
            'embeds': [{
                'title': webhook.escape(subject),
                'description': webhook.escape(message[:MESSAGE_LIMIT]),
                'color': COLORS.get(self.__level, 0xeee),
            }],
        })


class SimpleDiscordMessageHandler(DiscordMessageHandler):
    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        super().send_mail(subject, '', *args, **kwargs)
