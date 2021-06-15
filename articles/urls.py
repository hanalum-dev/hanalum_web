"""articles urls 정의 파일입니다."""
from django.urls import path

from .views import delete, dislike, edit, like, new, new_comment, search, show, restrict_comment, allow_comment

app_name = 'articles'

urlpatterns = [
    # path('', index, name="index"),
    path('<int:article_id>', show, name="show"),
    path('new/<int:board_id>', new, name="new"),
    path('edit/<int:article_id>', edit, name="edit"),
    path('delete/<int:article_id>', delete, name="delete"),
    path('<int:article_id>/comment/new/', new_comment, name="new_comment"),
    path('<int:article_id>/like', like, name="like"),
    path('<int:article_id>/dislike', dislike, name="dislike"),
    path('search', search, name="search"),
    path('restrict_comment/<int:article_id>', restrict_comment, name="restrict_comment"),
    path('allow_comment/<int:article_id>', allow_comment, name="allow_comment"),
]
