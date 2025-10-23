from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from apps.users.models import User
from apps.payments.models import PaymentIntent
from apps.payments.models_recon import WithdrawalRequest, PaymentProvider


class AdminFinanceApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email="admin@example.com", password="pass", is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

    def test_deposits_summary_and_list(self):
        # seed deposits
        PaymentIntent.objects.create(user=self.admin, provider='bkash', amount_cents=1000, status='pending')
        PaymentIntent.objects.create(user=self.admin, provider='bkash', amount_cents=2000, status='completed')
        PaymentIntent.objects.create(user=self.admin, provider='nagad', amount_cents=3000, status='failed')
        PaymentIntent.objects.create(user=self.admin, provider='nagad', amount_cents=1500, status='initiated')

        # summary
        resp = self.client.get('/api/admin/dashboard/finance/deposits/summary/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get('pending'), 1)
        self.assertEqual(data.get('successful'), 1)
        self.assertEqual(data.get('rejected'), 1)
        self.assertEqual(data.get('initiated'), 1)
        self.assertEqual(data.get('all'), 4)

        # list filter approved/successful -> completed
        resp = self.client.get('/api/admin/dashboard/finance/deposits/?status=approved&page_size=10')
        self.assertEqual(resp.status_code, 200)
        results = resp.json().get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'completed')

        # list filter rejected -> failed
        resp = self.client.get('/api/admin/dashboard/finance/deposits/?status=rejected&page_size=10')
        self.assertEqual(resp.status_code, 200)
        results = resp.json().get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'failed')

    def test_withdrawals_summary_and_list(self):
        provider = PaymentProvider.objects.create(key='bkash', name='bKash', display_number='01700-000000')
        WithdrawalRequest.objects.create(user=self.admin, amount_cents=5000, provider=provider, status='pending')
        WithdrawalRequest.objects.create(user=self.admin, amount_cents=6000, provider=provider, status='approved')
        WithdrawalRequest.objects.create(user=self.admin, amount_cents=7000, provider=provider, status='rejected')

        resp = self.client.get('/api/admin/dashboard/finance/withdrawals/summary/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get('pending'), 1)
        self.assertEqual(data.get('approved'), 1)
        self.assertEqual(data.get('rejected'), 1)
        self.assertEqual(data.get('all'), 3)

        resp = self.client.get('/api/admin/dashboard/finance/withdrawals/?status=approved&page_size=10')
        self.assertEqual(resp.status_code, 200)
        results = resp.json().get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'approved')
