from django.urls import path
from .views import ReconHealthView

urlpatterns = [
    path('health/', ReconHealthView.as_view(), name='reconciliation-health'),
]
