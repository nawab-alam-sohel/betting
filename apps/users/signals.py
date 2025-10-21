from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    Role = apps.get_model('users', 'Role')
    # check if roles exist before creating
    default_roles = [
        {'name': 'Super Admin', 'slug': 'superadmin', 'level': 100},
        {'name': 'Admin', 'slug': 'admin', 'level': 80},
        {'name': 'Agent', 'slug': 'agent', 'level': 50},
        {'name': 'User', 'slug': 'user', 'level': 10},
    ]
    for r in default_roles:
        Role.objects.get_or_create(slug=r['slug'], defaults={'name': r['name'], 'level': r['level']})
