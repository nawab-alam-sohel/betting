from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'


def ready(self):
        # Import signals so they register
        import apps.users.signals  # noqa