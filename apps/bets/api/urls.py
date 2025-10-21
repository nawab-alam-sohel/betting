from django.urls import path
from .views import PlaceBetView, MyBetsView

urlpatterns = [
    path('place/', PlaceBetView.as_view(), name='place-bet'),
    path('me/', MyBetsView.as_view(), name='my-bets'),
]
