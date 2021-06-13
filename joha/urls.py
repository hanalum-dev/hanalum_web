"""joha 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    index
)

app_name = 'joha'

urlpatterns = [
    path('', index, name="index"),
]
