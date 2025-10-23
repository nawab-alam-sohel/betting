from django.contrib import admin
from django.utils import timezone
from .models import Agent, AgentCommission, AgentPayout


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'parent', 'approved', 'is_blocked', 'created_at')
    search_fields = ('name', 'user__email')
    list_filter = ('approved', 'is_blocked')
    actions = ['approve_agents', 'block_agents', 'unblock_agents']

    def approve_agents(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"Approved {updated} agent(s)")
    approve_agents.short_description = "Approve selected agents"

    def block_agents(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f"Blocked {updated} agent(s)")
    block_agents.short_description = "Block selected agents"

    def unblock_agents(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f"Unblocked {updated} agent(s)")
    unblock_agents.short_description = "Unblock selected agents"


@admin.register(AgentCommission)
class AgentCommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'percentage', 'created_at')


@admin.register(AgentPayout)
class AgentPayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'amount_cents', 'status', 'requested_at', 'processed_at')
    list_filter = ('status',)
    actions = ['approve_payouts', 'reject_payouts']

    def approve_payouts(self, request, queryset):
        updated = queryset.update(status='approved', processed_at=timezone.now())
        self.message_user(request, f"Approved {updated} payout(s)")
    approve_payouts.short_description = "Approve selected payouts"

    def reject_payouts(self, request, queryset):
        updated = queryset.update(status='rejected', processed_at=timezone.now())
        self.message_user(request, f"Rejected {updated} payout(s)")
    reject_payouts.short_description = "Reject selected payouts"
