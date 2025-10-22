from django.urls import path
from .views import ReportsHealthView

urlpatterns = [
    path('health/', ReportsHealthView.as_view(), name='reports-health'),
]
