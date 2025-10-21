from django.db import models
from django.conf import settings
from django.utils import timezone


class ReconciliationBatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    provider = models.ForeignKey('PaymentProvider', on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['provider', 'status', 'created_at'])
        ]


class ReconciliationItem(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal')
    ]
    STATUS_CHOICES = [
        ('matched', 'Matched'),
        ('mismatched', 'Mismatched'),
        ('missing', 'Missing'),
        ('extra', 'Extra')
    ]
    
    batch = models.ForeignKey(ReconciliationBatch, on_delete=models.CASCADE, related_name='items')
    transaction_id = models.CharField(max_length=128)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount_cents = models.BigIntegerField()
    provider_reference = models.CharField(max_length=128, blank=True)
    provider_status = models.CharField(max_length=50, blank=True)
    our_status = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['batch', 'status', 'transaction_id'])
        ]


class ReconciliationReport(models.Model):
    batch = models.OneToOneField(ReconciliationBatch, on_delete=models.CASCADE)
    total_transactions = models.IntegerField(default=0)
    matched_count = models.IntegerField(default=0)
    mismatched_count = models.IntegerField(default=0)
    missing_count = models.IntegerField(default=0)
    extra_count = models.IntegerField(default=0)
    total_amount_cents = models.BigIntegerField(default=0)
    mismatched_amount_cents = models.BigIntegerField(default=0)
    generated_at = models.DateTimeField(default=timezone.now)
    report_data = models.JSONField(default=dict)
    summary = models.TextField(blank=True)


class PaymentProvider(models.Model):
    """Stores display info for manual provider deposits/withdrawals (e.g., bKash number)."""
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    display_number = models.CharField(max_length=64, help_text='Number shown to users for cash transfers')
    instructions = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.display_number})"


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_cents = models.BigIntegerField()
    provider = models.ForeignKey(PaymentProvider, on_delete=models.PROTECT)
    provider_account = models.CharField(max_length=128, blank=True, null=True, help_text='User provided number / account')
    reference = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Withdrawal({self.user.email}) {self.amount_cents} {self.status}"
