from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class KYCDocument(models.Model):
    """Document types that users can submit for KYC verification"""
    DOCUMENT_TYPES = [
        ('national_id', 'National ID Card'),
        ('passport', 'Passport'),
        ('drivers_license', "Driver's License"),
        ('utility_bill', 'Utility Bill'),
        ('bank_statement', 'Bank Statement'),
    ]

    VERIFICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='kyc_documents'
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES
    )
    document_number = models.CharField(
        max_length=50,
        help_text='Document ID or reference number'
    )
    front_image = models.ImageField(
        upload_to='kyc_documents/%Y/%m/',
        help_text='Front side of the document'
    )
    back_image = models.ImageField(
        upload_to='kyc_documents/%Y/%m/',
        help_text='Back side of the document',
        null=True,
        blank=True
    )
    selfie_image = models.ImageField(
        upload_to='kyc_documents/%Y/%m/',
        help_text='Selfie with document',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    rejection_reason = models.TextField(
        null=True,
        blank=True,
        help_text='Reason for rejection if status is rejected'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['document_type', 'status']),
        ]

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"


class KYCProfile(models.Model):
    """Extended KYC information for users"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    VERIFICATION_LEVEL = [
        (0, 'Unverified'),
        (1, 'Basic Verification'),  # Email + Phone verified
        (2, 'Identity Verified'),   # Basic + ID document verified
        (3, 'Enhanced Verification'),# Identity + Address + Additional checks
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='kyc_profile'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Required for age verification'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    nationality = models.CharField(max_length=100, null=True, blank=True)
    country_of_residence = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    verification_level = models.IntegerField(
        choices=VERIFICATION_LEVEL,
        default=0
    )
    is_politically_exposed = models.BooleanField(
        default=False,
        help_text='Whether the user is a politically exposed person'
    )
    occupation = models.CharField(max_length=100, null=True, blank=True)
    source_of_funds = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'KYC Profile'
        verbose_name_plural = 'KYC Profiles'

    def __str__(self):
        return f"KYC Profile - {self.user.email}"


class UserDevice(models.Model):
    """Track user devices for security"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    device_id = models.CharField(
        max_length=64,
        help_text='Unique device identifier'
    )
    device_type = models.CharField(
        max_length=20,
        help_text='Type of device (mobile, desktop, tablet)'
    )
    device_name = models.CharField(
        max_length=100,
        help_text='User-friendly device name'
    )
    os_type = models.CharField(
        max_length=20,
        help_text='Operating system'
    )
    os_version = models.CharField(
        max_length=20,
        help_text='OS version'
    )
    browser = models.CharField(
        max_length=50,
        help_text='Browser name and version'
    )
    ip_address = models.GenericIPAddressField()
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Geographic location based on IP'
    )
    is_trusted = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'device_id']
        indexes = [
            models.Index(fields=['user', 'is_trusted']),
            models.Index(fields=['device_id']),
        ]

    def __str__(self):
        return f"{self.device_name} - {self.user.email}"


class LoginAttempt(models.Model):
    """Track login attempts for security"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_attempts',
        null=True
    )
    ip_address = models.GenericIPAddressField()
    device_id = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    user_agent = models.TextField()
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('blocked', 'Blocked'),
        ]
    )
    failure_reason = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['ip_address', 'attempted_at']),
            models.Index(fields=['user', 'attempted_at']),
            models.Index(fields=['device_id', 'attempted_at']),
        ]

    def __str__(self):
        return f"Login attempt from {self.ip_address} at {self.attempted_at}"