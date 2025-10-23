from django.contrib import admin
from django.db.models import Q
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        try:
            role_slug = user.role.slug if user.role else None
        except Exception:
            role_slug = None
        # Super Admin sees all
        if user.is_superuser or role_slug == 'superadmin':
            return qs
        # Admin cannot see Super Admins
        if role_slug == 'admin':
            return qs.exclude(Q(is_superuser=True) | Q(role__slug='superadmin'))
        # Agent: only see own downline/clients (direct clients)
        if role_slug == 'agent':
            agent_profile = getattr(user, 'agent_profile', None)
            if agent_profile:
                return qs.filter(agent=agent_profile)
            return qs.none()
        # Others: no access in admin
        return qs.none()

    def has_add_permission(self, request):
        user = request.user
        role_slug = getattr(getattr(user, 'role', None), 'slug', None)
        if user.is_superuser or role_slug == 'superadmin':
            return True
        if role_slug == 'admin':
            return True
        if role_slug == 'agent':
            # Agents can add user accounts only
            return True
        return False

    def has_change_permission(self, request, obj=None):
        user = request.user
        role_slug = getattr(getattr(user, 'role', None), 'slug', None)
        if user.is_superuser or role_slug == 'superadmin':
            return True
        if obj:
            if role_slug == 'admin' and (obj.is_superuser or getattr(getattr(obj, 'role', None), 'slug', None) == 'superadmin'):
                return False
            if role_slug == 'agent':
                agent_profile = getattr(user, 'agent_profile', None)
                return agent_profile and obj.agent_id == agent_profile.id
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Mirror change permission
        return self.has_change_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Limit Role choices based on actor role
        user = request.user
        role_slug = getattr(getattr(user, 'role', None), 'slug', None)
        if 'role' in form.base_fields:
            role_field = form.base_fields['role']
            if user.is_superuser or role_slug == 'superadmin':
                pass
            elif role_slug == 'admin':
                role_field.queryset = Role.objects.exclude(slug='superadmin')
            elif role_slug == 'agent':
                role_field.queryset = Role.objects.filter(slug__in=['user'])
        return form

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
