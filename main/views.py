"""main(루트 페이지) views 모듈입니다."""
from django.shortcuts import render

from .models import TopBanner


def get_top_banner():
    """ TopBanner를 가져오는 함수입니다. """
    banner = TopBanner.objects.get(is_active=True)
    return banner


def root(request):
    """ 루트 페이지 뷰입니다. """
    response = {
        'top_banner': get_top_banner(),
    }
    return render(request, 'main/index.html', response)
