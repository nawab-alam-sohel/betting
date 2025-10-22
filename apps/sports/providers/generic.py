import os
import random
from datetime import datetime, timedelta
from django.utils import timezone
from apps.sports.models import Category, League, Team, Game, Market, Selection, SportsProvider


def sync_demo(provider: SportsProvider):
    """Populate a minimal demo catalog for sportsbook (football)."""
    football, _ = Category.objects.get_or_create(name="Football", defaults={"order": 1})
    league, _ = League.objects.get_or_create(category=football, name="Demo League", defaults={"country": "BD"})
    team_a, _ = Team.objects.get_or_create(name="Dhaka FC")
    team_b, _ = Team.objects.get_or_create(name="Chittagong United")
    start = timezone.now() + timedelta(hours=2)
    game, _ = Game.objects.get_or_create(league=league, home_team=team_a, away_team=team_b, start_time=start)

    # Create a simple 1X2 market
    m1, _ = Market.objects.get_or_create(game=game, market_type='1x2', defaults={
        'name': 'Full Time Result',
        'status': 'active',
        'priority': 1,
    })
    Selection.objects.get_or_create(market=m1, name='Home', defaults={'odds': 1.80, 'status': 'active'})
    Selection.objects.get_or_create(market=m1, name='Draw', defaults={'odds': 3.20, 'status': 'active'})
    Selection.objects.get_or_create(market=m1, name='Away', defaults={'odds': 4.50, 'status': 'active'})


def sync_real(provider: SportsProvider):
    """Scaffold for real provider sync. Implement HTTP calls and DB upserts here."""
    # Example pseudo-implementation:
    # import requests
    # api_key = provider.config.get('api_key')
    # base = provider.base_url.rstrip('/')
    # headers = {'Authorization': f'Bearer {api_key}'}
    # leagues = requests.get(f"{base}/v1/leagues", headers=headers, timeout=15).json()
    # for l in leagues:
    #     league, _ = League.objects.update_or_create(
    #         external_id=l['id'],
    #         defaults={'name': l['name'], 'category': category, 'country': l['country']}
    #     )
    # ... similar for teams/games/markets/selections ...
    pass


def sync_sports(provider_key: str):
    provider = SportsProvider.objects.get(key=provider_key)
    use_demo = os.getenv('SPORTS_USE_DEMO', '1') == '1'
    if use_demo:
        sync_demo(provider)
    else:
        sync_real(provider)
