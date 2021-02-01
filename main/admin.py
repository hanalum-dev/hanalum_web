"""루트 사이트 관련 어드민 사이트 설정 모듈입니다."""
from django.contrib import admin

from .models import TopBanner


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
