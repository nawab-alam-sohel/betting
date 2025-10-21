from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.agents.models import Agent, AgentCommission
from apps.wallets.models import Wallet, Transaction
from apps.bets.models import Bet
from apps.bets.tasks import settle_bet_task


User = get_user_model()


class AgentCommissionTests(TestCase):
    def setUp(self):
        # create agent users and profiles
        self.parent_user = User.objects.create_user(email='parent@example.com', password='pass')
        self.parent_agent = Agent.objects.create(user=self.parent_user, name='ParentAgent')
        AgentCommission.objects.create(agent=self.parent_agent, percentage=2.0)

        self.child_user = User.objects.create_user(email='child@example.com', password='pass')
        self.child_agent = Agent.objects.create(user=self.child_user, name='ChildAgent', parent=self.parent_agent)
        AgentCommission.objects.create(agent=self.child_agent, percentage=3.0)

        # create client who belongs to child agent
        self.client_user = User.objects.create_user(email='client@example.com', password='pass')
        self.client_user.agent = self.child_agent
        self.client_user.save()

        # prepare wallets
        self.parent_wallet, _ = Wallet.objects.get_or_create(user=self.parent_user, defaults={'balance_cents': 0})
        self.child_wallet, _ = Wallet.objects.get_or_create(user=self.child_user, defaults={'balance_cents': 0})
        self.client_wallet, _ = Wallet.objects.get_or_create(user=self.client_user, defaults={'balance_cents': 10000, 'reserved_balance_cents': 0})

    def test_commission_single_settlement(self):
        # client places a bet of 100.00 (10000 cents) reserved
        stake = 10000
        self.client_wallet.balance_cents = 10000
        self.client_wallet.reserved_balance_cents = stake
        self.client_wallet.save()

        bet = Bet.objects.create(user=self.client_user, total_stake_cents=stake, potential_win_cents=15000)

        # settle the bet
        res = settle_bet_task.apply(args=(bet.id,))
        self.assertTrue(res.successful())

        # commissions: child 3% of stake -> 300 cents, parent 2% -> 200 cents
        self.child_wallet.refresh_from_db()
        self.parent_wallet.refresh_from_db()
        self.assertEqual(self.child_wallet.balance_cents, 300)
        self.assertEqual(self.parent_wallet.balance_cents, 200)

    def test_commission_multi_level(self):
        # Add another level: grandparent
        grand_user = User.objects.create_user(email='grand@example.com', password='pass')
        grand_agent = Agent.objects.create(user=grand_user, name='GrandAgent')
        grand_comm = AgentCommission.objects.create(agent=grand_agent, percentage=1.0)

        # re-parent chain: parent_agent becomes child of grand_agent
        self.parent_agent.parent = grand_agent
        self.parent_agent.save()

        # client wallet reserve
        stake = 20000
        self.client_wallet.balance_cents = 20000
        self.client_wallet.reserved_balance_cents = stake
        self.client_wallet.save()

        bet = Bet.objects.create(user=self.client_user, total_stake_cents=stake, potential_win_cents=30000)
        res = settle_bet_task.apply(args=(bet.id,))
        self.assertTrue(res.successful())

        # commissions: child 3% -> 600, parent 2% -> 400, grand 1% -> 200
        self.child_wallet.refresh_from_db()
        self.parent_wallet.refresh_from_db()
        grand_wallet, _ = Wallet.objects.get_or_create(user=grand_user)
        self.assertEqual(self.child_wallet.balance_cents, 600)
        self.assertEqual(self.parent_wallet.balance_cents, 400)
        self.assertEqual(grand_wallet.balance_cents, 200)
