""" 게시글(articles) views """
from copy import deepcopy as dp

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from boards.models import Board
from comments.models import Comment
from configs.views import catch_all_exceptions
from hashtags.models import HashTag
from helpers.default import default_response
from history.models import LikeActivity, ViewHistory

from .forms import ArticleCreationForm, ArticleEditionForm
from .models import Article
from .validators import ArticlePermissionValidator


@catch_all_exceptions
def show(request, article_id):
    """articles#show"""

    response = dp(default_response)
    current_user = request.user

    ArticlePermissionValidator.show(current_user, article_id)

    article = Article.objects.get(pk=article_id)
    board = article.board

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
    is_author = article.author == current_user

    hashtags = HashTag.get_hashtag(tagged_object=article)

    next_article = get_next_article(article_id=article_id, board_id=board.id)
    prev_article = get_prev_article(article_id=article_id, board_id=board.id)
    popular_articles = get_recent_popular_articles(board_id=board.id)

    response.update({
        'banner_title' : article.title,
        'article' : article,
        'board': board,
        'comments' : comments,
        'is_author' : is_author,
        'hashtags' : hashtags,
        'next_article': next_article,
        'prev_article': prev_article,
        'popular_articles': popular_articles
    })

    if current_user.is_authenticated:
        ViewHistory.add_history(
            _viewed_obj=article,
            _viewer=current_user
        )

    return render(request, 'articles/show.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def new(request, board_id):
    """articles#new"""
    response = dp(default_response)
    response.update({
        'board_id': board_id,
        'full_screen': True,
        'form': ArticleCreationForm()
    })
    current_user = request.user

    ArticlePermissionValidator.new(current_user, board_id)

    current_board = get_object_or_404(Board, pk=board_id)  # 현재 글을 작성 중인 게시판
    response['board'] = current_board
    response['banner_title'] = current_board.title  # 배너 타이틀 지정

    if request.method == 'POST':
        # TODO: Validation 추가하기
        form = ArticleCreationForm(request.POST)

        if form.is_valid():
            author = current_user
            if author is None:
                # TODO: validation + error message 따로 빼기
                messages.error(request, '로그인 후, 글을 작성해주세요.')
                return redirect("users:signin")

            article = form.save(commit=False)
            article.author = author
            article.board = current_board
            article.save()

            hashtags_str = request.POST.get('hashtags_str')
            hashtags = get_hashtag_list(hashtags_str)
            for hashtag in hashtags:
                HashTag.add_hashtag(
                    article,
                    hashtag
                )

            messages.success(request, '글이 작성되었습니다.')
            return redirect("articles:show", article.id)
        messages.error(request, "글 작성 중 오류가 발생하였습니다.")
        return redirect("boards:show", board_id)
    else:
        response['form'] = ArticleCreationForm(
            initial={'content': (current_board.default_article_format or "")}
        )
        return render(request, 'articles/new.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def edit(request, article_id):
    """articles#edit"""

    response = dp(default_response)

    current_user = request.user
    ArticlePermissionValidator.edit(current_user, article_id)

    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 수정하실 수 없습니다.')
        return redirect("articles:show", article_id)

    form = ArticleEditionForm(request.POST or None, instance=article)

    hashtags = HashTag.get_hashtag(tagged_object=article)
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
        HashTag.destroy_all_hashtag(
            article
        )
        for hashtag in hashtags:
            HashTag.add_hashtag(
                article,
                hashtag
            )
        messages.success(request, '글이 수정되었습니다.')
        return redirect("articles:show", article_id)

    return render(request, 'articles/edit.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def delete(request, article_id):
    """articles#delete"""

    current_user = request.user
    ArticlePermissionValidator.delete(current_user, article_id)

    article = get_object_or_404(Article, pk=article_id)

    if article.author != current_user:
        messages.error(request, '해당 글은 삭제하실 수 없습니다.')
        return redirect("articles:show", article_id)

    board_id = article.board.id
    article.delete()
    messages.success(request, '글이 삭제되었습니다.')

    return redirect("boards:show", board_id)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def new_comment(request, article_id):
    """articles#new_comment"""

    article = get_object_or_404(Article, pk=article_id)
    user = request.user
    content = request.POST.get('content')

    parent_id = request.POST.get('parent_id')
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    else:
        parent = None

    Comment.new_comment(
        _commented_object=article,
        _user=user,
        _content=content,
        _parent=parent
    )

    # TODO: 댓글이 작성되었습니다. 메세지 띄우기
    return redirect("articles:show", article_id)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def like(request, article_id):
    """article을 좋아요 처리합니다."""

    current_user = request.user
    ArticlePermissionValidator.like(current_user, article_id)
    article = Article.objects.filter(pk=article_id).first()

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

    return redirect("articles:show", article_id)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def dislike(request, article_id):
    """article을 싫어요 처리합니다."""

    current_user = request.user

    ArticlePermissionValidator.dislike(current_user, article_id)
    article = get_object_or_404(Article, pk=article_id)

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

    return redirect("articles:show", article_id)


@catch_all_exceptions
def search(request):
    """ GET: search
        params: search_keyword, page
    """

    response = dp(default_response)

    search_keyword = request.GET.get('search_keyword')
    board_id = request.GET.get('board_id')

    articles = Article.objects.published().filter(
        Q(title__contains=search_keyword) | Q(content__contains=search_keyword)
    ).recent()
    popular_articles = get_recent_popular_articles(board_id=board_id)

    if board_id:
        articles = articles.filter(board_id=board_id)

    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    if page == "" or page is None:
        page = 1

    articles = paginator.get_page(page)
    start = max(int(page) - 5, 1)
    end = min(int(page) + 5, paginator.num_pages)

    response.update({
        'search_keyword': search_keyword,
        'articles': articles,
        'popular_articles': popular_articles,
        'range': list(range(start, end + 1)),
        'custom_query': "&search_keyword={}".format(search_keyword)
    })

    return render(request, 'articles/search.html', response)


@catch_all_exceptions
def restrict_comment(request, article_id):
    current_user = request.user
    ArticlePermissionValidator.restrict_comment(current_user, article_id)

    article = Article.objects.get(pk=article_id)
    article.comment_restricted = True
    article.save()

    return redirect('articles:show', article_id)


@catch_all_exceptions
def allow_comment(request, article_id):
    current_user = request.user
    ArticlePermissionValidator.allow_comment(current_user, article_id)

    article = Article.objects.get(pk=article_id)
    article.comment_restricted = False
    article.save()

    return redirect('articles:show', article_id)


def get_hashtag_list(hashtags_str):
    """입력된 hashtag 문자열을 list로 변환하여 반환합니다."""
    ret = []
    for hashtag in hashtags_str.split("\n"):
        if len(hashtag) > 0:
            ret.append(hashtag)
    return ret


def get_recent_popular_articles(board_id=None):
    """인기 게시글을 반환합니다."""
    if board_id:
        return Article.objects.published().filter(board_id=board_id).popular_order().five()
    else:
        return Article.objects.published().popular_order().five()


def get_next_article(article_id, board_id=None):
    """다음 게시글을 반환합니다."""
    if board_id:
        return Article.objects.published().filter(board_id=board_id, pk__gt=article_id).first()
    else:
        return Article.objects.published().filter(pk__gt=article_id).first()


def get_prev_article(article_id, board_id=None):
    """이전 게시글을 반환합니다."""
    if board_id:
        return Article.objects.published().filter(board_id=board_id, pk__lt=article_id).last()
    else:
        return Article.objects.published().filter(pk__lt=article_id).last()
