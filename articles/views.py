""" 게시글(articles) views """
from copy import deepcopy as dp

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from boards.models import Board
from comments.models import Comment
from .models import Article
from .forms import ArticleCreationForm, ArticleEditionForm
from helpers.default import default_response
from history.models import ViewHistory, LikeActivity
from hashtags.models import HashTag

view_history = ViewHistory()
hashtag_model = HashTag()
comment_model = Comment()
like_activity = LikeActivity()

def get_hashtag_list(hashtags_str):
    ret = []
    for hashtag in hashtags_str.split("\n"):
        if len(hashtag) > 0:
            ret.append(hashtag)
    return ret


def show(request, article_id):
    """ 게시글 상세 페이지 """
    # TODO: validation 추가
    response = dp(default_response)
    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment().get_comments(article)

    article.like_count = like_activity.get_like_count(
        _content_object=article
    )
    article.dislike_count = like_activity.get_dislike_count(
        _content_object=article
    )

    if current_user.is_authenticated:
        article.is_user_in_like = like_activity.is_user_in_like(
            _content_object=article,
            _user=current_user
        )
        article.is_user_in_dislike = like_activity.is_user_in_dislike(
            _content_object=article,
            _user=current_user
        )
    is_author = article.author == current_user

    if article.status != 'p':
        messages.error(request, '삭제된 글입니다.')
        return redirect("boards:show", article.board.id)

    hashtags = hashtag_model.get_hashtag(tagged_object=article)

    response.update({
        'banner_title' : article.title,
        'article' : article,
        'comments' : comments,
        'is_author' : is_author,
        'hashtags' : hashtags,
    })

    # 사용자 접속 로그 추가
    if current_user.is_authenticated:
        view_history.add_history(
            _viewed_obj=article,
            _viewer=current_user
        )

    return render(request, 'articles/show.dj.html', response)

@login_required(login_url='/users/signin')
def new(request, board_id):
    response = dp(default_response)
    response.update({
        'board_id': board_id,
        'form': ArticleCreationForm()
    })

    current_board = get_object_or_404(Board, pk=board_id)  # 현재 글을 작성 중인 게시판
    response['board'] = current_board
    response['banner_title'] = current_board.title  # 배너 타이틀 지정

    if request.method == 'POST':
        # TODO: Validation 추가하기
        form = ArticleCreationForm(request.POST)

        if form.is_valid():
            author = request.user
            if author is None:
                # TODO: validation + error message 따로 빼기
                messages.error(request, '로그인 후, 글을 작성해주세요.')
                return redirect("users:signin")

            article = form.save(commit=False)
            article.author = author
            article.board  = current_board
            article.save()

            hashtags_str = request.POST.get('hashtags_str')
            hashtags = get_hashtag_list(hashtags_str)
            for hashtag in hashtags:
                hashtag_model.add_hashtag(
                    article,
                    hashtag
                )

            messages.success(request, '글이 작성되었습니다.')
            return redirect("articles:show", article.id)
        messages.error(request, "글 작성 중 오류가 발생하였습니다.")
        return redirect("boards:show", board_id)
    else:
        response['form'] = ArticleCreationForm(initial={'content': (current_board.default_article_format or "")})
        return render(request, 'articles/new.dj.html', response)


@login_required(login_url='/users/signin')
def edit(request, article_id):
    response = dp(default_response)

    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 수정하실 수 없습니다.')
        return redirect("articles:show", article_id)

    form = ArticleEditionForm(request.POST or None, instance=article)

    hashtags = hashtag_model.get_hashtag(tagged_object=article)
    hashtags_str = ""
    for hashtag in hashtags:
        hashtags_str += hashtag.content

    response.update({
        'form' : form,
        'article' : article,
        'banner_title' : "[수정] {}".format(article.title),
        'hashtags_str' : hashtags_str,
    })

    if request.POST and form.is_valid():
        form.save()

        hashtags_str = request.POST.get('hashtags_str')
        hashtags = get_hashtag_list(hashtags_str)
        hashtag_model.destroy_all_hashtag(
            article
        )
        for hashtag in hashtags:
            hashtag_model.add_hashtag(
                article,
                hashtag
            )
        messages.success(request, '글이 수정되었습니다.')
        return redirect("articles:show", article_id)

    return render(request, 'articles/edit.dj.html', response)

@login_required(login_url='/users/signin')
def delete(request, article_id):
    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 삭제하실 수 없습니다.')
        return redirect("articles:show", article_id)

    board_id = article.board.id
    article.delete()
    messages.success(request, '글이 삭제되었습니다.')

    return redirect("boards:show", board_id)


@login_required(login_url='/users/signin')
def new_comment(request, article_id):

    article = get_object_or_404(Article, pk=article_id)
    user = request.user
    content = request.POST.get('content')

    parent_id = request.POST.get('parent_id')
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    else:
        parent = None

    comment_model.new_comment(
        _commented_object = article,
        _user = user,
        _content = content,
        _parent=parent
    )

    # TODO: 댓글이 작성되었습니다. 메세지 띄우기
    return redirect("articles:show", article_id)

@login_required(login_url='/users/signin')
def like(request, article_id):
    """ 좋아요 view"""

    article = get_object_or_404(Article, pk=article_id)
    # TODO: validation 추가하기

    user = request.user
    if like_activity.is_user_in_like(_content_object=article, _user=user):
        activity_result = like_activity.set_user_in_none(
            _content_object=article,
            _user=user
        )
    else:
        activity_result = like_activity.set_user_in_like(
            _content_object=article,
            _user=user
        )

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return redirect("articles:show", article_id)

@login_required(login_url='/users/signin')
def dislike(request, article_id):
    """ 싫어요 view """

    article = get_object_or_404(Article, pk=article_id)
    # TODO: validation 추가하기

    user = request.user

    if like_activity.is_user_in_dislike(_content_object=article, _user=user):
        activity_result = like_activity.set_user_in_none(
            _content_object=article,
            _user=user
        )
    else:
        activity_result = like_activity.set_user_in_dislike(
            _content_object=article,
            _user=user
        )

    if activity_result.status:
        messages.success(request, activity_result.msg)
    else:
        messages.error(request, activity_result.msg)

    return redirect("articles:show", article_id)
