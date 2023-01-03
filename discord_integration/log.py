import json
import traceback
from logging import LogRecord
from typing import Any, Dict, Optional
from urllib import request

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.log import AdminEmailHandler
from urllib3 import encode_multipart_formdata

__all__ = ['DiscordMessageHandler', 'SimpleDiscordMessageHandler']


MESSAGE_LIMIT: int = getattr(settings, 'DISCORD_MESSAGE_LIMIT', 1000)
BOT_USERNAME: Optional[str] = getattr(settings, 'DISCORD_BOT_USERNAME', None)
AVATAR_URL: Optional[str] = getattr(settings, 'DISCORD_AVATAR_URL', None)

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

    def message(self, message: Dict[str, Any], full_message: Optional[str] = None) -> None:
        if self.model is None:
            raise ImproperlyConfigured('Discord integration model does not exist.')

        username = self.model.bot_name or BOT_USERNAME
        if username and 'username' not in message:
            message['username'] = username

        avatar_url = self.model.avatar_url or AVATAR_URL
        if avatar_url and 'avatar_url' not in message:
            message['avatar_url'] = avatar_url

        files = []
        if full_message is not None:
            files.append(('full_message.txt', full_message, 'text/plain'))

        data = {
            'payload_json': ('', json.dumps(message), 'application/json'),
        }
        for i, file in enumerate(files):
            data['files[{}]'.format(i)] = file

        body, header = encode_multipart_formdata(data)

        req = request.Request(
            self.model.webhook_url,
            data=body,
            headers={'User-Agent': 'Python/3', 'Content-Type': header},
        )
        request.urlopen(req)

    @staticmethod
    def escape(text: str) -> str:
        escape_chars = ('*', '_', '~', '`', '|')
        for ch in escape_chars:
            text = text.replace(ch, '\\' + ch)
        return text

    @staticmethod
    def format_codeblock(text: str, language: str = '') -> str:
        return '```{}\n{}\n```'.format(language, text)


class DiscordMessageHandler(AdminEmailHandler):
    def __init__(self, model_name: str = 'default', **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.model_name = model_name

    def emit(self, record: LogRecord) -> None:
        self.__level = record.levelname
        ei = record.exc_info
        self.__traceback = ''.join(traceback.format_exception(*ei)) if ei is not None else record.getMessage()
        return super().emit(record)

    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        webhook = DiscordWebhook(self.model_name)

        webhook.message(
            {
                'embeds': [{
                    'title': webhook.escape(subject),
                    'description': webhook.format_codeblock(self.__traceback[:MESSAGE_LIMIT], 'py'),
                    'color': COLORS.get(self.__level, 0xeee),
                }],
            },
            full_message=message,
        )


class SimpleDiscordMessageHandler(DiscordMessageHandler):
    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        super().send_mail(subject, '', *args, **kwargs)
