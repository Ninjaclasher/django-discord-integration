# Django Discord Integration

Discord integration for Django, supporting error reporting via webhooks.

This app comes with two message handlers: `DiscordMessageHandler` and `SimpleDiscordMessageHandler`. `DiscordMessageHandler` sends all the information related to the message, such as a traceback if there is one, while the `SimpleDiscordMessageHandler` only sends the title.

## Installation
```bash
$ pip install django-discord-integration
```

In your `settings.py`, add the following:
```python
INSTALLED_APPS = (
    'discord_integration',
    ...
)
```

Next, migrate the database:
```
$ python manage.py migrate
```

Finally, create a Discord integration object in the Django admin site. Set the Discord webhook URL as well as the bot username and avatar URL if necessary. You can create multiple objects to direct different logs to different channels. The default object should the name `default`.


## Sample Logging Configuration

```python
LOGGING = {
    'handlers': {
        'discord_integration': {
            'level': 'ERROR',
            'class': 'discord_integration.log.DiscordMessageHandler',
            'model_name': 'default',  # OPTIONAL: specify a name to use a different integration configuration.
        },
    },
    'loggers': {
        'handlers': ['discord_integration'],
    },
}
```
