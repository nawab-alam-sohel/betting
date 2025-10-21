from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from ..models import Category, League, Game, Market, Selection
from .serializers import (
    CategorySerializer, LeagueSerializer, GameSerializer,
    MarketSerializer, SelectionSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeagueSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['priority', 'name']
    ordering = ['-priority', 'name']

    def get_queryset(self):
        queryset = League.objects.filter(active=True)
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_time']
    ordering = ['start_time']

    def get_queryset(self):
        now = timezone.now()
        queryset = Game.objects.filter(
            Q(status='scheduled') | Q(status='live'),
            start_time__gte=now - timedelta(hours=2)
        ).select_related('home_team', 'away_team', 'league')

        category_id = self.request.query_params.get('category', None)
        league_id = self.request.query_params.get('league', None)
        status = self.request.query_params.get('status', None)

        if category_id:
            queryset = queryset.filter(league__category_id=category_id)
        if league_id:
            queryset = queryset.filter(league_id=league_id)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    @action(detail=False)
    def live(self, request):
        games = Game.objects.filter(status='live')\
            .select_related('home_team', 'away_team', 'league')
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def upcoming(self, request):
        now = timezone.now()
        games = Game.objects.filter(
            status='scheduled',
            start_time__gte=now,
            start_time__lte=now + timedelta(days=2)
        ).select_related('home_team', 'away_team', 'league')
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)


class MarketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MarketSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Market.objects.filter(status='active')\
            .select_related('game')\
            .prefetch_related('selections')


class BetSlipValidationView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        selections = request.data.get('selections', [])
        validation_results = []

        for selection in selections:
            try:
                sel = Selection.objects.get(id=selection['id'])
                current_odds = sel.odds
                submitted_odds = selection.get('odds')

                validation_results.append({
                    'id': sel.id,
                    'valid': (
                        sel.status == 'active' and
                        sel.market.status == 'active' and
                        sel.market.game.status in ['scheduled', 'live'] and
                        float(current_odds) == float(submitted_odds)
                    ),
                    'current_odds': current_odds,
                    'reason': self._get_validation_reason(sel, submitted_odds)
                })
            except Selection.DoesNotExist:
                validation_results.append({
                    'id': selection['id'],
                    'valid': False,
                    'reason': 'Selection not found'
                })

        return Response(validation_results)

    def _get_validation_reason(self, selection, submitted_odds):
        if selection.status != 'active':
            return 'Selection is not active'
        if selection.market.status != 'active':
            return 'Market is not active'
        if selection.market.game.status not in ['scheduled', 'live']:
            return 'Game is not available for betting'
        if float(selection.odds) != float(submitted_odds):
            return 'Odds have changed'
        return None