from django.urls import path
from .views import RiskHealthView

urlpatterns = [
    path('health/', RiskHealthView.as_view(), name='riskengine-health'),
]
