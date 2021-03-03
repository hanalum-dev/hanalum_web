""" notice(공지사항) 어드민 설정 파일입니다."""
from django.contrib import admin

from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """ 공지사항 어드민 설정 클래스입니다. """

    list_display = [
        'title',
        'summary',
        'top_fixed',
        'status',
        'priority',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'priority',
        'top_fixed',
        'status',
        'title',
    ]