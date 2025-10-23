from django.urls import path
from .views import AuditHealthView

urlpatterns = [
    path('health/', AuditHealthView.as_view(), name='audit-health'),
]
