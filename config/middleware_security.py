from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

from apps.fraud_aml.models import IPBlock, CountryRestriction
from apps.cms.models import SiteSetting


class IPBlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if not ip:
            return None
        if IPBlock.objects.filter(ip_address=ip, active=True).exists():
            return HttpResponse('Your IP is blocked.', status=403)
        return None


class CountryRestrictionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # In production, integrate a GeoIP resolver; for now, use header if present
        country = request.META.get('HTTP_X_COUNTRY_CODE') or request.headers.get('X-Country-Code')
        if not country:
            return None
        country = country.upper()
        if CountryRestriction.objects.filter(country_code=country, blocked=True).exists():
            return HttpResponse('Access from your country is restricted.', status=451)
        return None


class MaintenanceModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Allow admin and staff to bypass maintenance
        user = getattr(request, 'user', AnonymousUser())
        path = request.path or ''
        if path.startswith('/admin'):
            return None
        # Use the latest SiteSetting
        setting = SiteSetting.objects.order_by('-updated_at').first()
        if setting and getattr(setting, 'maintenance_mode', False):
            if user.is_authenticated and user.is_staff:
                return None
            return HttpResponse('Site under maintenance. Please check back later.', status=503)
        return None
