from celery import shared_task
from django.db import transaction
from apps.bets.models import Bet
from apps.wallets.models import Wallet, Transaction
from apps.agents.models import Agent, AgentCommission
from apps.users.models import User


@shared_task(bind=True)
def settle_bet_task(self, bet_id):
    """Settle a single bet synchronously in a DB transaction.

    This is a simplified placeholder: real settlement needs to calculate
    outcome, handle partial refunds, commissions, and race conditions.
    """
    try:
        with transaction.atomic():
            bet = Bet.objects.select_for_update().get(id=bet_id)
            if bet.status != 'placed':
                return {'status': 'ignored', 'reason': 'already-settled'}

            # Finalize reserved stake and credit potential win
            wallet = Wallet.objects.select_for_update().get(user=bet.user)
            # deduct reserved stake and balance
            wallet.finalize_reservation(bet.total_stake_cents)

            # credit win amount (placeholder demo logic: mark as 'won')
            bet.result = 'won'
            if bet.potential_win_cents > 0:
                wallet.balance_cents += bet.potential_win_cents
                wallet.save(update_fields=['balance_cents'])
                Transaction.objects.create(wallet=wallet, amount_cents=bet.potential_win_cents, type='win', status='completed')

            # Commission payouts to agent chain (simple model: commission % on stake)
            agent = None
            try:
                agent = bet.user.agent
            except Exception:
                agent = None

            current = agent
            while current:
                # get latest commission configured for this agent
                commission = AgentCommission.objects.filter(agent=current).order_by('-created_at').first()
                if commission and commission.percentage and commission.percentage > 0:
                    # compute commission on total stake
                    pct = float(commission.percentage)
                    commission_cents = int(bet.total_stake_cents * (pct / 100.0))
                    if commission_cents > 0:
                        # credit to agent's user wallet
                        agent_user = current.user
                        agent_wallet, _ = Wallet.objects.select_for_update().get_or_create(user=agent_user)
                        agent_wallet.balance_cents += commission_cents
                        agent_wallet.save(update_fields=['balance_cents'])
                        Transaction.objects.create(wallet=agent_wallet, amount_cents=commission_cents, type='commission', status='completed', reference=f'bet:{bet.id}')
                # move up the chain
                current = current.parent

            bet.status = 'settled'
            bet.save()
            return {'status': 'settled', 'bet_id': bet_id}
    except Bet.DoesNotExist:
        return {'status': 'error', 'reason': 'not_found'}
