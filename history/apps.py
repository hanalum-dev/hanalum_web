""" history 앱 모듈입니다. """
from django.apps import AppConfig
from django.db.models.signals import pre_save


class HistoryConfig(AppConfig):
    """ history 기본 설정 클래스입니다. """
    name = 'history'

    def ready(self):
        import history.signals
