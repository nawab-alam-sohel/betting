from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, LeagueViewSet, GameViewSet,
    MarketViewSet, BetSlipValidationView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'games', GameViewSet, basename='game')
router.register(r'markets', MarketViewSet, basename='market')
router.register(r'validate-betslip', BetSlipValidationView, basename='betslip-validation')

urlpatterns = [
    path('', include(router.urls)),
]