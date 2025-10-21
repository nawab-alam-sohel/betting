from django.contrib import admin
from .models_recon import PaymentProvider, WithdrawalRequest


@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'display_number', 'active')


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_cents', 'provider', 'status', 'created_at')
    list_filter = ('status', 'provider')
    search_fields = ('user__email', 'provider_account', 'reference')
