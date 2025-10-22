from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50)
    model = models.CharField(max_length=120, blank=True)
    object_id = models.CharField(max_length=120, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    changes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['path', 'created_at']),
            models.Index(fields=['model', 'object_id']),
            models.Index(fields=['action', 'created_at']),
        ]

    def __str__(self):
        who = self.actor.email if self.actor else 'system'
        return f"{self.action} by {who} on {self.model}#{self.object_id}"
