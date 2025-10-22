from django.urls import path
from .views import JobsHealthView

urlpatterns = [
    path('health/', JobsHealthView.as_view(), name='jobs-health'),
]
