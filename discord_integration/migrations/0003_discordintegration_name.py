# Generated by Django 3.2.6 on 2022-03-13 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_integration', '0002_auto_20200412_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordintegration',
            name='name',
            field=models.CharField(default='default', help_text='The name to specify as a keyword argument in the Django logging settings.', max_length=30, unique=True, verbose_name='logger name'),
        ),
    ]
