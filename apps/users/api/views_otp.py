from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .serializers_otp import RequestOTPSerializer, VerifyOTPSerializer, OTPLoginSerializer
from apps.users.models_otp import OTP

class RequestOTPView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        otp = OTP.create_otp(**data)

        # TODO: Integrate with SMS/email service to send OTP
        if settings.DEBUG:
            return Response({
                'message': 'OTP sent successfully',
                'debug_code': otp.code  # Only in development!
            })
        return Response({
            'message': 'OTP sent successfully'
        })

class VerifyOTPView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data['otp']
        code = serializer.validated_data['code']
        
        if otp.verify(code):
            return Response({
                'message': 'OTP verified successfully'
            })
        
        return Response({
            'message': 'Invalid OTP'
        }, status=status.HTTP_400_BAD_REQUEST)

class OTPLoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data['otp']
        user = serializer.validated_data['user']
        code = serializer.validated_data['code']
        
        if otp.verify(code):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone': user.phone,
                    'full_name': user.full_name,
                }
            })
        
        return Response({
            'message': 'Invalid OTP'
        }, status=status.HTTP_400_BAD_REQUEST)