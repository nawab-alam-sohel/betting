from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=120, default="VelkiList")
    default_locale = models.CharField(max_length=5, default="en")
    logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True)
    ga_measurement_id = models.CharField(max_length=32, blank=True, null=True)
    meta_pixel_id = models.CharField(max_length=32, blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)
    # SEO & front-end controls
    seo_default_title = models.CharField(max_length=200, blank=True, default="")
    seo_default_description = models.TextField(blank=True, default="")
    robots_txt = models.TextField(blank=True, default="")
    custom_css = models.TextField(blank=True, default="")
    homepage_title = models.CharField(max_length=200, blank=True, default="")
    homepage_subtitle = models.CharField(max_length=300, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name


class Page(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    title_en = models.CharField(max_length=200)
    title_bn = models.CharField(max_length=200, blank=True)
    meta_description_en = models.TextField(blank=True)
    meta_description_bn = models.TextField(blank=True)
    content_en = models.TextField(blank=True)
    content_bn = models.TextField(blank=True)
    published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug


class SingletonBase(models.Model):
    """Simple base to hint singleton semantics in admin: one row table."""
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SeoSetting(SingletonBase):
    default_title = models.CharField(max_length=200, blank=True, default="")
    default_description = models.TextField(blank=True, default="")
    meta_keywords = models.TextField(blank=True, default="")
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)

    def __str__(self):
        return "SEO Settings"


class PaymentSetting(SingletonBase):
    provider = models.CharField(max_length=50, blank=True, default="manual")
    config = models.JSONField(blank=True, null=True, default=dict)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment: {self.provider or 'manual'}"


class SocialLoginSetting(SingletonBase):
    google_enabled = models.BooleanField(default=False)
    google_client_id = models.CharField(max_length=200, blank=True, default="")
    google_client_secret = models.CharField(max_length=200, blank=True, default="")
    facebook_enabled = models.BooleanField(default=False)
    facebook_app_id = models.CharField(max_length=200, blank=True, default="")
    facebook_app_secret = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return "Social Login"


class LanguageSetting(SingletonBase):
    default_language = models.CharField(max_length=10, default="en")
    supported_languages = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f"Language: {self.default_language}"


class ExtensionSetting(SingletonBase):
    sportsbook_enabled = models.BooleanField(default=True)
    casino_enabled = models.BooleanField(default=True)
    realtime_enabled = models.BooleanField(default=True)
    reports_enabled = models.BooleanField(default=True)

    def __str__(self):
        return "Extensions"


class CronJobSetting(SingletonBase):
    jobs_enabled = models.BooleanField(default=True)
    sports_fetch_schedule = models.CharField(max_length=50, blank=True, default="*/5 * * * *")
    odds_fetch_schedule = models.CharField(max_length=50, blank=True, default="*/10 * * * *")
    backup_schedule = models.CharField(max_length=50, blank=True, default="0 2 * * *")

    def __str__(self):
        return "Cron Jobs"


class GDPRCookieSetting(SingletonBase):
    enabled = models.BooleanField(default=False)
    title = models.CharField(max_length=120, default="We value your privacy")
    message = models.TextField(blank=True, default="We use cookies to enhance your experience. By continuing, you agree to our cookie policy.")
    policy_url = models.CharField(max_length=255, blank=True, default="/pages/privacy-policy")

    def __str__(self):
        return "GDPR Cookie"
