from django.contrib import admin
from apps.cms.models import SiteSetting, Page


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "default_locale", "maintenance_mode", "ga_measurement_id", "meta_pixel_id", "updated_at")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("slug", "published", "updated_at")
    list_filter = ("published",)
    search_fields = ("slug", "title_en", "title_bn")
