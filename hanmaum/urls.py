"""hanmaum 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    edit, index, new, show, introduce, like, dislike, cancle, new_comment
)

app_name = 'hanmaum'

urlpatterns = [
    path('', index, name="index"),
    path('<int:article_id>', show, name="show"),
    # path('show/<int:article_id>', show, name="show"),
    path('new', new, name="new"),
    path('edit', edit, name="edit"),
    path('introduce', introduce, name="introduce"),
    path('like', like, name="like"),
    path('dislike', dislike, name="dislike"),
    path('cancle', cancle, name="cancle"),
    path('<int:article_id>/comment/new/', new_comment, name="new_comment")
]
