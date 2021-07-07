""" Board 모델을 정의하는 모듈입니다. """
from django.db import models
from django_summernote.fields import SummernoteTextField

from hanalum_web.base_model import BaseModel, BaseModelManager

class BoardModelManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True).filter(type=self.model.__name__.lower())

class BoardQuerySet(models.QuerySet):
    """ Board 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시판만 리턴합니다. """
        return self.filter(status='p')

    def priority_order(self):
        # FIXME: 가나다 순이 제대로 안 작동함.
        """ 우선순위 높은 순서에 따라 정렬하고, 우선순위가 같다면 게시판 제목의 가나다 순으로 정렬합니다. """
        return self.order_by('-priority', 'title')


class Board(BaseModel):
    """ 게시판 모델 클래스입니다."""
    class Meta:
        verbose_name = '게시판'
        verbose_name_plural = '게시판'

    objects = BaseModelManager.from_queryset(BoardQuerySet)()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    CREATOR_CATEGORY_CHOICES = (
        ('hanalum', '한아름'),
        ('user', '일반유저')
    )

    BOARD_FORAMT_CATEGORY_CHOICES = (
        ('text', '텍스트 중심'),
        ('gallery', '이미지 중심')
    )

    type = models.CharField(
        verbose_name='게시판 타입',
        max_length=20,
        blank=True,
        null=True,
        default='board',
    )

    title = models.CharField(
        verbose_name='게시판명',
        max_length=100
    )
    creator = models.ForeignKey(
        'users.user',
        verbose_name="게시판 제작자",
        on_delete=models.SET_NULL,
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
    default_article_format = SummernoteTextField(
        verbose_name="기본 작성 포맷",
        null=True,
        blank=True,
        default="",
    )
    board_format_category = models.CharField(
        verbose_name='게시판 기본 형태',
        max_length=10,
        default='text',
        null=False,
        choices=BOARD_FORAMT_CATEGORY_CHOICES
    )
    max_attachment_count = models.IntegerField(
        verbose_name="첨부 파일 최대 개수",
        default=0,
        blank=True,
        null=True,
    )
    priority = models.IntegerField(
        verbose_name="우선순위",
        default=0
    )

    def __str__(self):
        return "{}".format(self.title)


class GalleryBoard(Board):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = 'galleryboard'
        super(GalleryBoard, self).__init__(*args, **kwargs)

    objects = BoardModelManager.from_queryset(BoardQuerySet)()

class BoardAdminUser(models.Model):
    """ 게시판 관리자 유저 모델"""
    class Meta:
        verbose_name = '게시판 어드민 유저'
        verbose_name_plural = '게시판 어드민 유저'

    user = models.ForeignKey(
        'users.user',
        verbose_name="게시판 관리자",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    board = models.ForeignKey(
        'boards.board',
        verbose_name="게시판",
        on_delete=models.SET_NULL,
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
