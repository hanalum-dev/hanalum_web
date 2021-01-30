"""user(사용자 계정) 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    "user(사용자 계정) 어드민 설정 클래스입니다."
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "nickname",
        "realname",
        "gender",
        "avatar",
        "is_admin",
        "is_staff",
        "is_active",
        "is_superuser",
        "read_authority",
        "write_authority",
        "user_category",
    ]
    list_filter = ["is_admin", "read_authority", "write_authority", "user_category"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("nickname", "realname", "gender", "avatar", "user_category")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "read_authority",
                    "write_authority",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    search_fields = ("email", "realname", "nickname")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
