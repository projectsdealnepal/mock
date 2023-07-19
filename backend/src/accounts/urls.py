from django.urls import path, re_path
from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView, LogoutView
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    RegisterView,
    ConfirmEmailView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    LoginView,
    EmailTokenObtainPairView,
    kyc_status_view,
    profile_create_update_view,
    profile_details_view,
)


urlpatterns = [
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        "account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("password-reset/", PasswordResetView.as_view()),
    path(
        "password-reset-confirm/<slug:uidb64>/<slug:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    path("kyc-status/", kyc_status_view, name="kyc_status"),
    path("profile-update/", profile_create_update_view, name="profile_create_update_view"),
    path("profile-details/", profile_details_view, name="profile_details_view"),

]
