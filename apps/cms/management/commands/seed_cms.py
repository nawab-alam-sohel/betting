from django.core.management.base import BaseCommand
from apps.cms.models import SiteSetting, Page


class Command(BaseCommand):
    help = "Seed CMS settings and demo pages with bn/en content"

    def handle(self, *args, **options):
        SiteSetting.objects.update_or_create(
            id=1,
            defaults=dict(
                site_name="VelkiList",
                default_locale="bn",
                ga_measurement_id="G-XXXXXXX",
                meta_pixel_id="1234567890",
            ),
        )

        Page.objects.update_or_create(
            slug="home",
            defaults=dict(
                title_en="Welcome to VelkiList",
                title_bn="ভেলকি-লিস্টে স্বাগতম",
                meta_description_en="Betting and casino platform.",
                meta_description_bn="বেটিং এবং ক্যাসিনো প্ল্যাটফর্ম।",
                content_en="Home page content",
                content_bn="হোম পেজ কনটেন্ট",
                published=True,
            ),
        )

        Page.objects.update_or_create(
            slug="sportsbook",
            defaults=dict(
                title_en="Sportsbook",
                title_bn="স্পোর্টসবুক",
                meta_description_en="Live and upcoming matches.",
                meta_description_bn="লাইভ এবং আসন্ন ম্যাচ।",
                content_en="Sportsbook page",
                content_bn="স্পোর্টসবুক পেজ",
                published=True,
            ),
        )

        self.stdout.write(self.style.SUCCESS("CMS seed completed."))
