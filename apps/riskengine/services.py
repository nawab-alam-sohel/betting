from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db import models
from apps.bets.models import Bet


def check_bet(user, total_stake_cents: int) -> dict:
    """
    Simple risk checks: max per bet and max daily stake per user.
    Returns { allowed: bool, reasons: [str] }
    """
    reasons = []
    max_per_bet = getattr(settings, 'RISK_MAX_STAKE_PER_BET_CENTS', 1_000_000)
    if total_stake_cents > max_per_bet:
        reasons.append(f"Stake exceeds per-bet cap ({max_per_bet} cents)")

    # Daily cap for user's total stakes (placed bets) in last 24h
    max_daily = getattr(settings, 'RISK_MAX_DAILY_STAKE_CENTS', 5_000_000)
    since = timezone.now() - timedelta(hours=24)
    spent = (
        Bet.objects.filter(user=user, placed_at__gte=since)
        .exclude(status='cancelled')
        .aggregate(total=models.Sum('total_stake_cents'))
        .get('total')
        or 0
    )
    if spent + total_stake_cents > max_daily:
        reasons.append(f"Daily stake cap exceeded ({max_daily} cents)")

    return {"allowed": len(reasons) == 0, "reasons": reasons}
