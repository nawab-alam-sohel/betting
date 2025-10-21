from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction
from apps.wallets.api.serializers import WalletSerializer, TransactionSerializer
from apps.wallets.models import Wallet, Transaction


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if amount is None:
            return Response({'error': 'amount required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # convert to cents
            cents = int(float(amount) * 100)
        except Exception:
            return Response({'error': 'invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            wallet, _ = Wallet.objects.select_for_update().get_or_create(user=request.user)
            txn = Transaction.objects.create(wallet=wallet, amount_cents=cents, type='deposit', status='completed')
            wallet.balance_cents = wallet.balance_cents + cents
            wallet.save()
        serializer = TransactionSerializer(txn)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        txns = wallet.transactions.all().order_by('-created_at')
        serializer = TransactionSerializer(txns, many=True)
        return Response(serializer.data)
