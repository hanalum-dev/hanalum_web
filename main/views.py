"""main(루트 페이지) views 모듈입니다."""
from copy import deepcopy as dp

from django.shortcuts import render
from board.models import Board

from articles.models import Article
from .models import TopBanner, MainBoard
from helpers.default import default_response


def get_top_banner():
    """ TopBanner를 가져오는 함수입니다. """
    try:
        banner = TopBanner.objects.get(is_active=True)
        return banner
    except TopBanner.DoesNotExist:  # pylint: disable=no-member
        return None


def root(request):
    """ 루트 페이지 뷰입니다. """
    response = dp(default_response)
    published_boards = Board.objects.published().all()
    main_boards = MainBoard.objects.priority_order().all()

    response.update({
        'top_banner': get_top_banner(),
        'boards' : published_boards,
        'main_boards': main_boards
    })

    return render(request, 'main/index.dj.html', response)
