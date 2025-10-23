from django.http import HttpResponse
from .models import SiteSetting


def robots_txt(_request):
    content = SiteSetting.objects.order_by('-updated_at').values_list('robots_txt', flat=True).first() or ''
    return HttpResponse(content, content_type='text/plain')
