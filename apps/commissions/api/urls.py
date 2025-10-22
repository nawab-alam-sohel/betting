from django.urls import path
from .views import CommissionHealthView

urlpatterns = [
    path('health/', CommissionHealthView.as_view(), name='commissions-health'),
]
