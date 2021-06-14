""" 히스토리 어드민 사이트 설정 모듈입니다. """
from django.contrib import admin

from .models import ViewHistory, LikeActivity

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    """ ViewHistory 어드민 설정 클래스입니다. """
    autocomplete_fields = [
        'viewer'
    ]

    list_display = [
        "viewed_type",
        "viewed_id",
        "viewed_object",
        "viewer",
        "viewed_count",
        "created_at",
        "updated_at"
    ]
    list_filter = [
        "viewed_type",
        "viewed_id",
        "viewer",
        "viewed_count"
    ]


@admin.register(LikeActivity)
class LikeActivityAdmin(admin.ModelAdmin):
    """ LikeActivity 어드민 설정 클래스입니다. """
    autocomplete_fields = [
        'user'
    ]

    list_display = [
        "content_type",
        "content_id",
        "content_object",
        "user",
        "category",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "content_type",
        "content_id",
        "user",
        "category"
    ]