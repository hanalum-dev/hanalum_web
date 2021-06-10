""" 한마음 views 모듈입니다."""
import json
from copy import deepcopy as dp

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from hanalum_web.base_views import catch_all_exceptions
from .models import HanmaumArticle
from history.models import ViewHistory, LikeActivity
from helpers.default import default_response
from comments.models import Comment
from hanmaum.validators import HanmaumArticlePermissionValidator
from .forms import HanmaumCreationForm

@catch_all_exceptions
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


@catch_all_exceptions
def show(request, article_id):
    """ show """
    response = dp(default_response)
    current_user = request.user

    HanmaumArticlePermissionValidator.show(current_user, article_id)

    article = HanmaumArticle.objects.get(pk=article_id)

    comments = Comment.get_comments(article)

    if current_user.is_authenticated:
        article.is_user_in_like = LikeActivity.is_user_in_like(
            _content_object=article,
            _user=current_user
        )
        article.is_user_in_dislike = LikeActivity.is_user_in_dislike(
            _content_object=article,
            _user=current_user
        )
        ViewHistory.add_history(
            _viewed_obj=article,
            _viewer=current_user
        )  # 사용자 접속 로그 추가

    next_article = get_next_article(article_id=article_id)
    prev_article = get_prev_article(article_id=article_id)

    response.update({
        'banner_title' : article.title,
        'article' : article,
        'comments' : comments,
        'next_article': next_article,
        'prev_article': prev_article,
    })

    return render(request, 'hanmaum/show.dj.html', response)

@catch_all_exceptions
@login_required(login_url='/users/signin')
def edit(request):
    """ edit """
    response = {

    }
    return render(request, 'hanmaum/edit.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def new(request):
    """hanmaum#new"""
    response = dp(default_response)
    response.update({
        'form': HanmaumCreationForm()
    })
    current_user = request.user

    HanmaumArticlePermissionValidator.new(current_user)

    if request.method == 'POST':
        form = HanmaumCreationForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)

            article.save()

            # hashtags_str = request.POST.get('hashtags_str')
            # hashtags = get_hashtag_list(hashtags_str)
            # for hashtag in hashtags:
            #     HashTag.add_hashtag(
            #         article,
            #         hashtag
            #     )

            messages.success(request, '글이 작성되었습니다.')
            return redirect("hanmaum:show", article.id)
        messages.error(request, "글 작성 중 오류가 발생하였습니다.")
        return redirect("hanmaum:index")
    else:
        return render(request, 'hanmaum/new.dj.html', response)

def introduce(request):
    response = dp(default_response)

    response.update({
        'banner_title': '한민 마을의 소리, 한마음',
        'banner_sub_title': '여러분들에게 한민의 소리를 전해드립니다.'
    })

    return render(request, 'hanmaum/introduce.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def like(request, article_id):
    """article을 좋아요 처리합니다."""

    current_user = request.user
    HanmaumArticlePermissionValidator.like(current_user, article_id)
    article = HanmaumArticle.objects.filter(pk=article_id).first()

    if LikeActivity.is_user_in_like(_content_object=article, _user=current_user):
        activity_result = LikeActivity.set_user_in_none(
            _content_object=article,
            _user=current_user
        )
    else:
        activity_result = LikeActivity.set_user_in_like(
            _content_object=article,
            _user=current_user
        )

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return redirect("hanmaum:show", article_id)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def dislike(request, article_id):
    """article을 싫어요 처리합니다."""

    current_user = request.user

    HanmaumArticlePermissionValidator.dislike(current_user, article_id)
    article = get_object_or_404(HanmaumArticle, pk=article_id)

    if LikeActivity.is_user_in_dislike(_content_object=article, _user=current_user):
        activity_result = LikeActivity.set_user_in_none(
            _content_object=article,
            _user=current_user
        )
    else:
        activity_result = LikeActivity.set_user_in_dislike(
            _content_object=article,
            _user=current_user
        )

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return redirect("hanmaum:show", article_id)

@catch_all_exceptions
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


def get_next_article(article_id):
    """다음 게시글을 반환합니다."""
    return HanmaumArticle.objects.published().order_by('pk').filter(pk__gt=article_id).first()


def get_prev_article(article_id):
    """이전 게시글을 반환합니다."""
    return HanmaumArticle.objects.published().order_by('pk').filter(pk__lt=article_id).last()
