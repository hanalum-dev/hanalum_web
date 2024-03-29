""" history 앱 모듈입니다. """
from django.apps import AppConfig


class HistoryConfig(AppConfig):
    """ history 기본 설정 클래스입니다. """
    name = 'history'
    verbose_name = '로그 모음'

    def ready(self):
        import history.signals
