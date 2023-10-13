from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth import login, logout
from .utils import generate_otp_code, send_otp_code
from .forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from .models import OtpCode, User

# Create your views here.


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone, email, full_name, password = (
                form.cleaned_data["phone"],
                form.cleaned_data["email"],
                form.cleaned_data["full_name"],
                form.cleaned_data["password"],
            )
            code = generate_otp_code()
            print(code)
            send_otp_code(phone=phone, otp_code=code)
            OtpCode.objects.create(phone=phone, code=code)
            request.session["user_registration_info"] = {
                "phone": phone,
                "email": email,
                "full_name": full_name,
                "password": password,
            }
            messages.success(request, "we sent you a code.", "success")
            return redirect("accounts:user-verify-code")
        return render(request, self.template_name, {"form": form})


class UserVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class()
        return render(
            request=request, template_name=self.template_name, context={"form": form}
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        user_session = request.session["user_registration_info"]
        form = self.form_class(request.POST)
        phone, email, full_name, password = (
            user_session["phone"],
            user_session["email"],
            user_session["full_name"],
            user_session["password"],
        )
        user_code = OtpCode.objects.get(phone=user_session["phone"])
        if form.is_valid():
            if user_code.expire_time < datetime.now().timestamp():
                user_code.delete()
                messages.error(request, "code is expired, please try again", "danger")
                return redirect("accounts:user-register")
            code = form.cleaned_data["code"]
            if code == user_code.code and code and user_code.code:
                user = User.objects.create_user(
                    phone=phone, email=email, full_name=full_name, password=password
                )
                user_code.delete()
                login(request, user)
                messages.success(request, "user registered successfully", "success")
                return redirect("home:home")
            else:
                messages.error(request, "this code is wrong", "danger")
                return redirect("accounts:user-verify-code")
        return redirect("home:home")


class LoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email, password = form.cleaned_data["email"], form.cleaned_data["password"]
            user = User.objects.get(email=email)
            print(user.email)
            if not user.check_password(password):
                messages.error(request, "password is wrong, try again", "danger")
                return redirect("accounts:user-login")
            login(request, user)
            messages.success(request, "you logged in successfully", "success")
            return redirect("home:home")

        return redirect("home:home")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "user logged out successfully", "success")
        return redirect("home:home")
