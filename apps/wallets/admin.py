from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from django.utils.safestring import mark_safe
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_cents', 'currency', 'created_at')
    change_list_template = "admin/wallets/wallet_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('adjust/', self.admin_site.admin_view(self.adjust_balance_view), name='wallet-adjust'),
        ]
        return custom + urls

    class AdjustForm(forms.Form):
        wallet_id = forms.ModelChoiceField(queryset=Wallet.objects.select_related('user').all(), label='Wallet')
        amount_cents = forms.IntegerField(label='Amount (cents)')
        reason = forms.CharField(required=False, widget=forms.Textarea, label='Reason')
        status = forms.ChoiceField(choices=[('completed','Completed'),('pending','Pending')], initial='completed')
        type = forms.ChoiceField(choices=[('deposit','Credit (+)'),('withdraw','Debit (-)')], initial='deposit')

    def adjust_balance_view(self, request):
        if request.method == 'POST':
            form = self.AdjustForm(request.POST)
            if form.is_valid():
                wallet: Wallet = form.cleaned_data['wallet_id']
                amount_cents = form.cleaned_data['amount_cents']
                tx_type = form.cleaned_data['type']
                status = form.cleaned_data['status']
                reason = form.cleaned_data['reason']

                # Create transaction first
                tx = Transaction.objects.create(
                    wallet=wallet,
                    type='deposit' if tx_type == 'deposit' else 'withdraw',
                    amount_cents=amount_cents,
                    status=status,
                    meta={'admin_reason': reason, 'by': request.user.id},
                )
                # Apply balance only if completed
                if status == 'completed':
                    if tx_type == 'deposit':
                        wallet.balance_cents = (wallet.balance_cents or 0) + amount_cents
                    else:
                        wallet.balance_cents = (wallet.balance_cents or 0) - amount_cents
                    wallet.save(update_fields=['balance_cents'])

                messages.success(request, mark_safe(f"Adjustment created for <b>{wallet.user.email}</b>: {amount_cents} cents ({tx_type})."))
                return redirect('admin:wallets_wallet_changelist')
        else:
            form = self.AdjustForm()
        context = dict(
            self.admin_site.each_context(request),
            title='Adjust Wallet Balance',
            form=form,
        )
        return render(request, 'admin/wallets/adjust_balance.html', context)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'type', 'amount_cents', 'status', 'created_at')
    list_filter = ('type', 'status')
