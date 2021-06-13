"""user(사용자 계정) 앱 설정 파일입니다."""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """user 앱의 설정들을 정의합니다."""

    name = "users"
    verbose_name = "유저"
