""" 댓글( 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment 어드민 설정 클래스입니다. """
    list_display = [
        'id',
        'user',
        'content',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'user',
    ]
