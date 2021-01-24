"""user(사용자 계정) forms 모듈입니다."""
import re

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User
from .tokens import account_activation_token


class CheckUserClass:
    """유저 생성 Validation 클래스"""

    def __init__(self):
        """생성자"""
        self.cleaned_data = None

    def check_password(self):
        """비밀번호 Validation"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        password_regex = re.compile(
            r"^\s*(?:\S\s*){8,16}$"
        )  # 8~16개의 비 공백 문자가 포함된 문자열과 일치된다.
        is_match = password_regex.match(password1)
        if is_match is None:  # 비밀번호가 정규식에 매치되지 않음
            return "비밀번호는 8자리 이상 16자리 이하로 만들어야합니다."

        if password1 and password2 and password1 != password2:
            return "비밀번호가 일치하지 않습니다."
        return ""

    def check_nickname(self, _nickname, user_nickname=None):
        """닉네임 Validation"""
        # _nickname : 생성할(변경할) 닉네임  # user_nickname : 기존 닉네임
        if user_nickname is not None:  # CustomUserChangeForm에서 사용
            if user_nickname == _nickname:  # 현재 닉네임이랑 같은경우
                return "현재 닉네임과 동일합니다."  # 그대로 사용

        if User.objects.filter(nickname=_nickname).count() > 0:  # 닉네임 중복인 경우
            return "이미 사용중인 닉네임 입니다."

        nickname_regex = re.compile(
            r"^[a-zA-Z0-9가-힣]{1,10}$"
        )  # 영문 & 숫자로 이루어진 길이 1~8 닉네임만 허용
        is_match = nickname_regex.match(nickname_regex)

        if is_match is None:  # 비밀번호가 정규식에 매치되지 않음
            return "닉네임은 한글 & 영문 & 숫자 조합으로 이루어져야합니다."

        return ""

    def check_realname(self, _realname):  # 실명확인
        """이름 Validation"""
        realname_regex = re.compile("^[가-힣]+$")
        is_match = realname_regex.match(_realname)
        if is_match is None:
            return "한글 실명을 입력하세요."
        return ""

    def check_email(self, _email):
        """이메일 Validation"""
        email_regex = re.compile(
            r"/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i"
        )
        is_match = email_regex.match(_email)
        if is_match is None:
            return "형식에 맞는 이메일을 입력해주세요."

        if User.objects.filter(email=_email).count() > 0:
            return "이미 등록된 이메일입니다."
        else:
            return ""


class UserCreationForm(forms.ModelForm, CheckUserClass):
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

    def form_save(self, current_site, mail_to, commit=True):
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


class CustomUserChangeForm(UserChangeForm, CheckUserClass):
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

    def form_save(self, commit=True):
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
