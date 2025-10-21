from rest_framework import serializers
from apps.wallets.models import Wallet, Transaction
from decimal import Decimal


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'currency']

    def get_balance(self, obj):
        # return string to match previous responses
        return format(obj.balance, '.2f')


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'reference', 'status', 'created_at']

    def get_amount(self, obj):
        return format(Decimal(obj.amount_cents) / Decimal(100), '.2f')
