"""user(사용자 계정) forms 모듈입니다."""
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User
from .tokens import account_activation_token


class UserCreationForm(forms.ModelForm):
    """user 생성 폼 클래스"""

    class Meta:
        """user creation form meta 클래스"""

        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "nickname",
            "realname",
            "gender",
            "user_category",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "example@hanalum.kr"}
            ),
            "nickname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "입력하세요"}
            ),
            "realname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "입력하세요"}
            ),
            "gender": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "user_category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "email": "이메일",
            "nickname": "닉네임",
            "realname": "실명",
            "gender": "성별",
            "user_category": "분류",
        }

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "영문 + 숫자로 8자 이상"}
        ),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "영문 + 숫자로 8자 이상"}
        ),
    )

    # TODO: save ovrriden issue 해결해서 save로 변경하기
    def f_save(self, current_site, mail_to, commit=True):
        """비밀번호를 해시 상태로 저장"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
            message = render_to_string(
                "activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            mail_title = "한아름 계정 활성화 확인 이메일"
            send_mail(
                subject=mail_title,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail_to],
                fail_silently=False,
                html_message=message,
            )
        return user


class CustomUserChangeForm(UserChangeForm):
    """유저 정보 변경 폼 클래스"""

    class Meta:
        """user change form meta class"""

        model = User
        fields = ["avatar", "nickname", "password1", "password2"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "custom-file-input"}),
            "nickname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "입력하세요"}
            ),
        }
        labels = {
            "avatar": "프로필",
            "nickname": "닉네임",
        }

    password = None
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "영문 + 숫자로 8자 이상"}
        ),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "영문 + 숫자로 8자 이상"}
        ),
    )

    def f_save(self, commit=True):
        """비밀번호를 해시 상태로 저장"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# TODO: 비밀번호 변경 폼 클래스
# from django.contrib.auth.forms import PasswordChangeForm
# class CustomPasswordChageform(PasswordChangeForm):
#     """유저 비밀번호 변경 폼 클래스"""
