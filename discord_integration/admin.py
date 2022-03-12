from django.contrib import admin
from solo.admin import SingletonModelAdmin  # type: ignore

from discord_integration.models import DiscordIntegration


class DiscordIntegrationAdmin(SingletonModelAdmin):
    exclude = ()


admin.site.register(DiscordIntegration, DiscordIntegrationAdmin)
