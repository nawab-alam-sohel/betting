from django.core.management.base import BaseCommand
from apps.sports.models import SportsProvider


class Command(BaseCommand):
    help = "Create or update a sports provider with base_url and config (api_key, secret, etc.)"

    def add_arguments(self, parser):
        parser.add_argument('--key', required=True, help='Provider key (slug)')
        parser.add_argument('--name', required=False, help='Display name')
        parser.add_argument('--base-url', required=False, help='Provider API base URL')
        parser.add_argument('--api-key', required=False, help='API key credential')
        parser.add_argument('--secret', required=False, help='Secret credential')
        parser.add_argument('--active', required=False, default='1', help='Active flag 1/0 (default 1)')

    def handle(self, *args, **options):
        key = options['key']
        name = options.get('name') or key.title()
        base_url = options.get('base_url') or ''
        api_key = options.get('api_key')
        secret = options.get('secret')
        active = options.get('active', '1') == '1'

        provider, _ = SportsProvider.objects.get_or_create(key=key, defaults={
            'name': name,
            'base_url': base_url,
            'active': active,
        })

        provider.name = name
        provider.base_url = base_url
        provider.active = active

        cfg = provider.config or {}
        if api_key is not None:
            cfg['api_key'] = api_key
        if secret is not None:
            cfg['secret'] = secret
        provider.config = cfg
        provider.save()

        self.stdout.write(self.style.SUCCESS(
            f"Sports provider '{provider.key}' configured. Active={provider.active} BaseURL='{provider.base_url}'"
        ))
