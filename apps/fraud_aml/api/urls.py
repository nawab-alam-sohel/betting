from django.urls import path
from .views import AmlHealthView

urlpatterns = [
    path('health/', AmlHealthView.as_view(), name='fraud-aml-health'),
]
