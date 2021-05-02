"""Articles App Admin Site Settings"""
from django.contrib import admin

from history.models import LikeActivity

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """게시글 어드민 설정 클래스입니다."""

    actions = [
        'reset_like_and_dislike_counter'
    ]

    list_display = [
        'id',
        'abstract_title',
        'board',
        'author',
        'anonymous_author',
        'top_fixed',
        'status',
        'created_at',
        'updated_at',
        'like_count',
        'dislike_count',
    ]

    list_display_links = [
        'id',
        'abstract_title'
    ]

    list_filter = [
        'board',
        'top_fixed',
        'anonymous_author',
        'status',
        'author',
    ]

    search_fields = [
        'title'
    ]

    list_per_page = 10

    def reset_like_and_dislike_counter(modeladmin, request, queryset):
        """좋아요/싫어요 캐시 카운터를 쿼리를 날려 다시 설정한다."""
        articles = queryset

        for article in articles:
            article.like_count = LikeActivity.get_like_count(article)
            article.dislike_count = LikeActivity.get_dislike_count(article)
            article.save()
    reset_like_and_dislike_counter.short_description = '좋아요/싫어요 카운터 재설정'
