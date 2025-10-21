from django.db import models
from django.conf import settings


class PaymentIntent(models.Model):
    PROVIDER_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
    ]
    FLOW_CHOICES = [
        ('server', 'Server'),
        ('redirect', 'Redirect'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    amount_cents = models.BigIntegerField()
    currency = models.CharField(max_length=3, default='BDT')
    flow = models.CharField(max_length=10, choices=FLOW_CHOICES, default='server')
    reference = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentIntent({self.user.email}) {self.provider} {self.amount_cents} {self.status}"
