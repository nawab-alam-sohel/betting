from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.cms.models import Page, SiteSetting
from apps.cms.api.serializers import PageSerializer, SiteSettingSerializer


class CmsHealthView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"status": "ok", "module": "cms"})


class SiteSettingView(APIView):
    # Public GET; admin required for write
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request):
        setting = SiteSetting.objects.order_by('-updated_at').first()
        if not setting:
            # return empty defaults
            return Response(SiteSettingSerializer(SiteSetting()).data)
        return Response(SiteSettingSerializer(setting).data)

    def put(self, request):
        setting = SiteSetting.objects.order_by('-updated_at').first() or SiteSetting()
        s = SiteSettingSerializer(instance=setting, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        setting = s.save()
        return Response(SiteSettingSerializer(setting).data)


class PageDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, slug: str):
        try:
            page = Page.objects.get(slug=slug, published=True)
        except Page.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(PageSerializer(page).data)
