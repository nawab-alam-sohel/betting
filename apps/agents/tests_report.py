from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User
from apps.agents.models import Agent
from apps.wallets.models import Wallet, Transaction


class CommissionReportTests(TestCase):
    def setUp(self):
        # create staff user
        self.staff = User.objects.create_user(email='staff@example.com', password='pass', is_staff=True)
        self.agent_user = User.objects.create_user(email='agent@example.com', password='pass')
        self.agent = Agent.objects.create(user=self.agent_user, name='Agent A')
        # create wallets and a commission transaction
        self.agent_wallet = Wallet.objects.create(user=self.agent_user, balance_cents=0, reserved_balance_cents=0)
        Transaction.objects.create(wallet=self.agent_wallet, amount_cents=1500, type='commission', status='completed')

        self.client = APIClient()

    def test_agent_report_for_non_agent(self):
        # a normal user without agent profile should get 403
        user = User.objects.create_user(email='u1@example.com', password='pass')
        self.client.force_authenticate(user=user)
        url = reverse('agents:commission-report')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_agent_can_view_own_report(self):
        self.client.force_authenticate(user=self.agent_user)
        url = reverse('agents:commission-report')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, list)

    def test_staff_can_export_csv(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('agents:commission-export-csv')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')

    def test_commission_detail_pagination_and_filter(self):
        # create a few commission transactions across dates
        now = Transaction.objects.create(wallet=self.agent_wallet, amount_cents=2000, type='commission', status='completed')
        older = Transaction.objects.create(wallet=self.agent_wallet, amount_cents=3000, type='commission', status='completed')

        self.client.force_authenticate(user=self.agent_user)
        url = reverse('agents:commission-detail')
        resp = self.client.get(url + '?page_size=1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(len(resp.data['results']), 1)

        # test date filter - future date should return none
        resp2 = self.client.get(url + '?from=2100-01-01')
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.data['results']), 0)
