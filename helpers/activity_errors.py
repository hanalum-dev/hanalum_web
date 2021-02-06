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


class AlreadyNoneActivityArticle(Error):
    """ (실제로는 발생할 수는 없지만) None 상태에서 None 상태가 된 경우 에러 클래스 """

    def __init__(self):
        """생성자"""
        super().__init__()
        self.msg = "알 수 없는 에러가 발생하였습니다."

