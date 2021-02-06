""" 한마음 views 모듈입니다."""
import json

from django.shortcuts import get_object_or_404, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import HanmaumArticle
from history.models import ViewHistory, LikeActivity


HANMAUMARTICLE = HanmaumArticle().classname()

def index(request):
    """ index """
    response = {
        'banner_title' : '한민 마을의 소리, 한마음'
    }
    response['articles'] = HanmaumArticle.objects.published()

    for article in response['articles']:
        article.total_viewed_count = ViewHistory().total_viewed_count(
            _viewed_model=HANMAUMARTICLE,
            _viewed_id=article.id
        )
        if request.user.is_authenticated:
            article.is_user_in_like = LikeActivity().is_user_in_like(
                _activity_model=HANMAUMARTICLE,
                _activity_id=article.id,
                _user=request.user
            )
            article.is_user_in_dislike = LikeActivity().is_user_in_dislike(
                _activity_model=HANMAUMARTICLE,
                _activity_id=article.id,
                _user=request.user
            )
    return render(request, 'hanmaum/index.dj.html', response)


def show(request, article_id):
    """ show """
    response = {
    }

    article = get_object_or_404(HanmaumArticle, pk=article_id)

    response['article'] = article
    response['banner_title'] = article.title

    # 사용자 접속 로그 추가
    if request.user.is_authenticated:
        ViewHistory().add_history(
            _viewed_model=HANMAUMARTICLE,
            _viewed_id=article_id,
            _viewer=request.user
        )


    return render(request, 'hanmaum/show.dj.html', response)

@login_required(login_url='/user/signin')
def edit(request):
    """ edit """
    response = {

    }
    return render(request, 'hanmaum/edit.dj.html', response)

@login_required(login_url='/user/signin')
def new(request):
    """ new """
    response = {

    }
    return render(request, 'hanmaum/new.dj.html', response)

@login_required(login_url='/user/signin')
def like(request, article_id):
    """ 좋아요 view""" 
    response = {
        'status' : False   
    }
    
    user = request.user

    activity_result = LikeActivity().set_user_in_like(
        _activity_model=HANMAUMARTICLE,
        _activity_id=article_id,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url='/user/signin')
def dislike(request, article_id):
    """ 싫어요 view """
    response = {
        'status' : False   
    }
    
    user = request.user

    activity_result = LikeActivity().set_user_in_like(
        _activity_model=HANMAUMARTICLE,
        _activity_id=article_id,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")