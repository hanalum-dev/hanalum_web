""" user 앱 관련 success module 입니다. """

from .success import Success


class UserCreationSuccess(Success):
    """계정 생성 성공"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "회원가입이 완료되었습니다."


class UserCreationValidationSuccess(Success):
    """ 사용자 생성 데이터 검증 성공 """

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "정상적으로 입력되었습니다."
