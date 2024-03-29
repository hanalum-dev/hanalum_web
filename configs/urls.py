"""config urls 정의 파일입니다."""
from copy import deepcopy as dp
from policies.views import personal_information
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.shortcuts import render
from django.views.static import serve
from main.views import root
from helpers.default import default_response

urlpatterns = [
    path('', root, name='root'),
    path('summernote/', include('django_summernote.urls')),
    path("users/", include('users.urls', 'users')),
    path("main/", include('main.urls', 'main')),
    path("notices/", include('notices.urls', 'notices')),
    path("articles/", include('articles.urls', 'articles'), name='articles'),
    path("boards/", include('boards.urls', 'boards')),
    path("mailers/", include('mailers.urls', 'mailers')),
    path("comments/", include('comments.urls', 'comments')),
    path("hanmaum/", include('hanmaum.urls', 'hanmaum')),
    path("joha/", include('joha.urls', 'joha')),
    path("admin/", admin.site.urls),
    path("policy/personal_information", personal_information),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root' : settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
