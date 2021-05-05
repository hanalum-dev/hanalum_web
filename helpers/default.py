"""기본 값들에 대한 helper 모듈입니다."""
from boards.models import Board

default_response = {
    'nav_board_list' : Board.objects.published().priority_order().all()
}
