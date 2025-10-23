from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.DashboardSummaryView.as_view(), name='admin-dashboard-summary'),
    path('charts/', views.DashboardChartsView.as_view(), name='admin-dashboard-charts'),
    # Settings & Providers
    path('settings/providers/sports/', views.AdminSportsProviderView.as_view(), name='admin-sports-provider'),
    path('settings/providers/casino/', views.AdminCasinoProviderView.as_view(), name='admin-casino-provider'),
    # Finance
    path('finance/deposits/summary/', views.AdminDepositsSummaryView.as_view(), name='admin-deposits-summary'),
    path('finance/deposits/', views.AdminDepositsListView.as_view(), name='admin-deposits-list'),
    path('finance/withdrawals/summary/', views.AdminWithdrawalsSummaryView.as_view(), name='admin-withdrawals-summary'),
    path('finance/withdrawals/', views.AdminWithdrawalsListView.as_view(), name='admin-withdrawals-list'),
]
