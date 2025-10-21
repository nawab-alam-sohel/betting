from django.contrib import admin
from django.utils.html import format_html
from .models import Category, League, Team, Game, Market, Selection


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'active', 'order')
    list_editable = ('active', 'order')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def display_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="30" height="30" />', obj.icon.url)
        return '-'
    display_icon.short_description = 'Icon'


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo', 'category', 'country', 'active', 'priority')
    list_filter = ('category', 'active', 'country')
    list_editable = ('active', 'priority')
    search_fields = ('name', 'country')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['make_active', 'make_inactive']

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="30" height="30" />', obj.logo.url)
        return '-'
    display_logo.short_description = 'Logo'

    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Mark selected leagues as active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected leagues as inactive"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo')
    search_fields = ('name',)
    filter_horizontal = ('leagues',)
    prepopulated_fields = {'slug': ('name',)}

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="30" height="30" />', obj.logo.url)
        return '-'
    display_logo.short_description = 'Logo'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'league', 'start_time', 'status', 'score_display')
    list_filter = ('status', 'league__category', 'league', 'start_time')
    search_fields = ('home_team__name', 'away_team__name', 'league__name')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['close_for_betting', 'mark_as_ended', 'mark_as_cancelled']
    ordering = ('-start_time',)

    def score_display(self, obj):
        if obj.score_home is not None and obj.score_away is not None:
            return f"{obj.score_home} - {obj.score_away}"
        return "-"
    score_display.short_description = "Score"

    def close_for_betting(self, request, queryset):
        queryset.update(status='closed')
    close_for_betting.short_description = "Close selected games for betting"

    def mark_as_ended(self, request, queryset):
        queryset.update(status='ended')
    mark_as_ended.short_description = "Mark selected games as ended"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected games as cancelled"


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'market_type', 'name', 'status', 'priority')
    list_filter = ('status', 'market_type', 'game__league__category')
    search_fields = ('game__home_team__name', 'game__away_team__name')
    readonly_fields = ('external_id',)
    actions = ['suspend_markets', 'activate_markets', 'cancel_markets']
    ordering = ('-game__start_time', 'priority')

    def suspend_markets(self, request, queryset):
        queryset.update(status='suspended')
    suspend_markets.short_description = "Suspend selected markets"

    def activate_markets(self, request, queryset):
        queryset.update(status='active')
    activate_markets.short_description = "Activate selected markets"

    def cancel_markets(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_markets.short_description = "Cancel selected markets"


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'market', 'name', 'odds', 'american_odds', 'status')
    list_filter = ('status', 'market__market_type', 'market__game__league__category')
    search_fields = ('name', 'market__game__home_team__name', 'market__game__away_team__name')
    readonly_fields = ('american_odds', 'external_id')
    actions = ['mark_as_won', 'mark_as_lost', 'suspend_selections', 'activate_selections']
    ordering = ('-market__game__start_time',)

    def mark_as_won(self, request, queryset):
        queryset.update(status='won', result='won')
    mark_as_won.short_description = "Mark selected selections as won"

    def mark_as_lost(self, request, queryset):
        queryset.update(status='lost', result='lost')
    mark_as_lost.short_description = "Mark selected selections as lost"

    def suspend_selections(self, request, queryset):
        queryset.update(status='suspended')
    suspend_selections.short_description = "Suspend selected selections"

    def activate_selections(self, request, queryset):
        queryset.update(status='active')
    activate_selections.short_description = "Activate selected selections"