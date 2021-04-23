"""hanmaum 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    show
)

app_name = 'boards'

urlpatterns = [
    # path('', index, name="index"),
    path('<int:board_id>', show, name="show"),
]
