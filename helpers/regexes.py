""" 주로 사용되는 regex 들을 모아두는 모듈입니다. """
import re

email_regex = re.compile(
    r"/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i"
)

nickname_regex = re.compile(
    r"^[a-zA-Z0-9가-힣]{1,10}$"
)  # 영문 & 숫자로 이루어진 길이 1~10인 닉네임만 허용

realname_regex = re.compile(
    r"^[가-힣]+$"
)

password_regex = re.compile(
    r"^\s*(?:\S\s*){8,16}$"
)
