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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("apps.users.api.urls")),
    # Legacy/auth alias - keep /api/auth/ for some clients/tests
    path("api/auth/", include("apps.users.api.urls")),
    path("api/wallets/", include("apps.wallets.api.urls")),
    path("api/bets/", include("apps.bets.api.urls")),
    path("api/agents/", include("apps.agents.api.urls")),
    path("api/payments/", include("apps.payments.api.urls")),
    path("api/sports/", include("apps.sports.api.urls")),
    path("api/notifications/", include("apps.notifications.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)