""" 게시글(article) views """
from copy import deepcopy as dp

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from board.models import Board
from comment.models import Comment
from .models import Article
from .forms import ArticleCreationForm, ArticleEditionForm
from helpers.default import default_response
from history.models import ViewHistory, LikeActivity
from hashtag.models import HashTag

view_history = ViewHistory()
hashtag_model = HashTag()
comment_model = Comment()

def get_hashtag_list(hashtags_str):
    ret = []
    for hashtag in hashtags_str.split("#"):
        if len(hashtag) > 0:
            ret.append("#" + hashtag)
    return ret


def show(request, article_id):
    """ 게시글 상세 페이지 """
    # TODO: validation 추가
    response = dp(default_response)
    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment().get_comments(article)
    is_author = article.author == current_user

    if article.status != 'p':
        messages.error(request, '삭제된 글입니다.')
        return redirect("board:show", article.board.id)

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

    return render(request, 'article/show.dj.html', response)

@login_required(login_url='/user/signin')
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
                return redirect("user:signin")

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

            messages.success(request, '글이 작성되었습니다.'+hashtags_str)
            return redirect("article:show", article.id)
        return redirect("/")
    else:
        response['form'] = ArticleCreationForm()
        return render(request, 'article/new.dj.html', response)


@login_required(login_url='/user/signin')
def edit(request, article_id):
    response = dp(default_response)

    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 수정하실 수 없습니다.')
        return redirect("article:show", article_id)

    form = ArticleEditionForm(request.POST or None, instance=article)

    response.update({
        'form' : form,
        'article' : article,
        'banner_title' : "[수정] {}".format(article.title),
    })

    if request.POST and form.is_valid():
        form.save()
        return redirect("article:show", article_id)

    return render(request, 'article/edit.dj.html', response)

@login_required(login_url='/user/signin')
def delete(request, article_id):
    current_user = request.user
    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 삭제하실 수 없습니다.')
        return redirect("article:show", article_id)

    article.status = 't'
    article.save()
    messages.success(request, '글이 삭제되었습니다.')

    return redirect("board:show", article.board.id)


@login_required(login_url='/user/signin')
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
    return redirect("article:show", article_id)
