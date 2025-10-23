from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Page


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Page.objects.filter(published=True)

    def location(self, obj):
        # Assuming your frontend serves pages at /pages/<slug>/
        return f"/pages/{obj.slug}/"


sitemaps = {
    'pages': PageSitemap,
}
