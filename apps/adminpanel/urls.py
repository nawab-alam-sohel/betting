from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('site-settings/', views.site_settings_form, name='site_settings_form'),
    path('site-settings/save/', views.site_settings_save, name='site_settings_save'),
]
