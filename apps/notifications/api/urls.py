from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NotificationLogViewSet, InAppNotificationViewSet

router = DefaultRouter()
router.register(r'logs', NotificationLogViewSet, basename='notification-log')
router.register(r'in-app', InAppNotificationViewSet, basename='in-app-notification')

urlpatterns = router.urls