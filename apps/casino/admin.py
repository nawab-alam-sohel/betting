from django.contrib import admin
from .models import CasinoProvider, CasinoCategory, CasinoGame, CasinoSession


@admin.register(CasinoProvider)
class CasinoProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "active", "display_order")
    list_filter = ("active",)
    search_fields = ("name", "key")
    ordering = ("display_order", "name")


@admin.register(CasinoCategory)
class CasinoCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name", "slug")
    ordering = ("order", "name")


@admin.register(CasinoGame)
class CasinoGameAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "slug", "active")
    list_filter = ("active", "provider")
    search_fields = ("name", "slug", "provider_game_id")
    filter_horizontal = ("categories",)
    ordering = ("name",)


@admin.register(CasinoSession)
class CasinoSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "game", "status", "created_at")
    list_filter = ("status", "game__provider")
    search_fields = ("provider_session_id", "user__username", "game__name")
    ordering = ("-created_at",)
