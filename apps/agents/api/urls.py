from django.urls import path
from .views import MyAgentProfile, AgentCommissions, CommissionReportView, CommissionExportCSV, CommissionDetailView

# Namespace for reversing in tests and project urls
app_name = 'agents'

urlpatterns = [
    path('me/', MyAgentProfile.as_view(), name='agent-me'),
    path('commissions/', AgentCommissions.as_view(), name='agent-commissions'),
    path('reports/commissions/', CommissionReportView.as_view(), name='commission-report'),
    path('reports/commissions/export/', CommissionExportCSV.as_view(), name='commission-export-csv'),
    path('reports/commissions/detail/', CommissionDetailView.as_view(), name='commission-detail'),
]
