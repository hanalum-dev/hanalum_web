"""hanalum_web urls 정의 파일입니다."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main.views import root

urlpatterns = [
    path('', root, name='root'),
    path('summernote/', include('django_summernote.urls')),
    path("user/", include('user.urls', 'user')),
    path("main/", include('main.urls', 'main')),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
