from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django import forms
from apps.cms.models import SiteSetting


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'default_locale', 'ga_measurement_id', 'meta_pixel_id',
            'maintenance_mode', 'seo_default_title', 'seo_default_description',
            'robots_txt', 'custom_css', 'homepage_title', 'homepage_subtitle'
        ]
        widgets = {
            'seo_default_description': forms.Textarea(attrs={'rows': 3}),
            'robots_txt': forms.Textarea(attrs={'rows': 3}),
            'custom_css': forms.Textarea(attrs={'rows': 5, 'class': 'font-monospace'}),
        }


@staff_member_required
def site_settings_form(request):
    setting = SiteSetting.objects.order_by('-updated_at').first() or SiteSetting()
    form = SiteSettingForm(instance=setting)
    return render(request, 'admin/system/site_settings_form.html', {'form': form})


@staff_member_required
@require_http_methods(["POST"])
def site_settings_save(request):
    setting = SiteSetting.objects.order_by('-updated_at').first() or SiteSetting()
    form = SiteSettingForm(request.POST, instance=setting)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Site settings saved"})
    response = render(request, 'admin/system/site_settings_form.html', {'form': form})
    response.status_code = 400
    return response
