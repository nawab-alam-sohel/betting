from django.urls import path
from apps.casino.api.views import ProviderListView, CategoryListView, GameListView, LaunchGameView

urlpatterns = [
    path('providers/', ProviderListView.as_view(), name='casino-providers'),
    path('categories/', CategoryListView.as_view(), name='casino-categories'),
    path('games/', GameListView.as_view(), name='casino-games'),
    path('launch/', LaunchGameView.as_view(), name='casino-launch'),
]
