from django.contrib import admin
from django.apps import apps as django_apps


def register_unregistered_models():
    """Auto-register any models from local apps that are not yet in the admin site.

    This runs after admin.autodiscover (invoked by including admin.site.urls),
    so it won't clobber custom ModelAdmin classes defined in app admin.py files.
    """
    local_prefix = 'apps.'
    # Collect app labels for local apps only
    local_app_labels = set()
    for ac in django_apps.get_app_configs():
        if ac.name.startswith(local_prefix):
            local_app_labels.add(ac.label)

    # Register any model with default ModelAdmin if not already present
    for model in django_apps.get_models():
        if model._meta.app_label not in local_app_labels:
            continue
        if model in admin.site._registry:
            continue
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            # In case of race or multiple calls, ignore
            pass
