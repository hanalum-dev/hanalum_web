""" 게시글(article) views """
from django.shortcuts import render, get_object_or_404
from helpers.default import default_response
from copy import deepcopy as dp

from .models import Article
from history.models import ViewHistory, LikeActivity

ARTICLE = Article().classname()

def show(request, article_id):
    """ 게시글 상세 페이지 """
    # TODO: validation 추가
    response = dp(default_response)
    article = get_object_or_404(Article, pk=article_id)

    response['article'] = article
    response['banner_title'] = article.board.title

    # 사용자 접속 로그 추가
    if request.user.is_authenticated:
        ViewHistory().add_history(
            _viewed_model=ARTICLE,
            _viewed_id=article_id,
            _viewer=request.user
        )

    return render(request, 'articles/show.dj.html', response)