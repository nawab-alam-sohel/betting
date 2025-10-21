from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.payments.api import views
from apps.payments.api import views_recon

router = DefaultRouter()
router.register(r'reconciliation/batches', views_recon.ReconciliationBatchViewSet)
router.register(r'reconciliation/items', views_recon.ReconciliationItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('initiate/', views.InitiatePaymentView.as_view(), name='payment-initiate'),
    path('webhook/<str:provider>/', views.WebhookView.as_view(), name='payment-webhook'),
    # reconciliation endpoints
    path('providers/', views_recon.PaymentProviderListView.as_view(), name='payment-providers'),
    path('withdrawals/', views_recon.CreateWithdrawalRequestView.as_view(), name='withdrawal-create'),
    path('withdrawals/<int:pk>/<str:action>/', views_recon.AdminWithdrawalActionView.as_view(), name='withdrawal-action'),
]
