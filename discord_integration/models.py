from django.db import models
from django.utils.translation import gettext_lazy as _


class DiscordIntegration(models.Model):
    name: models.CharField = models.CharField(
        max_length=30,
        unique=True,
        default='default',
        verbose_name=_('logger name'),
        help_text=_('The name to specify as a keyword argument in the Django logging settings.'),
    )
    bot_name: models.CharField = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_('discord bot username'),
        help_text=_('Override the bot username set in the Discord settings.'),
    )
    avatar_url: models.URLField = models.URLField(
        blank=True,
        verbose_name=_('discord bot avatar'),
        help_text=_('Override the bot avatar set in the Discord settings.'),
    )
    webhook_url: models.URLField = models.URLField(
        verbose_name=_('discord webhook url'),
        help_text=_('The Discord webhook url found in the Discord settings.'),
    )

    def __str__(self) -> str:
        return self.name
