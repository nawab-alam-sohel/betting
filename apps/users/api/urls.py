from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    ProfileUpdateView,
    LogoutView,
    PasswordChangeView,
    ResetPasswordView,
)
from .views_otp import RequestOTPView, VerifyOTPView, OTPLoginView
from .views_kyc import (
    KYCDocumentViewSet,
    KYCProfileViewSet,
    UserDeviceViewSet,
    LoginAttemptViewSet,
)

# API Router
router = DefaultRouter()
router.register(r'kyc/documents', KYCDocumentViewSet, basename='kyc-document')
router.register(r'kyc/profile', KYCProfileViewSet, basename='kyc-profile')
router.register(r'devices', UserDeviceViewSet, basename='user-device')
router.register(r'login-attempts', LoginAttemptViewSet, basename='login-attempt')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
    path("password/reset/", ResetPasswordView.as_view(), name="password_reset"),

  # JWT token obtain endpoint (convenience alias)
  path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # OTP endpoints
    path("otp/request/", RequestOTPView.as_view(), name="request-otp"),
    path("otp/verify/", VerifyOTPView.as_view(), name="verify-otp"),
    path("otp/login/", OTPLoginView.as_view(), name="otp-login"),
] + router.urls
