from django.test import Client
from django.contrib.auth import get_user_model
from apps.payments.models_recon import PaymentProvider
User=get_user_model()
# setup
u=User.objects.create_user(email='rec_user2@example.com', password='pass')
p=PaymentProvider.objects.create(key='bkash2', name='bKash', display_number='01XXXXXXXXX')
client=Client()
client.login(email='rec_user2@example.com', password='pass')
resp=client.post('/api/payments/withdrawals/', {'amount_cents':2000, 'provider':p.id, 'provider_account':'017XXXXXX'}, content_type='application/json')
print('status', resp.status_code)
print(resp.content)
