from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import Role
from apps.sports.models import Category, League, Team, Game, Market, Selection


class Command(BaseCommand):
    help = "Seed demo roles and sports data for development"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding roles..."))
        roles = [
            ("Super Admin", "superadmin", 100),
            ("Admin", "admin", 90),
            ("Agent", "agent", 50),
            ("User", "user", 10),
        ]
        for name, slug, level in roles:
            Role.objects.get_or_create(slug=slug, defaults={"name": name, "level": level})

        self.stdout.write(self.style.NOTICE("Seeding sports data..."))
        football, _ = Category.objects.get_or_create(name="Football", defaults={"order": 1})
        league, _ = League.objects.get_or_create(
            category=football,
            name="Premier League",
            defaults={"country": "UK", "priority": 10},
        )
        team_a, _ = Team.objects.get_or_create(name="Team A")
        team_b, _ = Team.objects.get_or_create(name="Team B")
        team_a.leagues.add(league)
        team_b.leagues.add(league)

        start = timezone.now() + timedelta(days=1)
        game, _ = Game.objects.get_or_create(
            league=league,
            home_team=team_a,
            away_team=team_b,
            start_time=start,
            defaults={"status": "scheduled"},
        )

        market, _ = Market.objects.get_or_create(
            game=game,
            market_type="1x2",
            name="Full Time Result",
            defaults={"status": "active", "priority": 1},
        )
        Selection.objects.get_or_create(market=market, name="Home", defaults={"odds": 1.85})
        Selection.objects.get_or_create(market=market, name="Draw", defaults={"odds": 3.40})
        Selection.objects.get_or_create(market=market, name="Away", defaults={"odds": 4.20})

        self.stdout.write(self.style.SUCCESS("Seed complete."))
