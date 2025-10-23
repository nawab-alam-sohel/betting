from django.contrib import admin
from .models import SMSTemplate, EmailTemplate, NotificationLog, InAppNotification
from django.utils.safestring import mark_safe
import json


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "template_key", "is_active", "updated_at")
    search_fields = ("name", "template_key", "content")
    list_filter = ("is_active",)
    ordering = ("name",)
    prepopulated_fields = {"template_key": ("name",)}
    fieldsets = (
        (None, {
            "fields": ("name", "template_key", "content", "is_active"),
        }),
    )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "template_key", "is_active", "updated_at")
    search_fields = ("name", "template_key", "subject")
    list_filter = ("is_active",)
    ordering = ("name",)
    prepopulated_fields = {"template_key": ("name",)}
    fieldsets = (
        (None, {
            "fields": ("name", "template_key", "subject", "html_content", "text_content", "is_active"),
        }),
    )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "notification_type",
        "recipient",
        "phone_number",
        "email",
        "template_key",
        "status",
        "created_at",
    )
    list_filter = ("notification_type", "status", "created_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    search_fields = (
        "template_key",
        "provider_message_id",
        "recipient__username",
        "recipient__email",
        "phone_number",
        "email",
        "error_message",
    )
    readonly_fields = (
        "notification_type",
        "recipient",
        "phone_number",
        "email",
        "template_key",
        "_pretty_context",
        "status",
        "error_message",
        "provider_message_id",
        "content_type",
        "object_id",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("Notification", {
            "fields": (
                "notification_type", "recipient", "phone_number", "email", "template_key", "status",
            )
        }),
        ("Context", {
            "fields": ("_pretty_context",),
        }),
        ("Delivery", {
            "fields": ("provider_message_id", "error_message"),
        }),
        ("Relation", {
            "fields": ("content_type", "object_id"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Read-only log entries
        return False

    def has_delete_permission(self, request, obj=None):
        # Keep logs immutable from admin
        return False

    def _pretty_context(self, obj):
        try:
            return mark_safe(f"<pre style='white-space:pre-wrap'>{json.dumps(obj.context_data, indent=2, ensure_ascii=False)}</pre>")
        except Exception:
            return str(obj.context_data)
    _pretty_context.short_description = "Context Data"


@admin.register(InAppNotification)
class InAppNotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "notification_type", "title", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("title", "message", "recipient__username", "recipient__email")
    actions = ("mark_as_read", "mark_as_unread")

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"Marked {updated} notification(s) as read")
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"Marked {updated} notification(s) as unread")
    mark_as_unread.short_description = "Mark selected as unread"
