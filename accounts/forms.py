from django.forms import (
    ModelForm,
    CharField,
    PasswordInput,
    Form,
    EmailField,
    EmailInput,
    IntegerField,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(ModelForm):
    password = CharField(label="password", widget=PasswordInput)
    password_confirm = CharField(label="confirm password", widget=PasswordInput)

    class Meta:
        model = User
        fields = ("phone", "email", "full_name")

    def clean_password_confirm(self):
        password_confirm, password = (
            self.cleaned_data["password_confirm"],
            self.cleaned_data["password"],
        )
        if password != password_confirm and password and password_confirm:
            raise ValidationError("password doesn't match...")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>'
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "full_name",
            "password",
            "last_login",
        )


class UserRegisterForm(Form):
    email = EmailField(label="email")
    full_name = CharField(label="full name")
    phone = CharField(max_length=11)
    password = CharField(label="password", widget=PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        user_email_check = User.objects.filter(email=email).exists()
        if user_email_check:
            raise ValidationError("this email already exists... please try ro login!")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        user_phone_check = User.objects.filter(phone=phone).exists()
        if user_phone_check:
            raise ValidationError("this phone already exists... please try ro login!")
        return phone


class VerifyCodeForm(Form):
    code = IntegerField()


class UserLoginForm(Form):
    email = EmailField(label="Email", required=False)
    password = CharField(label="password", widget=PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email does not exist, try to register...")
        return email
