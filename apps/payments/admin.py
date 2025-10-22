from django.contrib import admin
from django.utils import timezone
from .models_recon import PaymentProvider, WithdrawalRequest
from .models import PaymentIntent


@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'display_number', 'active')


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_cents', 'provider', 'status', 'created_at')
    list_filter = ('status', 'provider')
    search_fields = ('user__email', 'provider_account', 'reference')
    actions = ['approve_withdrawals', 'reject_withdrawals']

    def approve_withdrawals(self, request, queryset):
        updated = queryset.update(status='approved', processed_at=timezone.now())
        self.message_user(request, f"Approved {updated} withdrawal(s)")
    approve_withdrawals.short_description = "Approve selected withdrawals"

    def reject_withdrawals(self, request, queryset):
        updated = queryset.update(status='rejected', processed_at=timezone.now())
        self.message_user(request, f"Rejected {updated} withdrawal(s)")
    reject_withdrawals.short_description = "Reject selected withdrawals"


@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'provider', 'amount_cents', 'currency', 'status', 'created_at')
    list_filter = ('status', 'provider', 'currency')
    search_fields = ('user__email', 'reference')
    actions = ['mark_completed', 'mark_failed', 'mark_pending']

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"Marked {updated} deposit(s) as completed")
    mark_completed.short_description = "Mark selected as completed"

    def mark_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f"Marked {updated} deposit(s) as failed")
    mark_failed.short_description = "Mark selected as failed"

    def mark_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f"Marked {updated} deposit(s) as pending")
    mark_pending.short_description = "Mark selected as pending"
