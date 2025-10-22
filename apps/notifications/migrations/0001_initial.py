from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('template_key', models.SlugField(max_length=100, unique=True)),
                ('content', models.TextField(help_text='Use {variable} for placeholders. Example: Your OTP is {otp}')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('template_key', models.SlugField(max_length=100, unique=True)),
                ('subject', models.CharField(max_length=255)),
                ('html_content', models.TextField(help_text='HTML content with {variable} placeholders')),
                ('text_content', models.TextField(help_text='Plain text content with {variable} placeholders')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('sms', 'SMS'), ('email', 'Email'), ('push', 'Push Notification'), ('in_app', 'In-App Notification')], max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('template_key', models.CharField(max_length=100)),
                ('context_data', models.JSONField(default=dict, help_text='Template variables in JSON format')),
                ('status', models.CharField(choices=[('queued', 'Queued'), ('sending', 'Sending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='queued', max_length=10)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('provider_message_id', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [
                    models.Index(fields=['notification_type', 'status'], name='notif_type_status_idx'),
                    models.Index(fields=['recipient', 'created_at'], name='notif_recipient_created_idx'),
                    models.Index(fields=['phone_number', 'created_at'], name='notif_phone_created_idx'),
                    models.Index(fields=['email', 'created_at'], name='notif_email_created_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='InAppNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('info', 'Information'), ('success', 'Success'), ('warning', 'Warning'), ('error', 'Error')], default='info', max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('action_url', models.CharField(blank=True, help_text='URL to redirect when notification is clicked', max_length=255, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_app_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['recipient', 'is_read', 'created_at'], name='inapp_recipient_read_created_idx'),
                ],
            },
        ),
    ]
