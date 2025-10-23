from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django import forms
from django.forms import forms as _unused_forms  # placeholder to keep imports minimal
from apps.cms.models import (
    SiteSetting,
    SeoSetting,
    PaymentSetting,
    SocialLoginSetting,
    LanguageSetting,
    ExtensionSetting,
    CronJobSetting,
)
from apps.payments.models_recon import WithdrawalRequest
from apps.payments.models import PaymentIntent
from apps.notifications.models import InAppNotification, NotificationLog
from apps.users.models_kyc import KYCDocument
from django.http import JsonResponse



class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'default_locale', 'logo', 'favicon', 'ga_measurement_id', 'meta_pixel_id',
            'maintenance_mode', 'seo_default_title', 'seo_default_description',
            'robots_txt', 'custom_css', 'homepage_title', 'homepage_subtitle'
        ]
        widgets = {
            'seo_default_description': forms.Textarea(attrs={'rows': 3}),
            'robots_txt': forms.Textarea(attrs={'rows': 3}),
            'custom_css': forms.Textarea(attrs={'rows': 5, 'class': 'font-monospace'}),
        }


class SeoSettingForm(forms.ModelForm):
    class Meta:
        model = SeoSetting
        fields = [
            'default_title', 'default_description', 'meta_keywords', 'og_image'
        ]
        widgets = {
            'default_description': forms.Textarea(attrs={'rows': 3}),
            'meta_keywords': forms.Textarea(attrs={'rows': 2}),
        }


class PaymentSettingForm(forms.ModelForm):
    class Meta:
        model = PaymentSetting
        fields = ['provider', 'config', 'active']


class SocialLoginSettingForm(forms.ModelForm):
    class Meta:
        model = SocialLoginSetting
        fields = [
            'google_enabled', 'google_client_id', 'google_client_secret',
            'facebook_enabled', 'facebook_app_id', 'facebook_app_secret',
        ]


class LanguageSettingForm(forms.ModelForm):
    class Meta:
        model = LanguageSetting
        fields = ['default_language', 'supported_languages']


class ExtensionSettingForm(forms.ModelForm):
    class Meta:
        model = ExtensionSetting
        fields = [
            'sportsbook_enabled', 'casino_enabled', 'realtime_enabled', 'reports_enabled'
        ]


class CronJobSettingForm(forms.ModelForm):
    class Meta:
        model = CronJobSetting
        fields = [
            'jobs_enabled', 'sports_fetch_schedule', 'odds_fetch_schedule',
            'backup_schedule'
        ]


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


# Generic helpers for settings modals
def _get_or_new(model_cls):
    obj = model_cls.objects.first()
    return obj if obj else model_cls()


@staff_member_required
def settings_dashboard(request):
    return render(request, 'admin/system/settings_dashboard.html')


@staff_member_required
def seo_settings_form(request):
    obj = _get_or_new(SeoSetting)
    form = SeoSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'SEO Configuration',
        'save_url': 'adminpanel:seo_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def seo_settings_save(request):
    obj = _get_or_new(SeoSetting)
    form = SeoSettingForm(request.POST, request.FILES, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "SEO settings saved"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'SEO Configuration', 'save_url': 'adminpanel:seo_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def payment_settings_form(request):
    obj = _get_or_new(PaymentSetting)
    form = PaymentSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'Payment Gateway',
        'save_url': 'adminpanel:payment_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def payment_settings_save(request):
    obj = _get_or_new(PaymentSetting)
    form = PaymentSettingForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Payment settings saved"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'Payment Gateway', 'save_url': 'adminpanel:payment_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def social_settings_form(request):
    obj = _get_or_new(SocialLoginSetting)
    form = SocialLoginSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'Social Login',
        'save_url': 'adminpanel:social_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def social_settings_save(request):
    obj = _get_or_new(SocialLoginSetting)
    form = SocialLoginSettingForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Social login settings saved"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'Social Login', 'save_url': 'adminpanel:social_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def language_settings_form(request):
    obj = _get_or_new(LanguageSetting)
    form = LanguageSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'Language',
        'save_url': 'adminpanel:language_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def language_settings_save(request):
    obj = _get_or_new(LanguageSetting)
    form = LanguageSettingForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Language settings saved"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'Language', 'save_url': 'adminpanel:language_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def extension_settings_form(request):
    obj = _get_or_new(ExtensionSetting)
    form = ExtensionSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'Extensions',
        'save_url': 'adminpanel:extension_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def extension_settings_save(request):
    obj = _get_or_new(ExtensionSetting)
    form = ExtensionSettingForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Extensions updated"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'Extensions', 'save_url': 'adminpanel:extension_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def cron_settings_form(request):
    obj = _get_or_new(CronJobSetting)
    form = CronJobSettingForm(instance=obj)
    return render(request, 'admin/system/settings_form.html', {
        'form': form,
        'title': 'Cron Jobs',
        'save_url': 'adminpanel:cron_settings_save',
    })


@staff_member_required
@require_http_methods(["POST"])
def cron_settings_save(request):
    obj = _get_or_new(CronJobSetting)
    form = CronJobSettingForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'admin/system/success_toast.html', {"message": "Cron settings saved"})
    resp = render(request, 'admin/system/settings_form.html', {'form': form, 'title': 'Cron Jobs', 'save_url': 'adminpanel:cron_settings_save'})
    resp.status_code = 400
    return resp


@staff_member_required
def dashboard(request):
    """Render the Jazzmin dashboard shell; data loads via internal API."""
    return render(request, 'admin/dashboard.html')


@staff_member_required
def system_settings(request):
    """
    Clean System Settings grid (BetLab style) with cards that link to
    the relevant admin pages. No modals or custom posts—keep it simple
    and unified inside Django admin.
    """
    return render(request, 'admin/system/settings_grid.html')


@staff_member_required
def payments_metrics(request):
    """Return JSON counts for deposits and withdrawals to power sidebar badges."""
    deposits = {
        'pending': PaymentIntent.objects.filter(status__iexact='pending').count(),
        'completed': PaymentIntent.objects.filter(status__iexact='completed').count(),
        'failed': PaymentIntent.objects.filter(status__iexact='failed').count(),
    }
    deposits['all'] = sum(deposits.values())

    withdrawals = {
        'pending': WithdrawalRequest.objects.filter(status__iexact='pending').count(),
        'approved': WithdrawalRequest.objects.filter(status__iexact='approved').count(),
        'rejected': WithdrawalRequest.objects.filter(status__iexact='rejected').count(),
    }
    withdrawals['all'] = sum(withdrawals.values())

    return JsonResponse({'deposits': deposits, 'withdrawals': withdrawals})


@staff_member_required
def notifications_metrics(request):
    """Return JSON counts for notifications to power sidebar badges."""
    inapp = {
        'unread': InAppNotification.objects.filter(is_read=False).count(),
        'all': InAppNotification.objects.all().count(),
    }
    logs = {
        'all': NotificationLog.objects.all().count(),
    }
    return JsonResponse({'inapp': inapp, 'logs': logs})


@staff_member_required
def users_metrics(request):
    """Return JSON counts for users-related metrics (e.g., KYC)."""
    kyc = {
        'pending': KYCDocument.objects.filter(status__iexact='pending').count(),
        'approved': KYCDocument.objects.filter(status__iexact='approved').count(),
        'rejected': KYCDocument.objects.filter(status__iexact='rejected').count(),
    }
    kyc['all'] = sum(kyc.values())
    return JsonResponse({'kyc': kyc})


"""
SPA-related helpers were removed to keep admin fully native per requirements.
"""
