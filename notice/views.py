""" notice(공지사항) view 모듈 파일입니다. """
from copy import deepcopy as dp

from django.shortcuts import render
from helpers.default import default_response

def index(request):
    response = dp(default_response)
    response.update({
        'banner_title' : '공지사항',
    })

    return render(request, 'notice/index.html', response)