from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=120, default="VelkiList")
    default_locale = models.CharField(max_length=5, default="en")
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
