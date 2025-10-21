from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.payments.models_recon import (
    PaymentProvider, WithdrawalRequest, ReconciliationBatch,
    ReconciliationItem, ReconciliationReport
)
from apps.wallets.models import Wallet, Transaction

User = get_user_model()


class ReconciliationBatchTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='rec_user@example.com', password='pass')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='pass')
        self.provider = PaymentProvider.objects.create(key='bkash', name='bKash', display_number='01XXXXXXXXX')
        self.wallet = Wallet.objects.create(user=self.user, balance_cents=10000)
        
        # Create a test reconciliation batch
        now = timezone.now()
        self.batch = ReconciliationBatch.objects.create(
            provider=self.provider,
            start_date=now - timedelta(days=1),
            end_date=now,
            status='pending'
        )
        
        # Create some test reconciliation items
        self.items = []
        for i in range(3):
            item = ReconciliationItem.objects.create(
                batch=self.batch,
                transaction_id=f'TX{i}',
                transaction_type='deposit',
                amount_cents=1000 * (i + 1),
                provider_reference=f'PR{i}',
                provider_status='completed',
                our_status='completed',
                status='matched'
            )
            self.items.append(item)
            
        # Create a mismatched item
        self.mismatched_item = ReconciliationItem.objects.create(
            batch=self.batch,
            transaction_id='TX_MISMATCH',
            transaction_type='withdrawal',
            amount_cents=5000,
            provider_reference='PR_MISMATCH',
            provider_status='completed',
            our_status='pending',
            status='mismatched'
        )
        
        # Create report
        self.report = ReconciliationReport.objects.create(
            batch=self.batch,
            total_transactions=4,
            matched_count=3,
            mismatched_count=1,
            total_amount_cents=8000,
            mismatched_amount_cents=5000
        )

    def test_list_providers_public(self):
        url = '/api/payments/providers/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)

    def test_list_reconciliation_batches(self):
        self.client.force_authenticate(user=self.admin)
        url = '/api/payments/reconciliation/batches/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['provider'], self.provider.id)
        self.assertEqual(data[0]['status'], 'pending')
        
    def test_get_batch_details(self):
        self.client.force_authenticate(user=self.admin)
        url = f'/api/payments/reconciliation/batches/{self.batch.id}/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['items_count'], 4)
        self.assertEqual(data['mismatched_count'], 1)
        
    def test_start_reconciliation(self):
        self.client.force_authenticate(user=self.admin)
        url = f'/api/payments/reconciliation/batches/{self.batch.id}/start_reconciliation/'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.status, 'processing')
        
    def test_get_batch_summary(self):
        self.client.force_authenticate(user=self.admin)
        url = f'/api/payments/reconciliation/batches/{self.batch.id}/summary/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['total_transactions'], 4)
        self.assertEqual(data['matched_count'], 3)
        self.assertEqual(data['mismatched_count'], 1)
        
    def test_list_reconciliation_items(self):
        self.client.force_authenticate(user=self.admin)
        url = '/api/payments/reconciliation/items/'
        resp = self.client.get(url, {'batch': self.batch.id})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 4)
        
    def test_filter_mismatched_items(self):
        self.client.force_authenticate(user=self.admin)
        url = '/api/payments/reconciliation/items/'
        resp = self.client.get(url, {'batch': self.batch.id, 'status': 'mismatched'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['transaction_id'], 'TX_MISMATCH')