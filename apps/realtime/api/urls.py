from django.urls import path
from .views import RealtimeHealthView

urlpatterns = [
    path('health/', RealtimeHealthView.as_view(), name='realtime-health'),
]
