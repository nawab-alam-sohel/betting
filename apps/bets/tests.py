from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.wallets.models import Wallet


User = get_user_model()


class BetsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='bettor@example.com', password='pass1234')
        self.wallet = Wallet.objects.create(user=self.user, balance_cents=10000)  # 100.00
        self.client = APIClient()
        resp = self.client.post('/api/auth/token/', {'email': 'bettor@example.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_place_bet_success(self):
        payload = {
            'lines': [
                {'event': 'Match A', 'market': 'Winner', 'selection': 'Team A', 'odds': '1.50', 'stake': '10.00'},
            ]
        }
        resp = self.client.post('/api/bets/place/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.wallet.refresh_from_db()
        # stake should be reserved but not yet deducted from balance
        self.assertEqual(self.wallet.balance_cents, 10000)
        self.assertEqual(self.wallet.reserved_balance_cents, 1000)

        # settle the bet synchronously via the task (run locally)
        from apps.bets.tasks import settle_bet_task
        bet_id = resp.data['bet_id']
        # run the task locally and get the result
        res = settle_bet_task.apply(args=(bet_id,))
        self.assertTrue(res.successful())
        self.wallet.refresh_from_db()
        # reserved stake removed and winnings credited
        self.assertEqual(self.wallet.reserved_balance_cents, 0)
        self.assertEqual(self.wallet.balance_cents, 10000 - 1000 + 1500)

    def test_place_bet_insufficient(self):
        payload = {
            'lines': [
                {'event': 'Match A', 'market': 'Winner', 'selection': 'Team A', 'odds': '2.00', 'stake': '200.00'},
            ]
        }
        resp = self.client.post('/api/bets/place/', payload, format='json')
        self.assertEqual(resp.status_code, 400)
