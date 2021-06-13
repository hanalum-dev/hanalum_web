"""board(게시판) 앱 설정 파일입니다."""
from django.apps import AppConfig


class BoardConfig(AppConfig):
    """board 앱의 설정들을 정의합니다."""

    name = "boards"
    verbose_name = "게시판"