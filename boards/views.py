""" 게시판(board) views """
from copy import deepcopy as dp

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Board
from history.models import ViewHistory, LikeActivity
from articles.models import Article
from hashtags.models import HashTag
from helpers.default import default_response

hashtag_model = HashTag()
view_history = ViewHistory()
like_activity = LikeActivity()

# def index(request):
#     return render('')

def show(request, board_id):
    """ 게시판 페이지 """
    response = dp(default_response)
    board = get_object_or_404(Board, pk=board_id)
    top_fixed_articles = Article.objects.recent().filter(board=board).published().top_fixed()

    articles = Article.objects.recent().filter(board=board).published().non_top_fixed()

    paginator = Paginator(articles, 5)
    page= request.GET.get('page')
    if page == "" or page == None:
        page = 1

    articles = list(top_fixed_articles) + list(paginator.get_page(page))
    start = max(int(page)-5, 1)
    end = min(int(page)+5, paginator.num_pages)

    for article in articles:
        article.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=article,
        ) or 0
        article.hashtags = hashtag_model.get_hashtag(tagged_object=article)
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

    response.update({
        'board': board,
        'banner_title' : board.title,
        'articles': articles,
        'range': [i for i in range(start, end+1)]
    })

    return render(request, 'boards/show.dj.html', response)
