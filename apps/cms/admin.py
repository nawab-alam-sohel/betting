from django.contrib import admin
from apps.cms.models import (
    SiteSetting, Page,
    SeoSetting, PaymentSetting, SocialLoginSetting,
    LanguageSetting, ExtensionSetting, CronJobSetting,
    GDPRCookieSetting,
)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "default_locale", "maintenance_mode", "ga_measurement_id", "meta_pixel_id", "updated_at")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("slug", "published", "updated_at")
    list_filter = ("published",)
    search_fields = ("slug", "title_en", "title_bn")


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow a single row for these models
        return False


@admin.register(SeoSetting)
class SeoSettingAdmin(SingletonAdmin):
    list_display = ("default_title", "updated_at")


@admin.register(PaymentSetting)
class PaymentSettingAdmin(SingletonAdmin):
    list_display = ("provider", "active", "updated_at")


@admin.register(SocialLoginSetting)
class SocialLoginSettingAdmin(SingletonAdmin):
    list_display = ("google_enabled", "facebook_enabled", "updated_at")


@admin.register(LanguageSetting)
class LanguageSettingAdmin(SingletonAdmin):
    list_display = ("default_language", "updated_at")


@admin.register(ExtensionSetting)
class ExtensionSettingAdmin(SingletonAdmin):
    list_display = ("sportsbook_enabled", "casino_enabled", "realtime_enabled", "updated_at")


@admin.register(CronJobSetting)
class CronJobSettingAdmin(SingletonAdmin):
    list_display = ("jobs_enabled", "sports_fetch_schedule", "backup_schedule", "updated_at")


@admin.register(GDPRCookieSetting)
class GDPRCookieSettingAdmin(SingletonAdmin):
    list_display = ("enabled", "title", "updated_at")
