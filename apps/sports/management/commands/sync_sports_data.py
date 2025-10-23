from django.core.management.base import BaseCommand
from apps.sports.providers.generic import sync_sports


class Command(BaseCommand):
    help = "Sync sports data from provider into local DB (DEMO or REAL based on SPORTS_USE_DEMO)."

    def add_arguments(self, parser):
        parser.add_argument('--provider', required=True, help='Provider key (configured via configure_sports_provider)')

    def handle(self, *args, **options):
        provider_key = options['provider']
        sync_sports(provider_key)
        self.stdout.write(self.style.SUCCESS(f"Sports sync completed for provider '{provider_key}'."))
