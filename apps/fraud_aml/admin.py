from django.contrib import admin
from .models import IPBlock, CountryRestriction


@admin.register(IPBlock)
class IPBlockAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'active', 'reason', 'created_at')
    list_filter = ('active',)
    search_fields = ('ip_address', 'reason')


@admin.register(CountryRestriction)
class CountryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('country_code', 'blocked', 'reason', 'created_at')
    list_filter = ('blocked',)
    search_fields = ('country_code', 'reason')
