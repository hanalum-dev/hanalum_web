"""
    Models: ViewHistory, Activity, LikeActivity
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from hanalum_web.base_model import BaseModel
from helpers.activity_errors import (AlreadyDisLikeArticle, AlreadyLikeArticle,
                                     AlreadyNoneActivityArticle)
from helpers.activity_sucesses import (DisLikeCancleSuccess, DisLikeSuccess,
                                       LikeCancleSuccess, LikeSuccess)


class ViewHistory(BaseModel):
    """ 사용자 모델 뷰 로그 모델입니다. """
    viewed_type = models.ForeignKey(
        ContentType,
        verbose_name="모델명",
        on_delete=models.CASCADE,
        null=True,
    )
    viewed_id = models.PositiveIntegerField(
        null=True,
    )
    viewed_object = GenericForeignKey(
        'viewed_type',
        'viewed_id',
    )
    viewer = models.ForeignKey(
        "users.User",
        verbose_name="유저",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    viewed_count = models.IntegerField(
        verbose_name="유저별 조회수",
        null=False,
        default=0
    )

    def viewed_at(self):
        """ created_at 과 viewed_at을 동일시하기 위한 메서드"""
        return self.created_at

    @classmethod
    def total_viewed_count(cls, _viewed_obj):
        """ 특정 아이템의 사용자별 뷰 카운트를 모두 합쳐 리턴하는 메서드입니다. """
        viewed_type_obj = ContentType.objects.get_for_model(_viewed_obj)
        history_group = ViewHistory.objects.filter(
            viewed_type=viewed_type_obj,
            viewed_id=_viewed_obj.id,
        )
        total_count = 0
        for history in history_group:
            total_count += history.viewed_count
        return total_count

    @classmethod
    def distinct_total_viewed_count(cls, _viewed_obj):
        """ 특정 아이템을 본 사용자 카운트를 리턴하는 메서드입니다. """
        viewed_type_obj = ContentType.objects.get_for_model(_viewed_obj)
        return ViewHistory.objects.filter(
            viewed_type=viewed_type_obj,
            viewed_id=_viewed_obj.id,
        ).count()

    @classmethod
    def add_history(self, _viewed_obj, _viewer):
        """ 사용자 로그 접속 로그 추가 메서드 """
        viewed_type_obj = ContentType.objects.get_for_model(_viewed_obj)
        try:
            prev_history = ViewHistory.objects.get(
                viewed_type=viewed_type_obj,
                viewed_id=_viewed_obj.id,
                viewer=_viewer
            )
            prev_history.viewed_count += 1
            prev_history.save()
        except ViewHistory.DoesNotExist:  # pylint: disable=no-member
            new_history = ViewHistory(
                viewed_type=viewed_type_obj,
                viewed_id=_viewed_obj.id,
            )
            new_history.viewer = _viewer
            new_history.viewed_count = 1
            new_history.save()


class Activity(BaseModel):
    """ 사용자 액티비티 관련 베이스 모델입니다. """
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="모델명",
        on_delete=models.CASCADE,
        null=True,
    )
    content_id = models.PositiveIntegerField(
        null=True,
    )
    content_object = GenericForeignKey(
        'content_type',
        'content_id',
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="유저",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )


class LikeActivity(Activity):
    """ 좋아요/싫어요 등의 액션 모델입니다."""
    # TODO: 이후 슬퍼요, 멋져요 등의 카테고리도 추가하기
    ACTIVITY_CATEGORY = (
        ('like', '좋아요'),
        ('dislike', '싫어요'),
        ('none', '상태없음')
    )

    category = models.CharField(
        verbose_name="카테고리",
        max_length=10,
        null=True,
        choices=ACTIVITY_CATEGORY
    )

    @classmethod
    def is_user_in_activity(cls, _content_object, _user, _category):
        """ 사용자가 특정 액티비티를 수행하였는지 확인하는 메서드"""
        content_type_obj = ContentType.objects.get_for_model(_content_object)
        activity = LikeActivity.objects.filter(
            content_type=content_type_obj,
            content_id=_content_object.id,
            user=_user,
            category=_category
        ).first()
        if activity:
            return True
        return False

    @classmethod
    def is_user_in_like(cls, _content_object, _user):
        """ 사용자가 좋아요가 되어있는지 확인하는 메서드"""
        return cls.is_user_in_activity(
            _content_object,
            _user,
            'like'
        )

    @classmethod
    def is_user_in_dislike(cls, _content_object, _user):
        """ 사용자가 싫어요가 되어있는지 확인하는 메서드"""
        return cls.is_user_in_activity(
            _content_object,
            _user,
            'dislike'
        )

    @classmethod
    def set_user_in_category(cls, _content_object, _user, _category):
        """ 액티비티를 세팅하는 base 메서드 """
        content_type_obj = ContentType.objects.get_for_model(_content_object)
        response = {
            'prev_category': None,
            'crt_category': _category
        }
        activity = LikeActivity.objects.filter(
            content_type=content_type_obj,
            content_id=_content_object.id,
            user=_user
        ).first()

        if activity is None:
            activity = LikeActivity(
                content_type=content_type_obj,
                content_id=_content_object.id,
                user=_user,
                category=_category
            )
        else:
            response['prev_category'] = activity.category
            activity.category = _category

        activity.save()

        return response

    @classmethod
    def set_user_in_like(cls, _content_object, _user):
        """ set 사용자 좋아요 액티비티 """
        response = cls.set_user_in_category(_content_object, _user, 'like')

        prev_category = response['prev_category']  # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category']  # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyLikeArticle()

        return LikeSuccess()

    @classmethod
    def set_user_in_dislike(cls, _content_object, _user):
        """ set 사용자 싫어요 액티비티 """
        response = cls.set_user_in_category(_content_object, _user, 'dislike')

        prev_category = response['prev_category']  # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category']  # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyDisLikeArticle()

        return DisLikeSuccess()

    @classmethod
    def set_user_in_none(cls, _content_object, _user):
        """ set 사용자 싫어요 액티비티 """
        response = cls.set_user_in_category(_content_object, _user, 'none')

        prev_category = response['prev_category']  # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category']  # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyNoneActivityArticle()

        if prev_category == 'like':
            return LikeCancleSuccess()

        if prev_category == 'dislike':
            return DisLikeCancleSuccess()

        return AlreadyNoneActivityArticle()

    @classmethod
    def get_like_count(cls, _content_object):
        """좋아요 수를 반환합니다."""
        content_type_obj = ContentType.objects.get_for_model(_content_object)
        response = LikeActivity.objects.filter(
            content_type=content_type_obj,
            content_id=_content_object.id,
            category='like'
        ).count()

        return response

    @classmethod
    def get_dislike_count(cls, _content_object):
        """싫어요 수를 반환합니다."""

        content_type_obj = ContentType.objects.get_for_model(_content_object)
        response = LikeActivity.objects.filter(
            content_type=content_type_obj,
            content_id=_content_object.id,
            category='dislike'
        ).count()

        return response

    @classmethod
    def get_like_content_objects(cls, _user, _content_object):
        """_user가 좋아요한 _content_object 종류의 객체들을 반환합니다."""

        content_type_obj = ContentType.objects.get_for_model(_content_object)
        like_activities = LikeActivity.objects.filter(
            user=_user,
            content_type=content_type_obj,
            category='like'
        ).order_by('-updated_at')

        like_objects = []
        for like_activity in like_activities:
            try:
                like_objects.append(
                    content_type_obj.get_object_for_this_type(pk=like_activity.content_id)
                )
            except:
                pass

        return like_objects
