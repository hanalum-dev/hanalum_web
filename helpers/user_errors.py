""" user 앱 관련 error module 입니다. """

from .error import Error


class InvalidFormatEmailError(Error):
    """올바르지 않은 형식의 이메일 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "형식에 맞는 이메일을 입력해주세요."


class AlreadyRegisteredEmailError(Error):
    """이미 등록된 이메일 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "이미 등록된 이메일입니다."


class NoInputEmailError(Error):
    """입력되지 않은 이메일 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "이메일을 입력해주세요."


class InvalidFormatRealnameError(Error):
    """올바르지 않은 형식의 이름 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "한글 실명을 입력해주세요."


class NoInputRealnameError(Error):
    """입력되지 않은 이름 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "이름을 입력해주세요."


class InvalidFormatNicknameError(Error):
    """올바르지 않은 형식의 닉네임 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "닉네임은 최대 8글자 한글, 영문, 숫자 조합의 문자열만 가능합니다."


class NoInputNicknameError(Error):
    """입력되지 않은 닉네임 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "닉네임을 입력해주세요."


class AlreadyRegisteredNicknameError(Error):
    """이미 등록된 닉네임 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "이미 사용 중인 닉네임입니다."


class AlreadyUsedNicknameError(Error):
    """ 이미 사용자가 사용중인 닉네임 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "현재 닉네임과 동일합니다."


class InvalidFormatPasswordError(Error):
    """올바르지 않는 형식의 비밀번호 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "비밀번호는 8자리 이상 16자리 이하로 만들어져야 합니다."


class MismatchedPasswordError(Error):
    """비밀번호가 일치하지 않는 경우 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "비밀번호가 일치하지 않습니다."


class NoInputPasswordError(Error):
    """입력되지 않은 비밀번호 에러"""

    def __init__(self):
        """생성자"""
        super().__init__()
        self.message = "비밀번호를 입력해주세요."
