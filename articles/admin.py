"""Articles App Admin Site Settings"""
from django.contrib import admin

from history.models import LikeActivity, ViewHistory

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """게시글 어드민 설정 클래스입니다."""

    actions = [
        'reset_like_and_dislike_counter',
        'reset_viewed_counter',
        'copy_to_draft_article',
        'copy_to_published_article',
        'set_to_top_fixed_article',
        'set_to_top_unfixed_article'
    ]

    autocomplete_fields = [
        'author'
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
        'viewed_count',
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

    def copy_to_draft_article(modeladmin, request, queryset):
        """draft 상태로 게시글 복사"""
        articles = queryset

        for article in articles:
            article.copy()
    copy_to_draft_article.short_description = 'draft 상태로 게시글 복사'

    def copy_to_published_article(modeladmin, request, queryset):
        """published 상태로 게시글 복사"""
        articles = queryset

        for article in articles:
            article.copy(status='p')
    copy_to_published_article.short_description = 'published 상태로 게시글 복사'

    def set_to_top_fixed_article(modeladmin, request, queryset):
        """상단 고정 게시글 설정"""
        articles = queryset

        for article in articles:
            article.top_fixed = True
            article.save()
    set_to_top_fixed_article.short_description = '상단 고정 게시글 설정'

    def set_to_top_unfixed_article(modeladmin, request, queryset):
        """상단 고정 게시글 해제"""
        articles = queryset

        for article in articles:
            article.top_fixed = False
            article.save()
    set_to_top_unfixed_article.short_description = '상단 고정 게시글 해제'

    def reset_viewed_counter(modeladmin, request, queryset):
        """조회수 캐시 카운터를 쿼리를 날려 다시 설정한다."""
        articles = queryset

        for article in articles:
            article.viewed_count = ViewHistory.total_viewed_count(article)
            article.save()
    reset_viewed_counter.short_description = '조회수 카운터 재설정'
