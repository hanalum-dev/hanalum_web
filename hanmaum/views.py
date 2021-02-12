""" 한마음 views 모듈입니다."""
import json

from django.shortcuts import get_object_or_404, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import HanmaumArticle
from history.models import ViewHistory, LikeActivity
from helpers.default import default_response
from copy import deepcopy as dp

like_activity = LikeActivity()
view_history = ViewHistory()

def index(request):
    """ index """
    response = dp(default_response)
    response.update({
        'banner_title' : '한민 마을의 소리, 한마음',
        'articles': HanmaumArticle.objects.published()
    })

    for article in response['articles']:
        article.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=article,
        )
        if request.user.is_authenticated:
            article.is_user_in_like = like_activity.is_user_in_like(
                _content_obj=article,
                _user=request.user
            )
            article.is_user_in_dislike = LikeActivity().is_user_in_dislike(
                _content_obj=article,
                _user=request.user
            )
    return render(request, 'hanmaum/index.dj.html', response)


def show(request, article_id):
    """ show """
    response = dp(default_response)

    article = get_object_or_404(HanmaumArticle, pk=article_id)

    response['article'] = article
    response['banner_title'] = article.title

    # 사용자 접속 로그 추가
    if request.user.is_authenticated:
        view_history.add_history(
            _viewed_obj=article,
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
    response = dp(default_response)

    return render(request, 'hanmaum/new.dj.html', response)

@login_required(login_url='/user/signin')
def like(request):
    """ 좋아요 view""" 
    response = {
        'status' : False   
    }

    article_id = request.POST.get('article_id')

    article = get_object_or_404(HanmaumArticle, pk=article_id)
    # TODO: validation 추가하기
    
    user = request.user

    activity_result = like_activity.set_user_in_like(
        _content_obj=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url='/user/signin')
def dislike(request):
    """ 싫어요 view """
    response = {
        'status' : False   
    }

    article_id = request.POST.get('article_id')
    article = get_object_or_404(HanmaumArticle, pk=article_id)
    # TODO: validation 추가하기

    user = request.user

    activity_result = LikeActivity().set_user_in_dislike(
        _content_obj=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url='/user/signin')
def cancle(request):

    """ 좋아요/싫어요 취소 view """
    response = {
        'status' : False   
    }
    
    article_id = request.POST.get('article_id')
    article = get_object_or_404(HanmaumArticle, pk=article_id)
    # TODO: validation 추가하기

    user = request.user

    activity_result = like_activity.set_user_in_none(
        _content_obj=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")