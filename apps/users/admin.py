from django.contrib import admin
from .models import Role, User
from .models_kyc import KYCDocument, KYCProfile, LoginAttempt, UserDevice
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'level', 'parent')
    prepopulated_fields = {"slug": ("name",)}

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'email_verified', 'phone_verified', 'is_banned', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role', 'email_verified', 'phone_verified', 'is_banned')
    ordering = ('email',)
    search_fields = ('email', 'full_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'role', 'email_verified', 'phone_verified', 'is_banned')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'role', 'email_verified', 'phone_verified', 'is_banned', 'is_staff', 'is_active')}),
    )

admin.site.register(User, UserAdmin)


@admin.register(KYCDocument)
class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'created_at', 'verified_by', 'verified_at')
    list_filter = ('status', 'document_type')
    search_fields = ('user__email', 'document_number')
    actions = ['approve_kyc', 'reject_kyc']

    def approve_kyc(self, request, queryset):
        updated = queryset.update(status='approved', verified_by=request.user, verified_at=timezone.now())
        self.message_user(request, f"Approved {updated} KYC document(s)")
    approve_kyc.short_description = "Approve selected KYC documents"

    def reject_kyc(self, request, queryset):
        updated = queryset.update(status='rejected', verified_by=request.user, verified_at=timezone.now())
        self.message_user(request, f"Rejected {updated} KYC document(s)")
    reject_kyc.short_description = "Reject selected KYC documents"


@admin.register(KYCProfile)
class KYCProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_level', 'country_of_residence', 'created_at')
    list_filter = ('verification_level', 'country_of_residence')
    search_fields = ('user__email',)


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'status', 'attempted_at', 'location', 'device_id')
    list_filter = ('status',)
    search_fields = ('user__email', 'ip_address', 'device_id')


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'os_type', 'browser', 'ip_address', 'is_trusted', 'last_used')
    list_filter = ('is_trusted', 'os_type')
    search_fields = ('user__email', 'device_name', 'ip_address')
