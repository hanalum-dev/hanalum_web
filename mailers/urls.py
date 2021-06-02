"""mailers previewer 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    preview_user_activation
)

app_name = 'mailers'

urlpatterns = [
    path('preview_user_activation', preview_user_activation, name="preview_user_activation"),
]
