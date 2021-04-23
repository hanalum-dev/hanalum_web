"""comment 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    update, destroy
)

app_name = 'comments'

urlpatterns = [
    path('update/<int:comment_id>', update, name="update"),
    path('destroy/<int:comment_id>', destroy, name="destroy"),
]
