from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    path("verify/", views.UserVerifyCodeView.as_view(), name="user-verify-code"),
]
