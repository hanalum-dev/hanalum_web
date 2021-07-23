"""user(사용자 계정) 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationOnAdminSiteForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    "user(사용자 계정) 어드민 설정 클래스입니다."
    form = UserChangeForm
    add_form = UserCreationOnAdminSiteForm
    change_password_form = AdminPasswordChangeForm

    list_display = [
        'id',
        'email',
        'nickname',
        'realname',
        'gender',
        'avatar',
        'is_admin',
        'is_active',
        'is_superuser',
        'read_authority',
        'write_authority',
        'user_category',
        'created_at',
        'updated_at',
        'last_login',
        'roles',
    ]
    list_filter = ['is_admin', 'read_authority', 'write_authority', 'user_category']
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                )
            },
        ),
        (
            'Personal info',
            {'fields': ('nickname', 'realname', 'gender', 'avatar', 'user_category')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_admin',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'read_authority',
                    'write_authority',
                    'roles'
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes' : ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'nickname',
                    'realname',
                    'gender',
                    'avatar',
                    'is_admin',
                    'is_staff',
                    'read_authority',
                    'write_authority',
                    'roles',
                )
            }
        ),
    )
    search_fields = ('email', 'realname', 'nickname')
    ordering = ('-id',)
    filter_horizontal = ()
