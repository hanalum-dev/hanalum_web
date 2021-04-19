"""hanalum_web urls 정의 파일입니다."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from main.views import root

urlpatterns = [
    path('', root, name='root'),
    path('summernote/', include('django_summernote.urls')),
    path("user/", include('user.urls', 'user')),
    path("main/", include('main.urls', 'main')),
    path("notice/", include('notice.urls', 'notice')),
    path("articles/", include('articles.urls', 'articles')),
    path("board/", include('board.urls', 'board')),
    path("comment/", include('comment.urls', 'comment')),
    path("hanmaum/", include('hanmaum.urls', 'hanmaum')),
    path("admin/", admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root' : settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
