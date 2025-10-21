from rest_framework import serializers
from apps.agents.models import Agent, AgentCommission
from apps.wallets.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    wallet_user = serializers.CharField(source='wallet.user.email', read_only=True)
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'wallet_user', 'amount_cents', 'amount', 'type', 'status', 'reference', 'created_at')

    def get_amount(self, obj):
        return f"{(obj.amount_cents/100):.2f}"


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('id', 'name', 'user', 'parent')


class AgentCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentCommission
        fields = ('id', 'agent', 'percentage', 'created_at')
