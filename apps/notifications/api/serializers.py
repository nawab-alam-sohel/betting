from rest_framework import serializers
from .models import NotificationLog, InAppNotification


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = [
            'id',
            'notification_type',
            'phone_number',
            'email',
            'template_key',
            'context_data',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields


class InAppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'action_url',
            'is_read',
            'created_at'
        ]
        read_only_fields = [
            'notification_type',
            'title',
            'message',
            'action_url',
            'created_at'
        ]