""" notice(공지사항) 어드민 설정 파일입니다."""
from django.contrib import admin

from history.models import ViewHistory

from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """ 공지사항 어드민 설정 클래스입니다. """

    actions = [
        'reset_viewed_counter',
        'copy_to_draft_notice',
        'copy_to_published_notice',
        'set_to_top_fixed_notice',
        'set_to_top_unfixed_notice'
    ]

    list_display = [
        'title',
        'summary',
        'top_fixed',
        'status',
        'priority',
        'viewed_count',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'priority',
        'top_fixed',
        'status',
        'title',
    ]

    def copy_to_draft_notice(modeladmin, request, queryset):
        """draft 상태로 게시글 복사"""
        notices = queryset

        for notice in notices:
            notice.copy()
    copy_to_draft_notice.short_description = 'draft 상태로 게시글 복사'

    def copy_to_published_notice(modeladmin, request, queryset):
        """published 상태로 게시글 복사"""
        notices = queryset

        for notice in notices:
            notice.copy(status='p')
    copy_to_published_notice.short_description = 'published 상태로 게시글 복사'

    def set_to_top_fixed_notice(modeladmin, request, queryset):
        """상단 고정 게시글 설정"""
        notices = queryset

        for notice in notices:
            notice.top_fixed = True
            notice.save()
    set_to_top_fixed_notice.short_description = '상단 고정 게시글 설정'

    def set_to_top_unfixed_notice(modeladmin, request, queryset):
        """상단 고정 게시글 해제"""
        notices = queryset

        for notice in notices:
            notice.top_fixed = False
            notice.save()
    set_to_top_unfixed_notice.short_description = '상단 고정 게시글 해제'

    def reset_viewed_counter(modeladmin, request, queryset):
        """조회수 캐시 카운터를 쿼리를 날려 다시 설정한다."""
        notices = queryset

        for notice in notices:
            notice.viewed_count = ViewHistory.total_viewed_count(notice)
            notice.save()
    reset_viewed_counter.short_description = '조회수 카운터 재설정'
