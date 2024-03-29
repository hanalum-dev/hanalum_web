from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone

from users.models import User
from configs.base_model import BaseModel, BaseModelManager


class JohaEventSchedule(BaseModel):
    class Meta:
        verbose_name = 'JOHA 이벤트 일정'
        verbose_name_plural = 'JOHA 이벤트 일정'

    receipt_start_at = models.DateTimeField(
        verbose_name="이벤트 시작일",
        blank=False,
        null=False,
    )
    receipt_end_at = models.DateTimeField(
        verbose_name="이벤트 종료일",
        blank=False,
        null=False,
    )

    @classmethod
    def in_progress(cls):
        current_datetime = timezone.localtime()
        return JohaEventSchedule.objects.filter(receipt_start_at__lte=current_datetime, receipt_end_at__gte=current_datetime).count() > 0


class PaperCategory(BaseModel):
    class Meta:
        verbose_name = '논문 카테고리'
        verbose_name_plural = '논문 카테고리'

    content = models.TextField(
        verbose_name="카테고리 항목"
    )


class PaperQuerySet(models.QuerySet):
    """ paper 모델 쿼리셋 클래스입니다. """

    def recent(self):
        """ 최신 논문부터 담아서 리턴합니다. """
        return self.order_by("-created_at")


class Paper(BaseModel):
    class Meta:
        verbose_name = '논문'
        verbose_name_plural = '논문'

    objects = BaseModelManager.from_queryset(PaperQuerySet)()

    title = models.TextField(
        verbose_name="제목",
        blank=False,
        null=False,
    )
    subtitle = models.TextField(
        verbose_name="부제목",
        blank=True,
        null=True,
    )
    summary = models.TextField(
        verbose_name="요약문",
        blank=True,
        null=True,
    )


class PaperAuthor(BaseModel):
    class Meta:
        verbose_name = '논문 저자'
        verbose_name_plural = '논문 저자'

    author = models.ForeignKey(
        User,
        verbose_name="글쓴이",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    paper = models.ForeignKey(
        Paper,
        verbose_name="논문",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )


class PaperVersion(BaseModel):
    class Meta:
        verbose_name = '버전별 논문'
        verbose_name_plural = '버전별 논문'

    paper = models.ForeignKey(
        Paper,
        verbose_name="논문",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    chief = models.ForeignKey(
        User,
        verbose_name="JOHA 프로세스 담당자",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    version_number = models.IntegerField(
        verbose_name="논문 버전",
        blank=False,
        null=False,
        default=0,
    )
    file = models.FileField(
        verbose_name="파일",
        null=False,
        blank=False,
        upload_to='joha_files/%Y/%m/%d',
    )
    comment_to_reviewer = models.TextField(
        verbose_name="리뷰어에게 남기는 요청사항",
        null=True,
        blank=True
    )


class PaperVersionReviewer(BaseModel):
    class Meta:
        verbose_name = '버전별 논문 리뷰어'
        verbose_name_plural = '버전별 논문 리뷰어'

    STATUS_CHOICES = (
        ('unconfirm', '담당자 확인중'),
        ('pending', '리뷰어 배정 완료'),
        ('reviewing', '리뷰 진행중'),
        ('done', '리뷰 완료')
    )

    reviewer = models.ForeignKey(
        User,
        verbose_name="리뷰어",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    paper_version = models.ForeignKey(
        PaperVersion,
        verbose_name="할딩받은 논문 버전",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='논문 버전 리뷰 진행 상태',
        max_length=10,
        default='unconfirm',
        null=False,
        choices=STATUS_CHOICES
    )


class Review(BaseModel):
    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'

    before_version = models.ForeignKey(
        PaperVersion,
        verbose_name="리뷰 대상 논문 버전",
        related_name='before_paper_version',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    current_version = models.ForeignKey(
        PaperVersion,
        verbose_name="리뷰 후 논문 버전",
        related_name='current_paper_version',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="코멘트",
        null=True,
        blank=True,
    )
