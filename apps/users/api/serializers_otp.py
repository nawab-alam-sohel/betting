from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models_otp import OTP

User = get_user_model()

class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    otp_type = serializers.ChoiceField(choices=OTP.OTP_TYPE_CHOICES)

    def validate(self, data):
        if not data.get('phone') and not data.get('email'):
            raise serializers.ValidationError("Either phone or email is required")
        return data

class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    otp_type = serializers.ChoiceField(choices=OTP.OTP_TYPE_CHOICES)

    def validate(self, data):
        if not data.get('phone') and not data.get('email'):
            raise serializers.ValidationError("Either phone or email is required")

        # Get latest unverified OTP
        filters = {
            'otp_type': data['otp_type'],
            'is_verified': False,
        }
        if data.get('phone'):
            filters['phone'] = data['phone']
        if data.get('email'):
            filters['email'] = data['email']

        try:
            otp = OTP.objects.filter(**filters).latest('created_at')
            if not otp.is_valid():
                raise serializers.ValidationError("OTP expired or too many attempts")
            data['otp'] = otp
        except OTP.DoesNotExist:
            raise serializers.ValidationError("No valid OTP found")

        return data

class OTPLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, data):
        if not data.get('phone') and not data.get('email'):
            raise serializers.ValidationError("Either phone or email is required")
        
        filters = {
            'otp_type': 'login',
            'is_verified': False,
        }
        if data.get('phone'):
            filters['phone'] = data['phone']
            user_filter = {'phone': data['phone']}
        else:
            filters['email'] = data['email']
            user_filter = {'email': data['email']}

        try:
            otp = OTP.objects.filter(**filters).latest('created_at')
            if not otp.is_valid():
                raise serializers.ValidationError("OTP expired or too many attempts")
            
            # Verify the user exists
            try:
                user = User.objects.get(**user_filter)
                if not user.is_active:
                    raise serializers.ValidationError("Account is disabled")
                data['user'] = user
                data['otp'] = otp
            except User.DoesNotExist:
                raise serializers.ValidationError("User not found")

        except OTP.DoesNotExist:
            raise serializers.ValidationError("No valid OTP found")

        return data