from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class DiscordIntegration(SingletonModel):
    bot_name = models.CharField(max_length=30, blank=True,
                                verbose_name=_('discord bot username'),
                                help_text=_('Override the bot username set in '
                                            'the Discord settings.'))
    avatar_url = models.URLField(blank=True,
                                 verbose_name=_('discord bot avatar'),
                                 help_text=_('Override the bot avatar set in '
                                             'the Discord settings'))
    webhook_url = models.URLField(verbose_name=_('discord webhook url'),
                                  help_text=_('The Discord webhook url found '
                                              'in the Discord settings'))
