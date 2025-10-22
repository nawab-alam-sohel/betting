from rest_framework import serializers
from apps.cms.models import Page, SiteSetting


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = [
            "site_name",
            "default_locale",
            "ga_measurement_id",
            "meta_pixel_id",
            "seo_default_title",
            "seo_default_description",
            "robots_txt",
            "custom_css",
            "homepage_title",
            "homepage_subtitle",
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "slug",
            "title_en",
            "title_bn",
            "meta_description_en",
            "meta_description_bn",
            "content_en",
            "content_bn",
            "published",
        ]
