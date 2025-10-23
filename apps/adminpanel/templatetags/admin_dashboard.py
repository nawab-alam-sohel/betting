from django import template
from django.db.models import Sum

from apps.users.models import User
from apps.users.models_kyc import KYCDocument
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
def stat_rejected_deposits():
    return PaymentIntent.objects.filter(status='failed').count()


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
def stat_upcoming_games():
    return Game.objects.filter(status='scheduled').count()


@register.simple_tag
def stat_open_for_betting_games():
    # Consider scheduled and live as open for betting
    return Game.objects.filter(status__in=['scheduled', 'live']).count()


@register.simple_tag
def stat_not_open_for_betting_games():
    return Game.objects.filter(status__in=['closed', 'ended', 'cancelled']).count()


@register.simple_tag
def stat_email_unverified_users():
    return User.objects.filter(email_verified=False).count()


@register.simple_tag
def stat_mobile_unverified_users():
    return User.objects.filter(phone_verified=False).count()


@register.simple_tag
def stat_pending_kyc_documents():
    return KYCDocument.objects.filter(status='pending').count()


@register.simple_tag
def stat_pending_support_tickets():
    # No ticketing app yet - return 0 to keep dashboard stable
    return 0


@register.simple_tag
def stat_pending_outcomes():
    # Placeholder; settlement workflow not implemented
    return 0


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


@register.simple_tag
def sum_deposit_charges_cents():
    # No fee model implemented yet; keep 0 to avoid errors
    return 0


@register.simple_tag
def sum_withdrawal_charges_cents():
    # No fee model implemented yet; keep 0 to avoid errors
    return 0


@register.filter(name='cents_to_currency')
def cents_to_currency(value, currency='BDT'):
    try:
        cents = int(value or 0)
    except (TypeError, ValueError):
        cents = 0
    amount = cents / 100.0
    return f"{currency} {amount:,.2f}"
