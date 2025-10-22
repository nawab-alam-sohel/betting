from django import template
from django.db.models import Sum

from apps.users.models import User
from apps.bets.models import Bet
from apps.payments.models import PaymentIntent
from apps.payments.models_recon import WithdrawalRequest
from apps.wallets.models import Transaction
from apps.sports.models import Game

register = template.Library()


@register.simple_tag
def stat_total_users():
    return User.objects.count()


@register.simple_tag
def stat_active_users():
    return User.objects.filter(is_active=True, is_banned=False).count()


@register.simple_tag
def stat_pending_deposits():
    return PaymentIntent.objects.filter(status='pending').count()


@register.simple_tag
def stat_completed_deposits():
    return PaymentIntent.objects.filter(status='completed').count()


@register.simple_tag
def stat_pending_withdrawals():
    return WithdrawalRequest.objects.filter(status='pending').count()


@register.simple_tag
def stat_approved_withdrawals():
    return WithdrawalRequest.objects.filter(status='approved').count()


@register.simple_tag
def stat_pending_bets():
    return Bet.objects.filter(status='placed').count()


@register.simple_tag
def stat_live_games():
    return Game.objects.filter(status='live').count()


@register.simple_tag
def sum_deposits_cents():
    return (
        Transaction.objects.filter(type='deposit', status='completed')
        .aggregate(s=Sum('amount_cents'))['s'] or 0
    )


@register.simple_tag
def sum_withdrawals_cents():
    return (
        Transaction.objects.filter(type='withdraw', status='completed')
        .aggregate(s=Sum('amount_cents'))['s'] or 0
    )


@register.filter(name='cents_to_currency')
def cents_to_currency(value, currency='BDT'):
    try:
        cents = int(value or 0)
    except (TypeError, ValueError):
        cents = 0
    amount = cents / 100.0
    return f"{currency} {amount:,.2f}"
