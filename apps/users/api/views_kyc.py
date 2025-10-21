from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from apps.users.models_kyc import (
    KYCDocument,
    KYCProfile,
    UserDevice,
    LoginAttempt
)
from .serializers_kyc import (
    KYCDocumentSerializer,
    KYCProfileSerializer,
    UserDeviceSerializer,
    LoginAttemptSerializer,
    AdminKYCDocumentSerializer
)


class KYCDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_role('admin'):
            # Admins can see all documents
            return KYCDocument.objects.all().select_related('user')
        # Users can only see their own documents
        return KYCDocument.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.has_role('admin'):
            return AdminKYCDocumentSerializer
        return KYCDocumentSerializer


class KYCProfileViewSet(viewsets.ModelViewSet):
    serializer_class = KYCProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_role('admin'):
            return KYCProfile.objects.all().select_related('user')
        return KYCProfile.objects.filter(user=self.request.user)

    def get_object(self):
        # For non-admins, always return their own profile
        if not self.request.user.has_role('admin'):
            return get_object_or_404(KYCProfile, user=self.request.user)
        return super().get_object()


class UserDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_role('admin'):
            return UserDevice.objects.all().select_related('user')
        return UserDevice.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def trust(self, request, pk=None):
        device = self.get_object()
        device.is_trusted = True
        device.save()
        return Response({'status': 'Device marked as trusted'})

    @action(detail=True, methods=['post'])
    def untrust(self, request, pk=None):
        device = self.get_object()
        device.is_trusted = False
        device.save()
        return Response({'status': 'Device marked as untrusted'})


class LoginAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return LoginAttempt.objects.all().select_related('user')
        return LoginAttempt.objects.filter(
            Q(user=user) | 
            Q(ip_address=self.get_client_ip())
        )

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')