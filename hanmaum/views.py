""" 한마음 views 모듈입니다."""
import json
from copy import deepcopy as dp

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import HanmaumArticle
from history.models import ViewHistory, LikeActivity
from helpers.default import default_response
from comments.models import Comment

def index(request):
    """ index """
    response = dp(default_response)
    response['articles'] = HanmaumArticle.objects.published()

    for article in response['articles']:
        if request.user.is_authenticated:
            article.is_user_in_like = LikeActivity.is_user_in_like(
                _content_object=article,
                _user=request.user
            )
            article.is_user_in_dislike = LikeActivity.is_user_in_dislike(
                _content_object=article,
                _user=request.user
            )

    response.update({
        'banner_title' : '한민 마을의 소리, 한마음',
    })
    return render(request, 'hanmaum/index.dj.html', response)


def show(request, article_id):
    """ show """
    response = dp(default_response)

    article = get_object_or_404(HanmaumArticle, pk=article_id)

    comments = Comment.get_comments(article)

    response.update({
        'banner_title' : article.title,
        'article' : article,
        'comments' : comments,
    })

    # 사용자 접속 로그 추가
    if request.user.is_authenticated:
        ViewHistory.add_history(
            _viewed_obj=article,
            _viewer=request.user
        )

    return render(request, 'hanmaum/show.dj.html', response)

@login_required(login_url='/users/signin')
def edit(request):
    """ edit """
    response = {

    }
    return render(request, 'hanmaum/edit.dj.html', response)

@login_required(login_url='/users/signin')
def new(request):
    """ new """
    response = dp(default_response)

    return render(request, 'hanmaum/new.dj.html', response)

def introduce(request):
    response = dp(default_response)

    response.update({
        'banner_title': '한민 마을의 소리, 한마음',
        'banner_sub_title': '여러분들에게 한민의 소리를 전해드립니다.'
    })

    return render(request, 'hanmaum/introduce.dj.html', response)


@login_required(login_url='/users/signin')
def like(request):
    """ 좋아요 view""" 
    response = {
        'status' : False   
    }

    article_id = request.POST.get('article_id')

    article = get_object_or_404(HanmaumArticle, pk=article_id)
    # TODO: validation 추가하기
    
    user = request.user

    activity_result = LikeActivity.set_user_in_like(
        _content_object=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url='/users/signin')
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
        _content_object=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url='/users/signin')
def cancle(request):

    """ 좋아요/싫어요 취소 view """
    response = {
        'status' : False   
    }
    
    article_id = request.POST.get('article_id')
    article = get_object_or_404(HanmaumArticle, pk=article_id)
    # TODO: validation 추가하기

    user = request.user

    activity_result = LikeActivity.set_user_in_none(
        _content_object=article,
        _user=user
    )

    response['status'] = activity_result.status

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required(login_url='/users/signin')
def new_comment(request, article_id):

    hanmaum_article = get_object_or_404(HanmaumArticle, pk=article_id)
    user = request.user
    content = request.POST.get('content')

    parent_id = request.POST.get('parent_id')
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    else:
        parent = None

    Comment.new_comment(
        _commented_object = hanmaum_article,
        _user = user,
        _content = content,
        _parent=parent
    )

    # TODO: 댓글이 작성되었습니다. 메세지 띄우기
    return redirect("hanmaum:show", article_id)