""" 게시판 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin

from .models import Board, BoardAdminUser


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """게시판 어드민 설정 클래스입니다."""

    autocomplete_fields = [
        'creator'
    ]

    list_display = [
        'title',
        'creator',
        'creator_category',
        'auth_read',
        'auth_write',
        'use_comment',
        'use_good',
        'use_bad',
        'use_anonymous',
        'status',
        'priority',
        'board_format_category',
        'max_attachment_count'
    ]
    list_filter = [
        'auth_read',
        'creator',
        'creator_category',
        'auth_write',
        'use_comment',
        'use_good',
        'use_bad',
        'use_anonymous',
        'status',
        'board_format_category',
        'max_attachment_count',
    ]


@admin.register(BoardAdminUser)
class BoardAdminUserAdmin(admin.ModelAdmin):
    """게시판 관리자 유저 어드민 설정 클래스입니다."""
    list_display = [
        'user',
        'board',
        'register_notice_permission',
        'delete_article_permission',
    ]
    list_filter = [
        'user',
        'board',
        'register_notice_permission',
        'delete_article_permission',
    ]
