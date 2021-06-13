"""articles(게시글) 앱 설정 파일입니다."""
from django.apps import AppConfig


class ArticleConfig(AppConfig):
    """acticle 앱의 설정들을 정의합니다."""

    name = "articles"
    verbose_name = "게시글"
