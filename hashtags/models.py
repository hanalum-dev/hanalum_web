""" 해쉬태그 모델 모듈 파일입니다. """
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from hanalum_web.base_model import BaseModel, BaseModelManager


class HashTag(BaseModel):
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

    def add_hashtag(self, tagged_object, content):
        tagged_type_object = ContentType.objects.get_for_model(tagged_object)

        hashtag = HashTag(
            tagged_type=tagged_type_object,
            tagged_id=tagged_object.id,
            content=content
        )
        hashtag.save()

    def get_hashtag(self, tagged_object):
        content_type_obj = ContentType.objects.get_for_model(tagged_object)
        response = HashTag.objects.filter(
            tagged_type=content_type_obj,
            tagged_id=tagged_object.id,
        ).order_by('updated_at')
        return response

    def destroy_all_hashtag(self, tagged_object):
        content_type_obj = ContentType.objects.get_for_model(tagged_object)

        HashTag.objects.filter(
            tagged_type=content_type_obj,
            tagged_id=tagged_object.id,
        ).all().delete()
