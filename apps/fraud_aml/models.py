from django.db import models


class IPBlock(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IPBlock({self.ip_address}) active={self.active}"


class CountryRestriction(models.Model):
    country_code = models.CharField(max_length=2, unique=True)
    blocked = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CountryRestriction({self.country_code}) blocked={self.blocked}"
