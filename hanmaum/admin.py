""" 한마음 어드민 사이트 설정 모듈입니다. """
from django.contrib import admin

from .models import HanmaumArticle
from history.models import LikeActivity, ViewHistory


@admin.register(HanmaumArticle)
class HanmaumAdmin(admin.ModelAdmin):
    """ 한마음 어드민 설정 클래스입니다. """
    actions = [
        'reset_like_and_dislike_counter',
        'reset_viewed_counter',
    ]

    list_display = [
        'id',
        'title',
        'interviewer',
        'interviewee',
        'viewed_count',
        'like_count',
        'dislike_count',
        'created_at',
        'updated_at',
    ]
    list_filter = ["interviewer"]


    def reset_like_and_dislike_counter(modeladmin, request, queryset):
        """좋아요/싫어요 캐시 카운터를 쿼리를 날려 다시 설정한다."""
        articles = queryset

        for article in articles:
            article.like_count = LikeActivity.get_like_count(article)
            article.dislike_count = LikeActivity.get_dislike_count(article)
            article.save()
    reset_like_and_dislike_counter.short_description = '좋아요/싫어요 카운터 재설정'

    def reset_viewed_counter(modeladmin, request, queryset):
        """조회수 캐시 카운터를 쿼리를 날려 다시 설정한다."""
        articles = queryset

        for article in articles:
            article.viewed_count = ViewHistory.total_viewed_count(article)
            article.save()
    reset_viewed_counter.short_description = '조회수 카운터 재설정'
