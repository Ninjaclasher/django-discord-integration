from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiscordIntegrationConfig(AppConfig):
    name = 'discord_integration'
    verbose_name = _('Discord Integration')
