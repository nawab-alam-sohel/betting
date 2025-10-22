from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportsProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('base_url', models.URLField(blank=True)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
