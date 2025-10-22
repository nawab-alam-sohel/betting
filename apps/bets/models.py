from django.db import models
from django.conf import settings
from django.utils import timezone


class Bet(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ]
    RESULT_CHOICES = [
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bets')
    total_stake_cents = models.BigIntegerField()
    potential_win_cents = models.BigIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='placed')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True)
    placed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bet({self.user.email}) {self.total_stake_cents} -> {self.potential_win_cents} {self.status}"


class BetLine(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name='lines')
    event = models.CharField(max_length=128)
    market = models.CharField(max_length=128)
    selection = models.CharField(max_length=128)
    odds = models.DecimalField(max_digits=9, decimal_places=4)
    stake_cents = models.BigIntegerField()

    def __str__(self):
        return f"BetLine({self.bet_id}) {self.selection} @ {self.odds} stake={self.stake_cents}"
