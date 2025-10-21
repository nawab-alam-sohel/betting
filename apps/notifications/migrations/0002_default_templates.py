from django.db import migrations

def create_default_templates(apps, schema_editor):
    SMSTemplate = apps.get_model('notifications', 'SMSTemplate')
    EmailTemplate = apps.get_model('notifications', 'EmailTemplate')

    # SMS Templates
    sms_templates = [
        {
            'name': 'Login OTP',
            'template_key': 'login_otp',
            'content': 'Your {site_name} login code is {otp}. Valid for {expiry_minutes} minutes. Do not share this code with anyone.'
        },
        {
            'name': 'Registration OTP',
            'template_key': 'registration_otp',
            'content': 'Welcome to {site_name}! Your verification code is {otp}. Valid for {expiry_minutes} minutes.'
        },
        {
            'name': 'Password Reset OTP',
            'template_key': 'password_reset_otp',
            'content': 'Your {site_name} password reset code is {otp}. Valid for {expiry_minutes} minutes.'
        },
        {
            'name': 'Withdrawal Confirmation',
            'template_key': 'withdrawal_confirmation',
            'content': 'Confirm withdrawal of {amount} {currency} from your {site_name} account. Code: {otp}'
        },
        {
            'name': 'Bet Placement',
            'template_key': 'bet_placed',
            'content': 'Bet placed successfully on {event}. Stake: {amount} {currency}. Potential win: {potential_win} {currency}'
        },
    ]

    for template in sms_templates:
        SMSTemplate.objects.get_or_create(
            template_key=template['template_key'],
            defaults={
                'name': template['name'],
                'content': template['content'],
            }
        )

    # Email Templates
    email_templates = [
        {
            'name': 'Welcome Email',
            'template_key': 'welcome',
            'subject': 'Welcome to {site_name}!',
            'html_content': '''
                <h1>Welcome to {site_name}!</h1>
                <p>Dear {name},</p>
                <p>Thank you for joining {site_name}. We're excited to have you on board!</p>
                <p>To get started:</p>
                <ul>
                    <li>Complete your profile</li>
                    <li>Verify your identity</li>
                    <li>Make your first deposit</li>
                </ul>
                <p>If you need any assistance, our support team is available 24/7.</p>
            ''',
            'text_content': '''
                Welcome to {site_name}!

                Dear {name},

                Thank you for joining {site_name}. We're excited to have you on board!

                To get started:
                - Complete your profile
                - Verify your identity
                - Make your first deposit

                If you need any assistance, our support team is available 24/7.
            '''
        },
        {
            'name': 'Email Verification',
            'template_key': 'email_verification',
            'subject': 'Verify your {site_name} email',
            'html_content': '''
                <h2>Email Verification</h2>
                <p>Please use this code to verify your email address: <strong>{otp}</strong></p>
                <p>This code will expire in {expiry_minutes} minutes.</p>
            ''',
            'text_content': '''
                Email Verification

                Please use this code to verify your email address: {otp}
                This code will expire in {expiry_minutes} minutes.
            '''
        },
        {
            'name': 'Password Reset',
            'template_key': 'password_reset',
            'subject': 'Reset your {site_name} password',
            'html_content': '''
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password.</p>
                <p>Your password reset code is: <strong>{otp}</strong></p>
                <p>This code will expire in {expiry_minutes} minutes.</p>
                <p>If you didn't request this, please ignore this email.</p>
            ''',
            'text_content': '''
                Password Reset Request

                We received a request to reset your password.
                Your password reset code is: {otp}
                This code will expire in {expiry_minutes} minutes.

                If you didn't request this, please ignore this email.
            '''
        },
        {
            'name': 'Withdrawal Confirmation',
            'template_key': 'withdrawal_confirmation',
            'subject': 'Confirm your withdrawal - {site_name}',
            'html_content': '''
                <h2>Withdrawal Confirmation</h2>
                <p>Please confirm your withdrawal request:</p>
                <ul>
                    <li>Amount: {amount} {currency}</li>
                    <li>Method: {method}</li>
                    <li>Account: {account}</li>
                </ul>
                <p>Use this code to confirm: <strong>{otp}</strong></p>
                <p>This code will expire in {expiry_minutes} minutes.</p>
            ''',
            'text_content': '''
                Withdrawal Confirmation

                Please confirm your withdrawal request:
                Amount: {amount} {currency}
                Method: {method}
                Account: {account}

                Use this code to confirm: {otp}
                This code will expire in {expiry_minutes} minutes.
            '''
        },
        {
            'name': 'New Device Login',
            'template_key': 'new_device_login',
            'subject': 'New device login detected - {site_name}',
            'html_content': '''
                <h2>Security Alert</h2>
                <p>We detected a login from a new device:</p>
                <ul>
                    <li>Device: {device_name}</li>
                    <li>Location: {location}</li>
                    <li>IP Address: {ip_address}</li>
                    <li>Time: {time}</li>
                </ul>
                <p>If this wasn't you, please change your password immediately and contact support.</p>
            ''',
            'text_content': '''
                Security Alert

                We detected a login from a new device:
                Device: {device_name}
                Location: {location}
                IP Address: {ip_address}
                Time: {time}

                If this wasn't you, please change your password immediately and contact support.
            '''
        },
    ]

    for template in email_templates:
        EmailTemplate.objects.get_or_create(
            template_key=template['template_key'],
            defaults={
                'name': template['name'],
                'subject': template['subject'],
                'html_content': template['html_content'].strip(),
                'text_content': template['text_content'].strip(),
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_templates, migrations.RunPython.noop),
    ]