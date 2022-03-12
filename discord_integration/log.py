from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from logging import LogRecord

from django.conf import settings
from django.utils.log import AdminEmailHandler

__all__ = ['DiscordMessageHandler', 'SimpleDiscordMessageHandler']


MESSAGE_LIMIT: int = getattr(settings, 'DISCORD_MESSAGE_LIMIT', 1000)

COLORS: Dict[str, int] = getattr(settings, 'DISCORD_COLORS', {
    'ERROR': 0xe74c3c,
    'WARNING': 0xe78c3c,
    'INFO': 0xe7ec3c,
})


def escape(text: str) -> str:
    escape_chars = ('*', '_', '~', '`', '|')
    for ch in escape_chars:
        text = text.replace(ch, '\\' + ch)
    return text


class DiscordMessageHandler(AdminEmailHandler):
    def emit(self, record: LogRecord) -> None:
        from discord_integration.models import DiscordIntegration

        data = DiscordIntegration.get_solo()

        if not data.webhook_url:
            return

        self.__level = record.levelname
        return super().emit(record)

    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        from discord_integration.message import discord_message

        discord_message({
            'embeds': [{
                'title': escape(subject),
                'description': escape(message[:MESSAGE_LIMIT]),
                'color': COLORS.get(self.__level, 0xeee),
            }],
        })


class SimpleDiscordMessageHandler(DiscordMessageHandler):
    def send_mail(self, subject: str, message: str, *args: Any, **kwargs: Any) -> None:
        super().send_mail(subject, '', *args, **kwargs)
