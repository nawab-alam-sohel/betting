from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.casino.models import CasinoProvider, CasinoCategory, CasinoGame, CasinoSession
from apps.casino.api.serializers import (
    CasinoProviderSerializer,
    CasinoCategorySerializer,
    CasinoGameSerializer,
    LaunchGameSerializer,
)
from apps.casino.providers import generic as provider_generic


class ProviderListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        providers = CasinoProvider.objects.filter(active=True).order_by('display_order', 'name')
        return Response(CasinoProviderSerializer(providers, many=True).data)


class CategoryListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = CasinoCategory.objects.all().order_by('order', 'name')
        return Response(CasinoCategorySerializer(categories, many=True).data)


class GameListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        qs = CasinoGame.objects.filter(active=True).select_related('provider').prefetch_related('categories')
        q = request.query_params.get('q')
        provider = request.query_params.get('provider')
        category = request.query_params.get('category')
        letter = request.query_params.get('letter')  # A-Z filter
        ordering = request.query_params.get('ordering', 'name')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(slug__icontains=q))
        if provider:
            qs = qs.filter(provider__key=provider)
        if category:
            qs = qs.filter(categories__slug=category)
        if letter and len(letter) == 1:
            qs = qs.filter(name__istartswith=letter)
        if ordering:
            qs = qs.order_by(ordering)

        data = CasinoGameSerializer(qs[:500], many=True).data  # cap to 500 to avoid huge payloads
        return Response(data)


class LaunchGameView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        s = LaunchGameSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        game_id = s.validated_data['game_id']
        try:
            game = CasinoGame.objects.select_related('provider').get(id=game_id, active=True)
        except CasinoGame.DoesNotExist:
            return Response({'detail': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

        # Call provider adapter to create session / launch URL
        launch = provider_generic.create_session(game.provider, game, request.user)
        session = CasinoSession.objects.create(
            user=request.user,
            game=game,
            provider_session_id=launch.get('session_id', ''),
            launch_url=launch['launch_url'],
        )
        return Response({
            'session_id': session.id,
            'launch_url': session.launch_url,
        }, status=status.HTTP_201_CREATED)
