""" 한마음 어드민 사이트 설정 모듈입니다. """
from django.contrib import admin

from .models import HanmaumArticle


@admin.register(HanmaumArticle)
class HanmaumAdmin(admin.ModelAdmin):
    """ 한마음 어드민 설정 클래스입니다. """
    list_display = [
        "title",
        "interviewer",
        "interviewee",
        "created_at",
        "updated_at",
    ]
    list_filter = ["interviewer"]
