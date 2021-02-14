"""hanmaum 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    show, new, new_comment,
)

app_name = 'article'

urlpatterns = [
    # path('', index, name="index"),
    path('<int:article_id>', show, name="show"),
    path('new/<int:board_id>', new, name="new"),
    path('<int:article_id>/comment/new/', new_comment, name="new_comment")
]
