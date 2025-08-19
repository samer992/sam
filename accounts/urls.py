from django.urls import path
from .views import SignupUserView, LoginUserView, VerifyUserEmail, TestAuthView, PasswordResetConfrim, \
    PasswordResetRequestView, SetNewPassword, LogoutUserView, SignUp, logout, signin, prof

urlpatterns = [
    path("signup/", SignupUserView.as_view(), name="signup"),
    path("verify-email/", VerifyUserEmail.as_view(), name="verify-email"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("profile/", TestAuthView.as_view(), name="profile"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfrim.as_view(), name="password-reset-confirm"),
    path("set-new-password/", SetNewPassword.as_view(), name="set-new-password"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("logoutp/", logout, name="logoutp"),
    path("ragstar/", SignUp, name="ragstar"),
    path("signin/", signin, name="signin"),
    path("prof/", prof, name="prof"),



]
