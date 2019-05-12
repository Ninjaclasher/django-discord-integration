# Django Discord Integration

Discord integration for Django, supporting error reporting via webhooks.

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
