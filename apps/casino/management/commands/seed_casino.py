from django.core.management.base import BaseCommand

from apps.casino.models import CasinoProvider, CasinoCategory, CasinoGame


class Command(BaseCommand):
    help = "Seed minimal casino providers, categories, and games for demo/testing"

    def handle(self, *args, **options):
        provider, _ = CasinoProvider.objects.get_or_create(
            key="generic",
            defaults={"name": "Generic Provider", "display_order": 1},
        )

        slots, _ = CasinoCategory.objects.get_or_create(slug="slots", defaults={"name": "Slots", "order": 1})
        table, _ = CasinoCategory.objects.get_or_create(slug="table", defaults={"name": "Table", "order": 2})

        g1, _ = CasinoGame.objects.get_or_create(
            provider=provider,
            provider_game_id="GEN-SLOTS-001",
            defaults={
                "name": "A-Mystic Slots",
                "slug": "a-mystic-slots",
                "thumbnail_url": "https://via.placeholder.com/256x256.png?text=Mystic+Slots",
                "active": True,
            },
        )
        g1.categories.add(slots)

        g2, _ = CasinoGame.objects.get_or_create(
            provider=provider,
            provider_game_id="GEN-TABLE-001",
            defaults={
                "name": "Blackjack Classic",
                "slug": "blackjack-classic",
                "thumbnail_url": "https://via.placeholder.com/256x256.png?text=Blackjack",
                "active": True,
            },
        )
        g2.categories.add(table)

        self.stdout.write(self.style.SUCCESS("Casino seed completed."))
