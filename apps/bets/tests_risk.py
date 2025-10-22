from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.wallets.models import Wallet


User = get_user_model()


class BetsRiskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='riskbettor@example.com', password='pass1234')
        self.wallet = Wallet.objects.create(user=self.user, balance_cents=10000)  # 100.00
        self.client = APIClient()
        resp = self.client.post('/api/auth/token/', {'email': 'riskbettor@example.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(resp.status_code, 200)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @override_settings(RISK_MAX_STAKE_PER_BET_CENTS=500)
    def test_place_bet_denied_by_per_bet_cap(self):
        payload = {
            'lines': [
                {'event': 'Match R', 'market': 'Winner', 'selection': 'Team R', 'odds': '2.00', 'stake': '10.00'},
            ]
        }
        resp = self.client.post('/api/bets/place/', payload, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json().get('detail'), 'risk_denied')

    @override_settings(RISK_MAX_STAKE_PER_BET_CENTS=500)
    def test_quote_returns_risk_flags(self):
        payload = {
            'lines': [
                {'event': 'Match R', 'market': 'Winner', 'selection': 'Team R', 'odds': '2.00', 'stake': '10.00'},
            ]
        }
        resp = self.client.post('/api/bets/quote/', payload, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json().get('risk_allowed'))
        self.assertTrue(len(resp.json().get('risk_reasons') or []) > 0)
