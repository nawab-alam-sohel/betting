from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # System settings dashboard
    path('system/settings/', views.settings_dashboard, name='settings_dashboard'),
    path('system/site-settings/', views.site_settings_form, name='site_settings_form'),
    path('system/site-settings/save/', views.site_settings_save, name='site_settings_save'),
    # SEO settings
    path('system/settings/seo/', views.seo_settings_form, name='seo_settings_form'),
    path('system/settings/seo/save/', views.seo_settings_save, name='seo_settings_save'),
    # Payment
    path('system/settings/payment/', views.payment_settings_form, name='payment_settings_form'),
    path('system/settings/payment/save/', views.payment_settings_save, name='payment_settings_save'),
    # Social Login
    path('system/settings/social/', views.social_settings_form, name='social_settings_form'),
    path('system/settings/social/save/', views.social_settings_save, name='social_settings_save'),
    # Language
    path('system/settings/language/', views.language_settings_form, name='language_settings_form'),
    path('system/settings/language/save/', views.language_settings_save, name='language_settings_save'),
    # Extensions
    path('system/settings/extensions/', views.extension_settings_form, name='extension_settings_form'),
    path('system/settings/extensions/save/', views.extension_settings_save, name='extension_settings_save'),
    # Cron jobs
    path('system/settings/cron/', views.cron_settings_form, name='cron_settings_form'),
    path('system/settings/cron/save/', views.cron_settings_save, name='cron_settings_save'),
]
