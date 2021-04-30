""" 게시판(board) views """
from copy import deepcopy as dp

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from articles.models import Article
from articles.views import get_recent_popular_articles
from hashtags.models import HashTag
from helpers.default import default_response
from history.models import LikeActivity, ViewHistory

from .models import Board

hashtag_model = HashTag()
view_history = ViewHistory()


def show(request, board_id):
    """게시판 페이지"""
    response = dp(default_response)
    board = get_object_or_404(Board, pk=board_id)
    top_fixed_articles = Article.objects.filter(board=board)\
        .published().top_fixed().recent()

    articles = Article.objects.recent().filter(board=board).published().non_top_fixed()
    popular_articles = get_recent_popular_articles(board_id=board_id)

    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    if page == "" or page is None:
        page = 1

    articles = list(top_fixed_articles) + list(paginator.get_page(page))
    start = max(int(page) - 5, 1)
    end = min(int(page) + 5, paginator.num_pages)

    for article in articles:
        article.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=article,
        ) or 0
        article.hashtags = hashtag_model.get_hashtag(tagged_object=article)
        article.like_count = LikeActivity.get_like_count(
            _content_object=article
        )
        article.dislike_count = LikeActivity.get_dislike_count(
            _content_object=article
        )

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
        'board': board,
        'banner_title' : board.title,
        'articles': articles,
        'popular_articles': popular_articles,
        'range': list(range(start, end + 1))
    })

    return render(request, 'boards/show.dj.html', response)
