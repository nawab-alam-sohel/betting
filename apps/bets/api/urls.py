from django.urls import path
from .views import PlaceBetView, MyBetsView, QuoteBetView

urlpatterns = [
    path('place/', PlaceBetView.as_view(), name='place-bet'),
    path('quote/', QuoteBetView.as_view(), name='quote-bet'),
    path('me/', MyBetsView.as_view(), name='my-bets'),
]
