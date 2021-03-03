""" hashtag 어드민 사이트 설정 파일입니다. """
from django.contrib import admin

from .models import HashTag

@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    """게시글 어드민 설정 클래스입니다."""
    list_display = [
        "tagged_type",
        "tagged_id",
        "tagged_object",
        "content",
        "created_at",
        "updated_at"
    ]
    list_filter = [
        "tagged_type",
        "tagged_id",
        "content",
    ]
