""" notice(공지사항) view 모듈 파일입니다. """
from copy import deepcopy as dp

from django.shortcuts import render, get_object_or_404
from helpers.default import default_response

from .models import Notice

def index(request):
    response = dp(default_response)
    response.update({
        'banner_title' : '공지사항',
        'top_fixed_notices' : Notice.objects.published().top_fixed().recent(),
        'non_top_fixed_notices' : Notice.objects.published().non_top_fixed().recent(),
    })

    # TODO: HNM-0097: 공지사항 페이지네이션 추가

    return render(request, 'notice/index.dj.html', response)


def show(request, notice_id):
    response = dp(default_response)

    notice = get_object_or_404(Notice, pk=notice_id)

    response.update({
        'banner_title' : "[공지사항] " + notice.title,
        'notice' : notice,
    })

    return render(request, 'notice/show.dj.html', response)
