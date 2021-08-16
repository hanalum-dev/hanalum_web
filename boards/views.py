""" 게시판(board) views """
from copy import deepcopy as dp

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from articles.models import Article
from articles.views import get_recent_popular_articles
from hashtags.models import HashTag
from configs.base_views import catch_all_exceptions
from helpers.default import default_response
from history.models import LikeActivity, ViewHistory

from .models import Board
from .validators import BoardPermissionValidator


@catch_all_exceptions
def show(request, board_id):
    """게시판 페이지"""
    response = dp(default_response)
    board = get_object_or_404(Board, pk=board_id)
    current_user = request.user
    BoardPermissionValidator.show(current_user, board_id)

    top_fixed_articles = Article.objects.filter(board=board)\
        .published().top_fixed().recent()

    articles = Article.objects.recent().filter(board=board).published().non_top_fixed()
    popular_articles = get_recent_popular_articles(board_id=board_id)

    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    if page == "" or page is None:
        page = 1

    articles = paginator.get_page(page)
    start = max(int(page) - 5, 1)
    end = min(int(page) + 5, paginator.num_pages)

    for article in articles:
        article.hashtags = HashTag.get_hashtag(tagged_object=article)

        if current_user.is_authenticated:
            article.is_user_in_like = LikeActivity.is_user_in_like(
                _content_object=article,
                _user=current_user
            )
            article.is_user_in_dislike = LikeActivity.is_user_in_dislike(
                _content_object=article,
                _user=current_user
            )

    response.update({
        'board': board,
        'banner_title' : board.title,
        'top_fixed_articles': top_fixed_articles,
        'articles': articles,
        'popular_articles': popular_articles,
        'range': list(range(start, end + 1))
    })

    return render(request, 'boards/show.dj.html', response)
