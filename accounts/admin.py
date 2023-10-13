from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode


# Register your models here.
@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "phone", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "phone", "full_name", "password"),
            },
        ),
        ("permissions", {"fields": ("is_active", "is_admin", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {"fields": ("phone", "email", "full_name", "password", "password_confirm")},
        ),
    )

    search_fields = ("email", "full_name")
    ordering = ("email", "full_name")
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
