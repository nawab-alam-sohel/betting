from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User


class WalletsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='wallet@example.com')
        self.user.set_password('pass1234')
        self.user.save()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.wallet_url = reverse('wallet')
        self.deposit_url = reverse('wallet-deposit')
        self.txns_url = reverse('wallet-transactions')

    def authenticate(self):
        resp = self.client.post(self.login_url, data={'email': self.user.email, 'password': 'pass1234'})
        tokens = resp.json()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_deposit_and_balance(self):
        self.authenticate()
        resp = self.client.post(self.deposit_url, data={'amount': '100.00'})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get(self.wallet_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('balance'), '100.00')

    def test_transactions_list(self):
        self.authenticate()
        # deposit
        self.client.post(self.deposit_url, data={'amount': '50.00'})
        resp = self.client.get(self.txns_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) >= 1)
