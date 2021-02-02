""" Board 모델을 정의하는 모듈입니다. """
from django.db import models


class BoardQuerySet(models.QuerySet):
    """ Board 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시판만 리턴합니다. """
        return self.filter(status='p')


class Board(models.Model):
    """ 게시판 모델 클래스입니다."""
    objects = BoardQuerySet.as_manager()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    title = models.CharField(verbose_name='게시판명', max_length=100)
    auth_read = models.IntegerField(verbose_name='읽기 권한', default=10, null=False)
    auth_write = models.IntegerField(verbose_name='쓰기 권한', default=10, null=False)
    use_comment = models.BooleanField(verbose_name='댓글 사용 여부', default=True, null=False)
    use_good = models.BooleanField(verbose_name='좋아요 사용 여부', default=True, null=False)
    use_bad = models.BooleanField(verbose_name='싫어요 사용 여부', default=True, null=False)
    use_anonymous = models.BooleanField(verbose_name='익명 사용 가능 여부', default=False, null=False)
    status = models.CharField(verbose_name='게시판 공개 상태', max_length=2, default='d', null=False, choices=STATUS_CHOICES)

    def __str__(self):
        return "{}".format(self.title)
