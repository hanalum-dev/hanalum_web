"""user(사용자 계정) 토큰 제네레이터 모듈입니다."""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    """user(사용자 계정) 토큰 제네레이터입니다."""

    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp)) + str(user.is_active)


account_activation_token = UserActivationTokenGenerator()
