from rest_framework import serializers
from apps.payments.models_recon import (
    PaymentProvider, WithdrawalRequest, ReconciliationBatch,
    ReconciliationItem, ReconciliationReport
)


class ReconciliationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationItem
        fields = [
            'id', 'transaction_id', 'transaction_type', 'amount_cents',
            'provider_reference', 'provider_status', 'our_status',
            'status', 'created_at', 'updated_at', 'notes'
        ]


class ReconciliationBatchSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    mismatched_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ReconciliationBatch
        fields = [
            'id', 'provider', 'start_date', 'end_date', 'status',
            'items_count', 'mismatched_count', 'created_at',
            'updated_at', 'notes'
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()
    
    def get_mismatched_count(self, obj):
        return obj.items.filter(status='mismatched').count()


class ReconciliationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationReport
        fields = [
            'id', 'batch', 'total_transactions', 'matched_count',
            'mismatched_count', 'missing_count', 'extra_count',
            'total_amount_cents', 'mismatched_amount_cents',
            'generated_at', 'report_data', 'summary'
        ]


class PaymentProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = ('id', 'key', 'name', 'display_number', 'instructions', 'active')


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = WithdrawalRequest
        fields = ('id', 'user', 'user_email', 'amount_cents', 'provider', 'provider_account', 'reference', 'status', 'admin_comments', 'created_at', 'processed_at')
        read_only_fields = ('user', 'status', 'processed_at')
