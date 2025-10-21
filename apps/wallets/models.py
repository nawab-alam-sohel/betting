from django.db import models
from django.conf import settings
from decimal import Decimal


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    # store cents as integer for accuracy
    balance_cents = models.BigIntegerField(default=0)
    # reserved balance (holds for placed bets)
    reserved_balance_cents = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=3, default='BDT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet({self.user.email}) {self.balance_cents} {self.currency}"

    @property
    def balance(self):
        return Decimal(self.balance_cents) / Decimal(100)

    def reserve(self, cents):
        """Reserve cents for a pending action. Returns True if reserved, False if insufficient."""
        # atomic reservation should be handled by caller using select_for_update
        if self.balance_cents - self.reserved_balance_cents < cents:
            return False
        self.reserved_balance_cents += cents
        self.save(update_fields=['reserved_balance_cents'])
        return True

    def finalize_reservation(self, cents):
        """Finalize a reserved amount: deduct reserved and total balance (e.g., on bet settled/accepted)."""
        # atomic operation expected
        self.reserved_balance_cents -= cents
        self.balance_cents -= cents
        self.save(update_fields=['reserved_balance_cents', 'balance_cents'])


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('bet', 'Bet'),
        ('win', 'Win'),
        ('refund', 'Refund'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount_cents = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    reference = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Txn({self.wallet.user.email}) {self.type} {self.amount_cents} {self.status}"
