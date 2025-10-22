from celery import shared_task
from django.core.management import call_command

@shared_task
def fetch_sports_games_task():
    call_command('fetch_sports_data', '--type', 'games')

@shared_task
def fetch_sports_odds_task():
    call_command('fetch_sports_data', '--type', 'odds')

@shared_task
def fetch_sports_live_task():
    call_command('fetch_sports_data', '--type', 'live')
