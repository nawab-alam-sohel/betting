from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class SMSTemplate(models.Model):
    """Templates for SMS messages"""
    name = models.CharField(max_length=100, unique=True)
    template_key = models.SlugField(max_length=100, unique=True)
    content = models.TextField(
        help_text='Use {variable} for placeholders. Example: Your OTP is {otp}'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    """Templates for email messages"""
    name = models.CharField(max_length=100, unique=True)
    template_key = models.SlugField(max_length=100, unique=True)
    subject = models.CharField(max_length=255)
    html_content = models.TextField(
        help_text='HTML content with {variable} placeholders'
    )
    text_content = models.TextField(
        help_text='Plain text content with {variable} placeholders'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NotificationLog(models.Model):
    """Log of all notifications sent"""
    NOTIFICATION_TYPES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    ]

    NOTIFICATION_STATUS = [
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notifications'
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    email = models.EmailField(null=True, blank=True)
    template_key = models.CharField(max_length=100)
    context_data = models.JSONField(
        default=dict,
        help_text='Template variables in JSON format'
    )
    status = models.CharField(
        max_length=10,
        choices=NOTIFICATION_STATUS,
        default='queued'
    )
    error_message = models.TextField(null=True, blank=True)
    provider_message_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['notification_type', 'status']),
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['phone_number', 'created_at']),
            models.Index(fields=['email', 'created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} to {self.recipient or self.phone_number or self.email}"


class InAppNotification(models.Model):
    """Notifications shown in the app UI"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='in_app_notifications'
    )
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default='info'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    action_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='URL to redirect when notification is clicked'
    )
    is_read = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient}"