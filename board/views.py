""" 게시판(board) views """
from django.shortcuts import get_object_or_404, render
from helpers.default import default_response
from copy import deepcopy as dp

from .models import Board
from history.models import ViewHistory, LikeActivity
from article.models import Article

view_history = ViewHistory()
like_activity = LikeActivity()

# def index(request):
#     return render('')

def show(request, board_id):
    """ 게시판 페이지 """
    response = dp(default_response)
    board = get_object_or_404(Board, pk=board_id)
    response.update({
        'board': board,
        'banner_title' : board.title
    })
    articles = Article.objects.recent().filter(board= board).published().all()

    for article in articles:
        article.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=article,
        ) or 0
        article.like_count = like_activity.get_like_count(
            _content_object=article
        )
        article.dislike_count = like_activity.get_dislike_count(
            _content_object=article
        )

        if request.user.is_authenticated:
            article.is_user_in_like = like_activity.is_user_in_like(
                _content_object=article,
                _user=request.user
            )
            article.is_user_in_dislike = like_activity.is_user_in_dislike(
                _content_object=article,
                _user=request.user
            )


    # TODO: pagination

    response['articles'] = articles

    return render(request, 'board/show.dj.html', response)
