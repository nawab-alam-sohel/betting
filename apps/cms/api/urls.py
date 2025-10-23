from django.urls import path
from .views import CmsHealthView, SiteSettingView, PageDetailView

urlpatterns = [
    path('health/', CmsHealthView.as_view(), name='cms-health'),
    path('settings/', SiteSettingView.as_view(), name='cms-settings'),
    path('pages/<slug:slug>/', PageDetailView.as_view(), name='cms-page-detail'),
]
