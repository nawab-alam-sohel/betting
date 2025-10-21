from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from apps.sports.models import Category, League, Team, Game, Market, Selection
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch sports data from third party API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            choices=['categories', 'leagues', 'games', 'odds', 'live'],
            required=True,
            help='Type of data to fetch'
        )

    def handle(self, *args, **options):
        fetch_type = options['type']
        api_key = settings.SPORTS_API_KEY
        base_url = settings.SPORTS_API_BASE_URL

        try:
            if fetch_type == 'categories':
                self.fetch_categories(base_url, api_key)
            elif fetch_type == 'leagues':
                self.fetch_leagues(base_url, api_key)
            elif fetch_type == 'games':
                self.fetch_games(base_url, api_key)
            elif fetch_type == 'odds':
                self.fetch_odds(base_url, api_key)
            elif fetch_type == 'live':
                self.fetch_live_data(base_url, api_key)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully fetched {fetch_type}')
            )
        except Exception as e:
            logger.error(f"Error fetching {fetch_type}: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'Error fetching {fetch_type}: {str(e)}')
            )

    def fetch_categories(self, base_url, api_key):
        """Fetch sports categories"""
        response = requests.get(
            f"{base_url}/sports",
            headers={'Authorization': f'Bearer {api_key}'}
        )
        response.raise_for_status()
        
        for sport in response.json():
            Category.objects.update_or_create(
                external_id=sport['id'],
                defaults={
                    'name': sport['name'],
                    'active': True
                }
            )

    def fetch_leagues(self, base_url, api_key):
        """Fetch leagues for each category"""
        for category in Category.objects.filter(active=True):
            response = requests.get(
                f"{base_url}/leagues",
                params={'sport_id': category.external_id},
                headers={'Authorization': f'Bearer {api_key}'}
            )
            response.raise_for_status()
            
            for league in response.json():
                League.objects.update_or_create(
                    external_id=league['id'],
                    defaults={
                        'name': league['name'],
                        'category': category,
                        'country': league.get('country', ''),
                        'active': True
                    }
                )

    def fetch_games(self, base_url, api_key):
        """Fetch upcoming games"""
        # Fetch games for next 7 days
        start_date = timezone.now()
        end_date = start_date + timedelta(days=7)
        
        for league in League.objects.filter(active=True):
            response = requests.get(
                f"{base_url}/fixtures",
                params={
                    'league_id': league.external_id,
                    'from': start_date.date().isoformat(),
                    'to': end_date.date().isoformat()
                },
                headers={'Authorization': f'Bearer {api_key}'}
            )
            response.raise_for_status()
            
            for game in response.json():
                # Create or update teams
                home_team, _ = Team.objects.get_or_create(
                    external_id=game['home_team']['id'],
                    defaults={'name': game['home_team']['name']}
                )
                away_team, _ = Team.objects.get_or_create(
                    external_id=game['away_team']['id'],
                    defaults={'name': game['away_team']['name']}
                )
                
                # Create or update game
                Game.objects.update_or_create(
                    external_id=game['id'],
                    defaults={
                        'league': league,
                        'home_team': home_team,
                        'away_team': away_team,
                        'start_time': game['start_time'],
                        'status': 'scheduled'
                    }
                )

    def fetch_odds(self, base_url, api_key):
        """Fetch odds for upcoming games"""
        for game in Game.objects.filter(
            status='scheduled',
            start_time__gte=timezone.now(),
            start_time__lte=timezone.now() + timedelta(days=2)
        ):
            response = requests.get(
                f"{base_url}/odds/{game.external_id}",
                headers={'Authorization': f'Bearer {api_key}'}
            )
            response.raise_for_status()
            
            for market_data in response.json():
                market, _ = Market.objects.update_or_create(
                    game=game,
                    external_id=market_data['id'],
                    defaults={
                        'market_type': market_data['type'],
                        'name': market_data['name'],
                        'status': 'active',
                        'specifier': market_data.get('specifier')
                    }
                )
                
                for selection_data in market_data['selections']:
                    Selection.objects.update_or_create(
                        market=market,
                        external_id=selection_data['id'],
                        defaults={
                            'name': selection_data['name'],
                            'odds': selection_data['odds'],
                            'status': 'active'
                        }
                    )

    def fetch_live_data(self, base_url, api_key):
        """Fetch live game data and odds"""
        response = requests.get(
            f"{base_url}/live",
            headers={'Authorization': f'Bearer {api_key}'}
        )
        response.raise_for_status()
        
        for live_game in response.json():
            try:
                game = Game.objects.get(external_id=live_game['id'])
                game.status = 'live'
                game.score_home = live_game.get('score_home')
                game.score_away = live_game.get('score_away')
                game.save()
                
                # Update live odds
                for market_data in live_game['markets']:
                    market = Market.objects.get(
                        game=game,
                        external_id=market_data['id']
                    )
                    market.status = market_data['status']
                    market.save()
                    
                    for selection_data in market_data['selections']:
                        selection = Selection.objects.get(
                            market=market,
                            external_id=selection_data['id']
                        )
                        selection.odds = selection_data['odds']
                        selection.status = selection_data['status']
                        selection.save()
                        
            except Game.DoesNotExist:
                logger.warning(f"Live game not found: {live_game['id']}")
            except Exception as e:
                logger.error(f"Error updating live game {live_game['id']}: {str(e)}")