from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.wallets.models import Wallet
from apps.agents.models import Agent, AgentCommission
from apps.bets.models import Bet


User = get_user_model()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class BetsIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create agent chain
        self.parent_user = User.objects.create_user(email='parint_int@example.com', password='pass')
        self.parent_agent = Agent.objects.create(user=self.parent_user, name='ParentInt')
        AgentCommission.objects.create(agent=self.parent_agent, percentage=2.0)

        self.child_user = User.objects.create_user(email='child_int@example.com', password='pass')
        self.child_agent = Agent.objects.create(user=self.child_user, name='ChildInt', parent=self.parent_agent)
        AgentCommission.objects.create(agent=self.child_agent, percentage=3.0)

        # client user
        self.user = User.objects.create_user(email='client_int@example.com', password='pass')
        self.user.agent = self.child_agent
        self.user.save()

        # wallet
        self.wallet, _ = Wallet.objects.get_or_create(user=self.user, defaults={'balance_cents': 10000})

        # obtain token via API
        resp = self.client.post('/api/auth/token/', {'email': self.user.email, 'password': 'pass'}, format='json')
        self.token = resp.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_place_and_settle_async(self):
        payload = {
            'lines': [
                {'event': 'Match X', 'market': 'Winner', 'selection': 'X', 'odds': '2.00', 'stake': '10.00'},
            ]
        }
        resp = self.client.post('/api/bets/place/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        # run settlement explicitly (place-bet does not auto-enqueue settlement)
        from apps.bets.tasks import settle_bet_task
        bet_id = resp.json().get('bet_id')
        res = settle_bet_task.apply(args=(bet_id,))
        self.assertTrue(res.successful())
        self.wallet.refresh_from_db()
        # reserved cleared, balance updated: initial 10000 - 1000 stake + 2000 win
        self.assertEqual(self.wallet.balance_cents, 10000 - 1000 + 2000)

        # check agents received commissions
        child_wallet = Wallet.objects.get(user=self.child_user)
        parent_wallet = Wallet.objects.get(user=self.parent_user)
        # child 3% * 1000 = 30 cents
        self.assertEqual(child_wallet.balance_cents, 30)
        self.assertEqual(parent_wallet.balance_cents, 20)
