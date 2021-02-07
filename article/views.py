""" 게시글(article) views """
from helpers.default import default_response
from copy import deepcopy as dp

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from board.models import Board
from .models import Article
from .forms import ArticleCreationForm
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
            messages.success(request, '글이 작성되었습니다.')
            return redirect("article:show", article.id)
        return redirect("/")
    else:
        response['form'] = ArticleCreationForm()
        return render(request, 'articles/new.dj.html', response)
