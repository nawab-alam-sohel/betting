from django.urls import path
from .views import WalletView, DepositView, TransactionsView

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('deposit/', DepositView.as_view(), name='wallet-deposit'),
    path('transactions/', TransactionsView.as_view(), name='wallet-transactions'),
]
