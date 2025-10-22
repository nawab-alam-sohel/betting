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
from django.conf import settings 
from django.conf.urls.static import static  
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def health(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health),
    # API schema & docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)