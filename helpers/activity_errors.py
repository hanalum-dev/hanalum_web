""" 액티비티 관련 error module 입니다. """

from .error import Error


class AlreadyLikeArticle(Error):
    """이미 좋아요를 한 게시글 에러 클래스"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.msg = "이미 좋아요를 한 게시글입니다."

class AlreadyDisLikeArticle(Error):
    """이미 싫어요를 한 게시글 에러 클래스"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.msg = "이미 싫어요를 한 게시글입니다."

