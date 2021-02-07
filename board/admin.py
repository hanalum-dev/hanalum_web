""" 게시판 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """게시판 어드민 설정 클래스입니다."""

    list_display = [
        'title',
        'auth_read',
        'auth_write',
        'use_comment',
        'use_good',
        'use_bad',
        'use_anonymous',
        'status',
        'max_attachment_count'
    ]
    list_filter = [
        'auth_read', 'auth_write', 'use_comment', 'use_good', 'use_bad', 'use_anonymous', 'status', 'max_attachment_count',
    ]
