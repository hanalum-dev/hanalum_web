""" 액티비티 관련 success module 입니다. """

from .success import Success


class LikeSuccess(Success):
    """좋아요 성공"""

    def __init__(self):
        """생성자"""
        super().__init__()
        # TODO: 문구 매끄럽게 바꾸기
        self.msg = "좋아요 처리되었습니다."


class DisLikeSuccess(Success):
    """ 싫어요 성공 """

    def __init__(self):
        """생성자"""
        super().__init__()
        # TODO: 문구 매끄럽게 바꾸기
        self.msg = "싫어요 처리되었습니다."
