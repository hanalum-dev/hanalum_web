"""comment 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    destroy
)

app_name = 'comment'

urlpatterns = [
    path('destroy/<int:comment_id>', destroy, name="destroy"),
]
