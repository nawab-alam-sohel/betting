from django.db import migrations

def seed_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    defaults = [
        {"name": "Super Admin", "slug": "superadmin", "level": 100},
        {"name": "Admin", "slug": "admin", "level": 80},
        {"name": "Agent", "slug": "agent", "level": 50},
        {"name": "User", "slug": "user", "level": 10},
    ]
    for d in defaults:
        Role.objects.get_or_create(slug=d["slug"], defaults=d)


def unseed_roles(apps, schema_editor):
    # Don't delete roles on reverse to avoid data loss
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_email_verified_user_is_banned_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_roles, reverse_code=unseed_roles),
    ]
