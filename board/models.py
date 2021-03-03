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

    CREATOR_CATEGORY_CHOICES = (
        ('hanalum', '한아름'),
        ('user', '일반유저')
    )

    DEFAULT_BOARD_FORAMT_CHOICES = (
        ('text', '텍스트 중심'),
        ('gallery', '이미지 중심')
    )

    title = models.CharField(
        verbose_name='게시판명',
        max_length=100
    )
    creator = models.ForeignKey(
        'user.user',
        verbose_name="게시판 제작자",
        on_delete = models.DO_NOTHING,
        blank=True,
        null=True
    )
    creator_category = models.CharField(
        verbose_name='게시판 제작자 분류',
        max_length=8,
        default='hanalum',
        null=False,
        choices=CREATOR_CATEGORY_CHOICES
    )
    auth_read = models.IntegerField(
        verbose_name='읽기 권한',
        default=10,
        null=False
    )
    auth_write = models.IntegerField(
        verbose_name='쓰기 권한',
        default=10,
        null=False
    )
    use_comment = models.BooleanField(
        verbose_name='댓글 사용 여부',
        default=True,
        null=False
    )
    use_good = models.BooleanField(
        verbose_name='좋아요 사용 여부',
        default=True,
        null=False
    )
    use_bad = models.BooleanField(
        verbose_name='싫어요 사용 여부',
        default=True,
        null=False
    )
    use_anonymous = models.BooleanField(
        verbose_name='익명 사용 가능 여부',
        default=False,
        null=False
    )
    status = models.CharField(
        verbose_name='게시판 공개 상태',
        max_length=2,
        default='d',
        null=False,
        choices=STATUS_CHOICES
    )
    visible_anonymous = models.BooleanField(
        verbose_name="비로그인 유저의 확인 가능 여부",
        default=True
    )
    default_board_format = models.CharField(
        verbose_name='게시판 기본 형태',
        max_length=10,
        default='text',
        null=False,
        choices=DEFAULT_BOARD_FORAMT_CHOICES
    )
    max_attachment_count = models.IntegerField(
        verbose_name="첨부 파일 최대 개수",
        default=0,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{}".format(self.title)


class BoardAdminUser(models.Model):
    """ 게시판 관리자 유저 모델"""

    user = models.ForeignKey(
        'user.user',
        verbose_name="게시판 관리자",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    board = models.ForeignKey(
        'board.board',
        verbose_name="게시판",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    register_notice_permission = models.BooleanField(
        verbose_name="게시판 내 공지 생성 권한",
        default=True,
        null=False,
    )
    delete_article_permission = models.BooleanField(
        verbose_name="게시글 삭제 권한",
        default=False,
        null=False,
    )  # TODO: 실제로 article이 삭제되면 안 되고, article에 status 추가해서 trash 상태로 바꾸는 권한으로 설정할 것
