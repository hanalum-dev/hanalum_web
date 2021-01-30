"""user 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import delete, edit, show, signin, signout, signup, update

urlpatterns = [
    path('signin', signin, name="signin"),
    path('signup', signup, name="signup"),
    path('signout', signout, name="signout"),
    path('show', show, name="show"),
    path('edit', edit, name="edit"),
    path('update', update, name="update"),
    path('delete', delete, name="delete"),
]
