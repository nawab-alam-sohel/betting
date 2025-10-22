from django.contrib import admin
from .models import Bet, BetLine


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_stake_cents', 'potential_win_cents', 'status', 'result', 'placed_at')
    list_filter = ('status', 'result')


@admin.register(BetLine)
class BetLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'bet', 'selection', 'odds', 'stake_cents')
