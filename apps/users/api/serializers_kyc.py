from rest_framework import serializers
from django.utils import timezone
from apps.users.models_kyc import (
    KYCDocument,
    KYCProfile,
    UserDevice,
    LoginAttempt
)

class KYCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDocument
        fields = [
            'id',
            'document_type',
            'document_number',
            'front_image',
            'back_image',
            'selfie_image',
            'status',
            'rejection_reason',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'status',
            'rejection_reason',
            'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        # Check if user already has verified documents of this type
        user = self.context['request'].user
        existing = KYCDocument.objects.filter(
            user=user,
            document_type=attrs['document_type'],
            status='approved'
        ).exists()
        
        if existing:
            raise serializers.ValidationError(
                f"You already have a verified {attrs['document_type']} document"
            )
        
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class KYCProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCProfile
        fields = [
            'id',
            'date_of_birth',
            'gender',
            'nationality',
            'country_of_residence',
            'city',
            'address_line1',
            'address_line2',
            'postal_code',
            'verification_level',
            'occupation',
            'source_of_funds',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'verification_level',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = [
            'id',
            'device_type',
            'device_name',
            'os_type',
            'os_version',
            'browser',
            'ip_address',
            'location',
            'is_trusted',
            'last_used',
            'created_at'
        ]
        read_only_fields = [
            'device_id',
            'ip_address',
            'location',
            'last_used',
            'created_at'
        ]

    def create(self, validated_data):
        request = self.context['request']
        # Get IP address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        validated_data.update({
            'user': request.user,
            'ip_address': ip_address,
            # TODO: Implement proper device fingerprinting
            'device_id': request.META.get('HTTP_USER_AGENT', '')[:64]
        })
        
        return super().create(validated_data)


class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = [
            'id',
            'ip_address',
            'device_id',
            'user_agent',
            'location',
            'status',
            'failure_reason',
            'attempted_at'
        ]
        read_only_fields = fields


class AdminKYCDocumentSerializer(KYCDocumentSerializer):
    """Extended serializer for admin use"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta(KYCDocumentSerializer.Meta):
        fields = KYCDocumentSerializer.Meta.fields + [
            'user_email',
            'verified_by',
            'verified_at'
        ]
        read_only_fields = [
            'created_at',
            'updated_at',
            'user_email'
        ]

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            if validated_data['status'] == 'approved':
                validated_data.update({
                    'verified_by': self.context['request'].user,
                    'verified_at': timezone.now()
                })
                # Update user's KYC profile verification level
                kyc_profile = instance.user.kyc_profile
                if kyc_profile.verification_level < 2:
                    kyc_profile.verification_level = 2
                    kyc_profile.save()
            elif validated_data['status'] == 'rejected':
                if 'rejection_reason' not in validated_data:
                    raise serializers.ValidationError(
                        "Rejection reason is required when rejecting a document"
                    )
        return super().update(instance, validated_data)