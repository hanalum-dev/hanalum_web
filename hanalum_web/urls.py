"""hanalum_web urls 정의 파일입니다."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include('user.urls', 'user')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
