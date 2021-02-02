""" 한마음 views 모듈입니다."""

from django.shortcuts import get_object_or_404, render

from .models import HanmaumArticle


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
