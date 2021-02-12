""" 댓글(comemnt) 모델 모듈 파일입니다. """
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    """ comment 클래스입니다. """
    commented_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
    )
    commented_id = models.PositiveIntegerField(
        null=True,
    )
    commented_object = GenericForeignKey(
        'commented_type',
        'commented_id',
    )
    user = models.ForeignKey(
        "user.User",
        verbose_name="댓글을 단 사람",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    content = models.CharField(
        verbose_name="내용",
        max_length=200,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name="생성된 날짜",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 날짜",
        auto_now=True
    )
