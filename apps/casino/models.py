from django.db import models
from django.conf import settings


class CasinoProvider(models.Model):
    key = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    base_url = models.URLField(blank=True)
    # Arbitrary provider configuration (API keys, secrets, endpoints, launch options)
    config = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class CasinoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Casino categories"

    def __str__(self):
        return self.name


class CasinoGame(models.Model):
    provider = models.ForeignKey(CasinoProvider, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    provider_game_id = models.CharField(max_length=100, db_index=True)
    thumbnail_url = models.URLField(blank=True)
    rtp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    volatility = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(CasinoCategory, related_name='games', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("provider", "provider_game_id")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.provider.name})"


class CasinoSession(models.Model):
    STATUS = (
        ("active", "Active"),
        ("ended", "Ended"),
        ("failed", "Failed"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='casino_sessions')
    game = models.ForeignKey(CasinoGame, on_delete=models.CASCADE, related_name='sessions')
    provider_session_id = models.CharField(max_length=100, blank=True)
    launch_url = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.user} - {self.game}"
