"""notice 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
   index, show, new_comment
)

app_name = 'notice'

urlpatterns = [
    path('', index, name="index"),
    path('<int:notice_id>', show, name="show"),
    path('<int:notice_id>/comment/new/', new_comment, name="new_comment")
]
