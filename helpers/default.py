from boards.models import Board

default_response = {
    'nav_board_list' : Board.objects.published().all()
}