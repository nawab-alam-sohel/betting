from rest_framework import serializers
from apps.sports.models import Category, League, Team, Game, Market, Selection


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'slug', 'logo']


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name', 'odds', 'american_odds', 'status']


class MarketSerializer(serializers.ModelSerializer):
    selections = SelectionSerializer(many=True, read_only=True)

    class Meta:
        model = Market
        fields = ['id', 'market_type', 'name', 'status', 'selections', 'specifier']


class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    markets = MarketSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            'id', 'home_team', 'away_team', 'start_time', 'status',
            'score_home', 'score_away', 'markets'
        ]


class LeagueSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ['id', 'name', 'slug', 'logo', 'country', 'games']


class CategorySerializer(serializers.ModelSerializer):
    leagues = LeagueSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'leagues']