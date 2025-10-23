from django.contrib import admin
from django.db import models
from django.utils import timezone
from .models_recon import PaymentProvider, WithdrawalRequest
from .models import PaymentIntent
from .models_proxy import (
    PaymentIntentPending,
    PaymentIntentCompleted,
    PaymentIntentFailed,
    WithdrawalRequestPending,
    WithdrawalRequestApproved,
    WithdrawalRequestRejected,
)


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


class FilteredPaymentIntentAdmin(PaymentIntentAdmin):
    desired_status = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.desired_status:
            return qs.filter(status=self.desired_status)
        return qs

    def has_add_permission(self, request):
        return False

    # Custom list/detail UX for Pending Deposits only
    change_list_template = None

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        # Only attach custom views for pending deposits admin
        if getattr(self, 'desired_status', None) == 'pending':
            custom = [
                path('details/<int:pk>/', self.admin_site.admin_view(self.pending_detail_view), name='payments_paymentintentpending_details'),
                path('details/demo/<int:idx>/', self.admin_site.admin_view(self.pending_demo_detail_view), name='payments_paymentintentpending_demo_details'),
            ]
            return custom + urls
        return urls

    def changelist_view(self, request, extra_context=None):
        # For pending only, render custom two-pane list UI
        if getattr(self, 'desired_status', None) == 'pending':
            from django.db.models import Count
            from django.template.response import TemplateResponse
            from django.utils.timezone import make_aware
            from django.core.paginator import Paginator
            from datetime import datetime

            qs = self.get_queryset(request)
            # Filters
            provider = request.GET.get('provider')
            q = request.GET.get('q')
            start = request.GET.get('start')
            end = request.GET.get('end')
            if provider:
                qs = qs.filter(provider=provider)
            if q:
                qs = qs.filter(
                    models.Q(reference__icontains=q) |
                    models.Q(user__email__icontains=q)
                )
            # Date range (optional)
            try:
                if start:
                    qs = qs.filter(created_at__gte=make_aware(datetime.fromisoformat(start)))
                if end:
                    qs = qs.filter(created_at__lte=make_aware(datetime.fromisoformat(end)))
            except Exception:
                pass

            demo = False
            # Pagination params
            try:
                per_page = int(request.GET.get('per_page', 15))
            except Exception:
                per_page = 15
            page_number = request.GET.get('page') or 1
            base_qs = self.get_queryset(request)
            if not base_qs.exists():
                demo = True
                demo_items = self._demo_deposits()
                # Provider filter in demo mode
                if provider:
                    demo_items = [d for d in demo_items if d.provider == provider]
                # Simple search by email or reference
                if q:
                    ql = q.lower()
                    demo_items = [d for d in demo_items if ql in (d.reference or '').lower() or ql in (d.user.email or '').lower()]
                # Date range filter
                try:
                    if start:
                        dt = make_aware(datetime.fromisoformat(start))
                        demo_items = [d for d in demo_items if d.created_at >= dt]
                    if end:
                        dt2 = make_aware(datetime.fromisoformat(end))
                        demo_items = [d for d in demo_items if d.created_at <= dt2]
                except Exception:
                    pass

                # Compute provider counts from full demo set (not filtered)
                from collections import Counter
                pc = Counter([d.provider for d in self._demo_deposits()])
                provider_counts = [{ 'provider': k, 'c': v } for k, v in pc.items()]
                objects = demo_items
                total_count = len(self._demo_deposits())
            else:
                provider_counts = base_qs.values('provider').annotate(c=Count('id')).order_by('provider')
                qs = qs.order_by('-created_at')
                paginator = Paginator(qs, per_page)
                page_obj = paginator.get_page(page_number)
                objects = list(page_obj.object_list)
                total_count = base_qs.count()
            # Build paginator in demo mode as well
            if demo:
                paginator = Paginator(objects, per_page)
                page_obj = paginator.get_page(page_number)
                objects = list(page_obj.object_list)
            # Build base querystring without 'page' to preserve filters in links
            qd = request.GET.copy()
            qd.pop('page', None)
            base_qs = qd.urlencode()
            # Range text (Showing X to Y of Z results)
            if paginator.count:
                results_from = page_obj.start_index()
                results_to = page_obj.end_index()
            else:
                results_from = 0
                results_to = 0
            ctx = {
                **self.admin_site.each_context(request),
                **(extra_context or {}),
                'title': 'Pending Deposits',
                'objects': objects,
                'provider_counts': provider_counts,
                'total_count': total_count,
                'selected_provider': provider or '',
                'search_q': q or '',
                'start': start or '',
                'end': end or '',
                'demo': demo,
                'is_paginated': paginator.num_pages > 1,
                'paginator': paginator,
                'page_obj': page_obj,
                'per_page': per_page,
                'base_qs': base_qs,
                'results_from': results_from,
                'results_to': results_to,
            }
            # Use custom template within admin chrome
            return TemplateResponse(request, 'admin/payments/pending_deposits_list.html', ctx)
        return super().changelist_view(request, extra_context)

    def pending_detail_view(self, request, pk):
        from django.shortcuts import get_object_or_404, redirect, render
        obj = get_object_or_404(PaymentIntent, pk=pk, status='pending')
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'approve':
                PaymentIntent.objects.filter(pk=obj.pk).update(status='completed')
                self.message_user(request, 'Deposit approved')
                return redirect('admin:payments_paymentintentpending_changelist')
            if action == 'reject':
                PaymentIntent.objects.filter(pk=obj.pk).update(status='failed')
                self.message_user(request, 'Deposit rejected')
                return redirect('admin:payments_paymentintentpending_changelist')
        ctx = {
            'title': f'Deposit by {obj.user}',
            'obj': obj,
        }
        return render(request, 'admin/payments/pending_deposit_detail.html', ctx)

    def pending_demo_detail_view(self, request, idx):
        from django.shortcuts import render
        demo_items = self._demo_deposits()
        try:
            obj = demo_items[int(idx)]
        except Exception:
            # Out of range; show first
            obj = demo_items[0]
        ctx = {
            'title': f'Deposit by {getattr(obj.user, "email", "demo")} (Demo)',
            'obj': obj,
            'demo': True,
        }
        return render(request, 'admin/payments/pending_deposit_detail.html', ctx)

    # ---- Demo data helpers ----
    def _demo_deposits(self):
        from types import SimpleNamespace as NS
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()

        def make(provider_key, provider_label, email, ref, amount_cents, days_ago, hours_offset=0):
            user = NS(email=email, get_full_name=lambda: email.split('@')[0].replace('.', ' ').title())
            created = now - timedelta(days=days_ago, hours=hours_offset)
            # Callable for template get_provider_display()
            return NS(
                provider=provider_key,
                get_provider_display=lambda: provider_label,
                reference=ref,
                created_at=created,
                user=user,
                amount_cents=amount_cents,
                currency='USD',
                pk=0,
            )

        return [
            make('bank', 'Bank Transfer', 'phungthuy@example.com', 'OCTO4PA4SOIL', 505000, 7, 2),
            make('mobile', 'Mobile Money', 'al.mamun@example.com', 'HSHJNMT5MNBI', 100058, 14),
            make('bank', 'Bank Transfer', 'val.jean@example.com', '5D9ARP5RZENA', 2334034, 30, 4),
            make('mobile', 'Mobile Money', 'vadim.ept@example.com', 'A1LQALWHJ4E', 505000, 30),
            make('bank', 'Bank Transfer', 'sagorika.ray@example.com', 'TWJQ9ENG90WV', 1010500, 30),
            make('bank', 'Bank Transfer', 'md.zahid@example.com', 'GA7SHGLLY6J', 505000, 60),
            make('bank', 'Bank Transfer', 'terrence@example.com', 'OJYSSD51A6C', 505000, 60),
            make('bank', 'Bank Transfer', 'carlos.silva@example.com', '5UWJZ2WW8RCD', 101500, 90),
        ]


@admin.register(PaymentIntentPending)
class PaymentIntentPendingAdmin(FilteredPaymentIntentAdmin):
    desired_status = 'pending'


@admin.register(PaymentIntentCompleted)
class PaymentIntentCompletedAdmin(FilteredPaymentIntentAdmin):
    desired_status = 'completed'


@admin.register(PaymentIntentFailed)
class PaymentIntentFailedAdmin(FilteredPaymentIntentAdmin):
    desired_status = 'failed'


class FilteredWithdrawalRequestAdmin(WithdrawalRequestAdmin):
    desired_status = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.desired_status:
            return qs.filter(status=self.desired_status)
        return qs

    def has_add_permission(self, request):
        return False


@admin.register(WithdrawalRequestPending)
class WithdrawalRequestPendingAdmin(FilteredWithdrawalRequestAdmin):
    desired_status = 'pending'


@admin.register(WithdrawalRequestApproved)
class WithdrawalRequestApprovedAdmin(FilteredWithdrawalRequestAdmin):
    desired_status = 'approved'


@admin.register(WithdrawalRequestRejected)
class WithdrawalRequestRejectedAdmin(FilteredWithdrawalRequestAdmin):
    desired_status = 'rejected'
