"""board validator"""
from helpers.exeptions import NoPermissionException

from .models import Board


class BoardPermissionValidator():
    """Board views마다의 권한 제어 클래스"""

    @classmethod
    def show(cls, current_user, board_id):
        """show validator"""
        board = Board.objects.filter(pk=board_id).first()

        if not current_user or not current_user.is_authenticated:
            if board.auth_read > 0 or not board.visible_anonymous:
                raise NoPermissionException()
