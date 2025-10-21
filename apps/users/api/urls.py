from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from .views import (
  RegisterView,
  LoginView,
  UserProfileView,
  ProfileUpdateView,
  LogoutView,
  PasswordChangeView,
  ResetPasswordView,
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),  # ✅ New
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
    path("password/reset/", ResetPasswordView.as_view(), name="password_reset"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
