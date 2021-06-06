""" user(사용자 계정) validations 데이터 검증 모듈입니다."""
from helpers.error import Error
from helpers.regexes import (email_regex, nickname_regex, password_regex,
                             realname_regex)
from helpers.success import Success
from helpers.user_errors import (AlreadyRegisteredEmailError,
                                 AlreadyRegisteredNicknameError,
                                 InvalidFormatEmailError,
                                 InvalidFormatNicknameError,
                                 InvalidFormatPasswordError,
                                 InvalidFormatRealnameError,
                                 MismatchedPasswordError, NoInputEmailError,
                                 NoInputNicknameError, NoInputPasswordError,
                                 NoInputRealnameError)
from helpers.user_successes import UserCreationValidationSuccess, UserPasswordEditionValidationSuccess

from .models import User


class UserCreationValidator:
    """사용자 생성 데이터 검증 클래스"""

    def validate(self, _email, _nickname, _realname, _password1, _password2):
        """사용자 생성 validation"""

        v_email = self.validate_email(_email)
        v_nickname = self.validate_nickname(_nickname)
        v_realname = self.validate_realname(_realname)
        v_password = self.validate_password(_password1, _password2)

        e = Error()
        e.msg = {}

        if not v_email.status:
            e.msg['email'] = v_email
        if not v_nickname.status:
            e.msg['nickname'] = v_nickname
        if not v_realname.status:
            e.msg['realname'] = v_realname
        if not v_password.status:
            e.msg['password'] = v_password

        if e.msg != {}:
            return e

        return UserCreationValidationSuccess()

    def validate_email(self, _email):
        """ 이메일 validation"""

        if _email is None:
            return NoInputEmailError()

        is_match = email_regex.match(_email)

        if is_match is None:
            return InvalidFormatEmailError()

        if User.objects.filter(email=_email).count() > 0:
            return AlreadyRegisteredEmailError()

        return Success()

    def validate_nickname(self, _nickname):
        """ 닉네임 validation"""

        if _nickname is None:
            return NoInputNicknameError()

        is_match = nickname_regex.match(_nickname)

        if is_match is None:
            return InvalidFormatNicknameError()

        if User.objects.filter(nickname=_nickname).count() > 0:
            return AlreadyRegisteredNicknameError()

        return Success()

    def validate_realname(self, _realname):
        """ 이름 validation """

        if _realname is None:
            return NoInputRealnameError()

        is_match = realname_regex.match(_realname)

        if is_match is None:
            return InvalidFormatRealnameError()

        return Success()

    def validate_password(self, _password1, _password2):
        """ 비밀번호 validation """

        if _password1 is None or _password2 is None:
            return NoInputPasswordError()

        is_match = password_regex.match(_password1)

        if is_match is None:
            return InvalidFormatPasswordError()

        if _password1 != _password2:
            return MismatchedPasswordError()

        return Success()


class UserEditionValidator:
    """사용자 수정 데이터 검증 클래스"""

    def validate_nickname(self, current_user, _nickname):
        """ 닉네임 validation """
        # TODO : 내용 작성
        return Success()

class UserPasswordEditionValidator:
    """ 사용자 비밀번호 변경 데이터 검증 클래스"""

    def validate(self, _password1, _password2):
        """사용자 생성 validation"""

        v_password = self.validate_password(_password1, _password2)

        e = Error()
        e.msg = {}

        if not v_password.status:
            e.msg['password'] = v_password

        if e.msg != {}:
            return e

        return UserPasswordEditionValidationSuccess()

    def validate_password(self, _password1, _password2):
        """ 비밀번호 validation """

        if _password1 is None or _password2 is None:
            return NoInputPasswordError()

        is_match = password_regex.match(_password1)

        if is_match is None:
            return InvalidFormatPasswordError()

        if _password1 != _password2:
            return MismatchedPasswordError()

        return Success()