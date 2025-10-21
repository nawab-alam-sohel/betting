from django.contrib import admin
from .models import Agent, AgentCommission


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'parent', 'created_at')
    search_fields = ('name', 'user__email')


@admin.register(AgentCommission)
class AgentCommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'percentage', 'created_at')
