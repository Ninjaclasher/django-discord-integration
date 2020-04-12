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
    'solo',
    ...
)
```

Next, migrate the database:
```
$ python manage.py migrate
```

Finally, set the Discord webhook URL in the Django admin, as well as the bot username and avatar URL if necessary.


## Sample Logging Configuration

```python
LOGGING = {
    'handlers': {
        'discord_integration': {
            'level': 'ERROR',
            'class': 'discord_integration.log.DiscordMessageHandler',
        },
    },
    'loggers': {
        'handlers': ['discord_integration'],
    },
}
```
