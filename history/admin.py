""" 히스토리 어드민 사이트 설정 모듈입니다. """
from django.contrib import admin

from .models import ViewHistory, LikeActivity

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    """ ViewHistory 어드민 설정 클래스입니다. """
    list_display = [
        "viewed_model",
        "viewed_id",
        "viewer",
        "viewed_count",
        "created_at",
        "updated_at"
    ]
    list_filter = ["viewed_model", "viewed_id", "viewer", "viewed_count"]


@admin.register(LikeActivity)
class LikeActivityAdmin(admin.ModelAdmin):
    """ LikeActivity 어드민 설정 클래스입니다. """
    list_display = [
        "activity_model",
        "activity_id",
        "user",
        "category",
        "created_at",
        "updated_at",
    ]
    list_filter = ["activity_model", "activity_id", "user", "category"]