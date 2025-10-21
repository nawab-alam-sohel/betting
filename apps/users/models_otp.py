from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import string

class OTP(models.Model):
    OTP_TYPE_CHOICES = [
        ('phone', 'Phone Verification'),
        ('email', 'Email Verification'),
        ('login', 'Login Verification'),
        ('password', 'Password Reset'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otps',
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)

    class Meta:
        indexes = [
            models.Index(fields=['phone', 'is_verified']),
            models.Index(fields=['email', 'is_verified']),
            models.Index(fields=['user', 'otp_type']),
        ]

    def __str__(self):
        return f"{self.otp_type} OTP for {self.phone or self.email}"

    @classmethod
    def generate_otp(cls, length=6):
        """Generate a random numeric OTP code"""
        return ''.join(random.choices(string.digits, k=length))

    @classmethod
    def create_otp(cls, otp_type, expiry_minutes=5, **kwargs):
        """
        Create a new OTP instance
        
        Args:
            otp_type: Type of OTP (phone, email, login, password)
            expiry_minutes: Minutes until OTP expires
            **kwargs: user=User instance or phone=phone_number or email=email
        """
        otp = cls(
            otp_type=otp_type,
            code=cls.generate_otp(),
            expires_at=timezone.now() + timezone.timedelta(minutes=expiry_minutes),
            **kwargs
        )
        otp.save()
        return otp

    def verify(self, code):
        """
        Verify the OTP code
        
        Returns:
            bool: True if verified successfully, False otherwise
        """
        if self.is_verified:
            return False
        
        if self.attempts >= self.max_attempts:
            return False
            
        if timezone.now() > self.expires_at:
            return False

        self.attempts += 1
        if code == self.code:
            self.is_verified = True
            self.save()
            return True
            
        self.save()
        return False

    def is_valid(self):
        """Check if OTP is still valid (not expired, not verified, attempts remaining)"""
        return (
            not self.is_verified and
            self.attempts < self.max_attempts and
            timezone.now() <= self.expires_at
        )