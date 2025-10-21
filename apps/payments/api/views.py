from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.payments.models import PaymentIntent
from apps.payments.api.serializers import PaymentIntentSerializer
from apps.wallets.models import Wallet, Transaction
from apps.payments.providers import bkash


class InitiatePaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        provider = request.data.get('provider')
        amount = request.data.get('amount')
        flow = request.data.get('flow', 'server')
        if not provider or not amount:
            return Response({'detail': 'provider and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
        # expect amount as decimal string in BDT
        try:
            amount_cents = int(round(float(amount) * 100))
        except Exception:
            return Response({'detail': 'invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        pi = PaymentIntent.objects.create(user=request.user, provider=provider, amount_cents=amount_cents, flow=flow)
        data = PaymentIntentSerializer(pi).data
        # For redirect flows return a fake redirect url to simulate provider
        if flow == 'redirect':
            data['redirect_url'] = f"https://payments.example/{provider}/pay/{pi.id}"
        else:
            # server-side flow: call provider adapter to create a payment
            if provider == 'bkash':
                resp = bkash.create_payment(amount_cents, pi.id)
                data.update({'provider_payment_id': resp.get('provider_payment_id'), 'payment_url': resp.get('payment_url')})
        return Response(data, status=status.HTTP_201_CREATED)


class WebhookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, provider):
        # Provider will POST a payload containing intent id and status and reference
        intent_id = request.data.get('intent_id')
        status_val = request.data.get('status')
        reference = request.data.get('reference')
        pi = get_object_or_404(PaymentIntent, id=intent_id, provider=provider)
        if status_val == 'completed':
            pi.status = 'completed'
            pi.reference = reference
            pi.save()
            # credit wallet
            wallet, _ = Wallet.objects.get_or_create(user=pi.user)
            # create transaction
            Transaction.objects.create(wallet=wallet, amount_cents=pi.amount_cents, type='deposit', status='completed', reference=reference)
            # increase balance
            wallet.balance_cents += pi.amount_cents
            wallet.save(update_fields=['balance_cents'])
            return Response({'detail': 'ok'})
        else:
            pi.status = status_val
            pi.reference = reference
            pi.save()
            return Response({'detail': 'ignored'})
