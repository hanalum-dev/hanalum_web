""" 댓글(comemnt) 모델 모듈 파일입니다. """
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    """ comment 클래스입니다. """
    objects = models.Manager()

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

    parent = models.ForeignKey(
        "self",
        verbose_name="답글을 단 댓글",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="replies",
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

    def editable(self, current_user):
        return current_user == self.user

    def destroyable(self, current_user):
        return self.editable(current_user) or current_user.is_admin

    def get_comments(self, _commented_object):
        commented_type_obj = ContentType.objects.get_for_model(_commented_object)
        comments = Comment.objects.filter(
            commented_type=commented_type_obj,
            commented_id=_commented_object.id,
            parent=None,
        ).order_by('updated_at')
        for comment in comments:
            comment.recomments = Comment.objects.filter(
                commented_type=commented_type_obj,
                parent=comment,
            ).order_by('updated_at')
        return comments

    def new_comment(self, _commented_object, _user, _content, _parent=None):
        # TODO: transaction 적용하고, logger 적용하기
        # TODO: validation 추가하기 (user나 content가 비어있으면 안된다. commented_object가 댓글을 달 수 있는 상태인지 등)
        commented_type_obj = ContentType.objects.get_for_model(_commented_object)
        comment = Comment()
        comment.commented_type = commented_type_obj
        comment.commented_id = _commented_object.id
        comment.user = _user
        comment.content = _content
        comment.parent = _parent
        comment.save()
