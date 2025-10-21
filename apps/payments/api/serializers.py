from rest_framework import serializers
from apps.payments.models import PaymentIntent


class PaymentIntentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = PaymentIntent
        fields = ('id', 'provider', 'amount_cents', 'amount', 'currency', 'flow', 'status', 'reference', 'created_at')

    def get_amount(self, obj):
        return f"{(obj.amount_cents/100):.2f}"
