from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from ..models import NotificationLog, InAppNotification
from .serializers import NotificationLogSerializer, InAppNotificationSerializer


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return NotificationLog.objects.all().order_by('-created_at')
        return NotificationLog.objects.filter(
            Q(recipient=user) |
            Q(phone_number=user.phone) |
            Q(email=user.email)
        ).order_by('-created_at')


class InAppNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InAppNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return InAppNotification.objects.all().order_by('-created_at')
        return InAppNotification.objects.filter(
            recipient=user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})