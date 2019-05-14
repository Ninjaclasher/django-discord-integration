from django.conf import settings
from django.utils.log import AdminEmailHandler


MESSAGE_LIMIT = getattr(settings, 'DISCORD_MESSAGE_LIMIT', 1000)


def escape(text):
    escape_chars = ('*', '_', '~', '`')
    for ch in escape_chars:
        text = text.replace(ch, '\\' + ch)
    return text


class DiscordMessageHandler(AdminEmailHandler):
    def emit(self, record):
        from discord_integration.models import DiscordIntegration

        data = DiscordIntegration.get_solo()

        if not data.webhook_url:
            return

        self.__level = record.levelname
        super().emit(record)

    def send_mail(self, subject, message, *args, **kwargs):
        from discord_integration.message import discord_message

        colors = {
            'ERROR': 0xe74c3c,
            'WARNING': 0xe78c3c,
            'INFO': 0xe7ec3c,
        }

        discord_message({
            'embeds': [{
                'title': escape(subject),
                'description': escape(message[:MESSAGE_LIMIT]),
                'color': colors.get(self.__level, 0xeee),
            }],
        })
