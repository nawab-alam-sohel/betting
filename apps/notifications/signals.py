from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .services import NotificationService
from .models import NotificationLog

User = get_user_model()

@receiver(post_save, sender=NotificationLog)
def notify_user(sender, instance, created, **kwargs):
    """Update user about notification status changes"""
    if not created and instance.status == 'failed':
        service = NotificationService()
        service.create_in_app_notification(
            user=instance.recipient,
            title='Notification Failed',
            message=f'Failed to send {instance.notification_type} notification. Please update your contact information.',
            notification_type='error'
        )