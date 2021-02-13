"""notice 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
   index, show
)

app_name = 'notice'

urlpatterns = [
    path('', index, name="index"),
    path('<int:notice_id>', show, name="show"),
]
