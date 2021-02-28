"""루트 사이트 관련 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin

from .models import MainBoard, TopBanner


@admin.register(TopBanner)
class TopBannerAdmin(admin.ModelAdmin):
    """ 루트 사이트 어드민 설정 클래스입니다. """
    list_display = [
        "content",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active"]


@admin.register(MainBoard)
class MainBoardAdmin(admin.ModelAdmin):
    """ 메인보드 어드민 설정 클래스입니다. """
    list_display = [
        'board',
        'priority',
    ]
    list_filter = [
        'priority',
    ]
