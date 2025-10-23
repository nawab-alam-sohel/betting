"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from apps.adminpanel import views as adminpanel_views
# Ensure all local models are registered BEFORE admin URLs are built
try:
    from apps.adminpanel.auto_admin import register_unregistered_models
    register_unregistered_models()
except Exception:
    pass
from django.conf import settings 
from django.conf.urls.static import static  
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib.sitemaps.views import sitemap
from apps.cms.sitemaps import sitemaps
from apps.cms import views as cms_views

def health(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    # Add a clean System Settings page inside admin
    path('admin/system/settings/', adminpanel_views.system_settings, name='admin-system-settings'),
    # Admin metrics for sidebar badges
    path('admin/metrics/payments/', adminpanel_views.payments_metrics, name='admin-payments-metrics'),
    path('admin/metrics/notifications/', adminpanel_views.notifications_metrics, name='admin-notifications-metrics'),
    path('admin/metrics/users/', adminpanel_views.users_metrics, name='admin-users-metrics'),
    # Unified admin: use Django admin only (no extra CMS dashboards)
    # Default Django admin (kept last so our custom routes take precedence)
    path('admin/', admin.site.urls),
    path('health/', health),
    # Robots & sitemap
    path('robots.txt', cms_views.robots_txt, name='robots-txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # API schema & docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Public accounts endpoints
    path('accounts/', include('apps.users.urls')),
    # Admin dashboard API (for custom UI widgets)
    path('api/admin/dashboard/', include('apps.adminpanel.api.urls')),
    path("api/users/", include("apps.users.api.urls")),
    # Legacy/auth alias - keep /api/auth/ for some clients/tests
    path("api/auth/", include("apps.users.api.urls")),
    path("api/wallets/", include("apps.wallets.api.urls")),
    path("api/bets/", include("apps.bets.api.urls")),
    path("api/agents/", include("apps.agents.api.urls")),
    path("api/payments/", include("apps.payments.api.urls")),
    path("api/sports/", include("apps.sports.api.urls")),
    path("api/notifications/", include("apps.notifications.api.urls")),
    path("api/casino/", include("apps.casino.api.urls")),
    path("api/commissions/", include("apps.commissions.api.urls")),
    path("api/riskengine/", include("apps.riskengine.api.urls")),
    path("api/fraud-aml/", include("apps.fraud_aml.api.urls")),
    path("api/reconciliation/", include("apps.reconciliation.api.urls")),
    path("api/realtime/", include("apps.realtime.api.urls")),
    path("api/reports/", include("apps.reports.api.urls")),
    path("api/cms/", include("apps.cms.api.urls")),
    path("api/jobs/", include("apps.jobs.api.urls")),
    path("api/audit/", include("apps.audit.api.urls")),
]

# (registration moved above, before admin.site.urls is referenced)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)