""" 한마음 views 모듈입니다."""

from django.shortcuts import get_object_or_404, render
from django.contrib import auth

from .models import HanmaumArticle
from history.models import ViewHistory

def index(request):
    """ index """
    response = {
        'banner_title' : '한민 마을의 소리, 한마음'
    }
    response['articles'] = HanmaumArticle.objects.published()
    return render(request, 'hanmaum/index.html', response)


def show(request, article_id):
    """ show """
    response = {
    }

    article = get_object_or_404(HanmaumArticle, pk=article_id)

    response['article'] = article
    response['banner_title'] = article.title

    # 사용자 접속 로그 추가
    if request.user.is_authenticated:
        ViewHistory().add_history(_viewed_model=HanmaumArticle().classname(),_viewed_id=article_id, _viewer=request.user)


    return render(request, 'hanmaum/show.html', response)


def edit(request):
    """ edit """
    response = {

    }
    return render(request, 'hanmaum/edit.html', response)


def new(request):
    """ new """
    response = {

    }
    return render(request, 'hanmaum/new.html', response)
