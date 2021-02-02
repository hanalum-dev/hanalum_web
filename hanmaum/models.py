""" 한마음 게시글 모델 모듈 파일입니다."""
from django.db import models
from django_summernote.fields import SummernoteTextField


class HanmaumArticleQuerySet(models.QuerySet):
    """ 한마음 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시판만 리턴합니다. """
        return self.filter(status='p')


class HanmaumArticle(models.Model):
    """한마음 게시글 모델입니다."""
    objects = HanmaumArticleQuerySet.as_manager()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    title = models.CharField(verbose_name="인터뷰 제목", max_length=100, default='')
    interviewer = models.CharField(verbose_name="인터뷰어", max_length=10, default='')
    interviewee = models.CharField(verbose_name="인터뷰이", max_length=10, default='')
    content = SummernoteTextField(verbose_name="내용")
    thumnbail = models.ImageField(verbose_name="대표 이미지", null=True, blank=True, upload_to="hanmaum/%Y/%m/%d")
    created_at = models.DateTimeField(verbose_name="생성된 시각", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정된 시각", auto_now=True)
    status = models.CharField(verbose_name='게시글 공개 상태', max_length=2, default='d', null=False, choices=STATUS_CHOICES)

    def __str__(self):
        """ 제목만 표기 """
        return "{}".format(self.title)
