"""joha 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (
    index,
    apply,
    JohaReviewsView,
)

app_name = 'joha'

urlpatterns = [
    path('', index, name="index"),
    path('reviews/<int:review_id>', JohaReviewsView.show, name="reviews_show"),
    path('reviews/apply', apply, name="reviews_apply"),
    path('reviews', JohaReviewsView.index, name="reviews_index"),
    path('reviews/new', JohaReviewsView.new, name="reviews_new"),
    path('reviews/edit/<int:review_id>', JohaReviewsView.edit, name="reviews_edit"),
]
