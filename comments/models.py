""" 댓글(comemnt) 모델 모듈 파일입니다. """
import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from hanalum_web.base_model import BaseModel, BaseModelManager


class CommentQuerySet(models.QuerySet):
    """ Comment 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 댓글만 리턴합니다. """
        return self.filter(status='p')


class Comment(BaseModel):
    """ comment 클래스입니다. """
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'

    objects = BaseModelManager.from_queryset(CommentQuerySet)()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="댓글을 단 사람",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField(
        verbose_name="내용",
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name='댓글 상태',
        max_length=2,
        default='p',
        null=False,
        choices=STATUS_CHOICES
    )

    @property
    def is_updated(self):
        """수정된 댓글인지 여부를 리턴합니다."""
        return self.updated_at - self.created_at >= datetime.timedelta(seconds=1)

    def editable(self, current_user):
        """현재 유저가 해당 댓글을 수정할 수 있는지 여부를 리턴합니다."""
        return current_user.is_authenticated and current_user == self.user

    def destroyable(self, current_user):
        """현재 유저가 해당 댓글을 삭제할 수 있는지 여부를 리턴합니다."""
        return current_user.is_authenticated and (self.editable(current_user) or current_user.is_admin)

    def destroy(self):
        """현재 댓글을 삭제합니다."""
        self.status = 't'
        self.save()

    @classmethod
    def get_comments(cls, _commented_object):
        """특정 객체에 달린 댓글을 리턴합니다."""
        commented_type_obj = ContentType.objects.get_for_model(_commented_object)
        comments = Comment.objects.filter(
            commented_type=commented_type_obj,
            commented_id=_commented_object.id,
            parent=None,
        ).order_by('created_at')
        for comment in comments:
            comment.recomments = Comment.objects.filter(
                commented_type=commented_type_obj,
                parent=comment,
            ).order_by('created_at')
        return comments

    @classmethod
    def new_comment(self, _commented_object, _user, _content, _parent=None):
        """새로운 댓글을 추가합니다."""
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

    @classmethod
    def get_recent_user_comments(cls, _user):
        """특정 유저가 최근에 작성한 댓글을 리턴합니다."""
        comments = Comment.objects.published().filter(
            user=_user,
        ).order_by('-updated_at')

        for comment in comments:
            comment.show_url = "/{}/{}".format(comment.commented_type.app_label, comment.commented_id)
        
        return comments
