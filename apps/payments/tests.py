from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.payments.models import PaymentIntent
from apps.wallets.models import Wallet, Transaction

User = get_user_model()


class PaymentsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='payuser@example.com', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_initiate_redirect_flow(self):
        url = reverse('payment-initiate')
        resp = self.client.post(url, {'provider': 'bkash', 'amount': '100.00', 'flow': 'redirect'}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('redirect_url', resp.json())

    def test_server_flow_bkash_initiate(self):
        url = reverse('payment-initiate')
        resp = self.client.post(url, {'provider': 'bkash', 'amount': '50.00', 'flow': 'server'}, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn('provider_payment_id', data)
        self.assertIn('payment_url', data)

    def test_webhook_completes_and_credits_wallet(self):
        # create an intent
        pi = PaymentIntent.objects.create(user=self.user, provider='bkash', amount_cents=5000)
        # post webhook
        url = reverse('payment-webhook', kwargs={'provider': 'bkash'})
        resp = self.client.post(url, {'intent_id': pi.id, 'status': 'completed', 'reference': 'REF123'}, format='json')
        self.assertEqual(resp.status_code, 200)
        pi.refresh_from_db()
        self.assertEqual(pi.status, 'completed')
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(wallet.balance_cents, 5000)
        tx = Transaction.objects.filter(wallet=wallet, type='deposit', reference='REF123').first()
        self.assertIsNotNone(tx)