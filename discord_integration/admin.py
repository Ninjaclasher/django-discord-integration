from django.contrib import admin

from discord_integration.models import DiscordIntegration


class DiscordIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(DiscordIntegration, DiscordIntegrationAdmin)
