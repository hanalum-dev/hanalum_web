"""user 관련 urls 정의 파일입니다."""
from django.urls import path

from .views import (activate_account, delete, edit, me, show, signin, signout, signup, password_edit)

app_name = 'users'

urlpatterns = [
    path('signin', signin, name="signin"),
    path('signup', signup, name="signup"),
    path('signout', signout, name="signout"),
    path('me', me, name="me"),
    path('<int:user_id>', show, name="show"),
    path('edit', edit, name="edit"),
    path('password/edit',password_edit, name="password_edit"),
    path('delete', delete, name="delete"),
    path('activate_account/<str:uidb64>/<str:token>/', activate_account, name="activate_account")
]
