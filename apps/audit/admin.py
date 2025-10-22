from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'actor', 'action', 'model', 'object_id', 'ip_address')
    list_filter = ('action', 'model')
    search_fields = ('actor__email', 'path', 'model', 'object_id', 'user_agent')
    readonly_fields = ('actor', 'action', 'model', 'object_id', 'path', 'method', 'ip_address', 'user_agent', 'changes', 'created_at')
