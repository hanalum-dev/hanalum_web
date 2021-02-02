""" 한마음 게시글 모델 모듈 파일입니다."""
from django.db import models
from django_summernote.fields import SummernoteTextField


class Hanmaum(models.Model):
    """한마음 게시글 모델입니다."""

    title = models.CharField(verbose_name="인터뷰 제목", max_length=100, default='')
    interviewer = models.CharField(verbose_name="인터뷰어", max_length=10, default='')
    interviewee = models.CharField(verbose_name="인터뷰이", max_length=10, default='')
    content = SummernoteTextField(verbose_name="내용")
    thumnbail = models.ImageField(verbose_name="대표 이미지", null=True, blank=True, upload_to="hanmaum/%Y/%m/%d")
    created_at = models.DateTimeField(verbose_name="생성된 시각", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정된 시각", auto_now=True)

    def __str__(self):
        """ 제목만 표기 """
        return "{}".format(self.title)
