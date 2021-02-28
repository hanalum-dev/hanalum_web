""" 해쉬태그 모델 모듈 파일입니다. """
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class HashTag(models.Model):
    """ 해쉬태그 모델 클래스입니다. """
    tagged_type = models.ForeignKey(
        ContentType,
        verbose_name="모델명",
        on_delete=models.CASCADE,
        null=True,
    )
    tagged_id = models.PositiveIntegerField(
        null=True,
    )
    tagged_object = GenericForeignKey(
        'tagged_type',
        'tagged_id',
    )
    content = models.CharField(
        verbose_name="해쉬태그명",
        max_length=50,
        null=False,
        default=""
    )
    created_at = models.DateTimeField(
        verbose_name="생성된 날짜",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 날짜",
        auto_now=True
    )

    def add_hashtag(self, tagged_object, content):
        tagged_type_object = ContentType.objects.get_for_model(tagged_object)

        hashtag = HashTag(
            tagged_type=tagged_type_object,
            tagged_id=tagged_object.id,
            content=content
        )
        hashtag.save()
