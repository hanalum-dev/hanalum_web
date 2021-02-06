from django.db import models


from helpers.activity_errors import (
    AlreadyLikeArticle, AlreadyDisLikeArticle, AlreadyNoneActivityArticle
)
from helpers.activity_sucesses import(
    LikeSuccess, DisLikeSuccess, LikeCancleSuccess, DisLikeCancleSuccess
)

class ViewHistory(models.Model):
    """ 사용자 모델 뷰 로그 모델입니다. """
    viewed_model = models.CharField(verbose_name="모델명", max_length=100, null=False, blank=False, default="")
    viewed_id = models.IntegerField(verbose_name="객체 id", null=True, blank=True)
    viewer = models.ForeignKey("user.User", verbose_name="유저",  on_delete=models.DO_NOTHING, null=True, blank=True)
    viewed_count = models.IntegerField(verbose_name="유저별 조회수", null=False, default=0)
    created_at = models.DateTimeField(verbose_name="생성된 날짜", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정된 날짜", auto_now=True)

    objects = models.Manager()

    def viewed_at(self):
        """ created_at 과 viewed_at을 동일시하기 위한 메서드"""
        return self.created_at

    def total_viewed_count(self, _viewed_model, _viewed_id):
        """ 특정 아이템의 사용자별 뷰 카운트를 모두 합쳐 리턴하는 메서드입니다. """
        total_count = 0
        history_group = ViewHistory.objects.filter(viewed_model=_viewed_model, viewed_id=_viewed_id)
        for history in history_group:
            total_count += history.viewed_count
        return total_count        

    def distinct_total_viewed_count(self, _viewed_model, _viewed_id):
        """ 특정 아이템을 본 사용자 카운트를 리턴하는 메서드입니다. """
        return ViewHistory.objects.filter(viewed_model=_viewed_model, viewed_id=_viewed_id).count()

    def add_history(self, _viewed_model, _viewed_id, _viewer):
        """ 사용자 로그 접속 로그 추가 메서드 """
        try:
            prev_history = ViewHistory.objects.get(viewed_model=_viewed_model, viewed_id=_viewed_id, viewer=_viewer)
            prev_history.viewed_count +=1
            prev_history.save()
        except ViewHistory.DoesNotExist:  # pylint: disable=no-member
            new_history = ViewHistory()
            new_history.viewed_model = _viewed_model
            new_history.viewed_id = _viewed_id
            new_history.viewer = _viewer
            new_history.viewed_count = 1
            new_history.save()


class Activity(models.Model):
    """ 사용자 액티비티 관련 베이스 모델입니다. """
    activity_model = models.CharField(verbose_name="모델명", max_length=100, null=False, blank=False, default="")
    activity_id = models.IntegerField(verbose_name="객체 id", null=True, blank=True)
    user = models.ForeignKey("user.User", verbose_name="유저",  on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="생성된 날짜", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정된 날짜", auto_now=True)

    objects = models.Manager()


class LikeActivity(Activity):
    """ 좋아요/싫어요 등의 액션 모델입니다."""
    # TODO: 이후 슬퍼요, 멋져요 등의 카테고리도 추가하기
    ACTIVITY_CATEGORY = (
        ('like', '좋아요'),
        ('dislike', '싫어요'),
        ('none', '상태없음')
    )

    category = models.CharField(verbose_name="카테고리", max_length=10, null=True, choices=ACTIVITY_CATEGORY)

    def is_user_in_activity(self, _activity_model, _activity_id, _user, _category):
        """ 사용자가 특정 액티비티를 수행하였는지 확인하는 메서드"""
        try:
            activity = LikeActivity.objects.get(activity_model=_activity_model, activity_id=_activity_id, user=_user, category=_category)
            if activity:
                return True
        except LikeActivity.DoesNotExist:  # pylint: disable=no-member
            return False
        return False

    def is_user_in_like(self, _activity_model, _activity_id, _user):
        """ 사용자가 좋아요가 되어있는지 확인하는 메서드"""
        return self.is_user_in_activity(_activity_model, _activity_id, _user, 'like')
    
    def is_user_in_dislike(self, _activity_model, _activity_id, _user):
        """ 사용자가 싫어요가 되어있는지 확인하는 메서드"""
        return self.is_user_in_activity(_activity_model, _activity_id, _user, 'dislike')
    
    def set_user_in_category(self, _activity_model, _activity_id, _user, _category):
        """ 액티비티를 세팅하는 base 메서드 """
        response = {
            'prev_category': None,
            'crt_category': _category
        }
        try:
            activity = LikeActivity.objects.get(activity_model=_activity_model, activity_id=_activity_id, user=_user)
            response['prev_category'] = activity.category
            activity.category = _category

        except LikeActivity.DoesNotExist:  # pylint: disable=no-member
            activity = LikeActivity()
            activity.activity_model = _activity_model
            activity.activity_id = _activity_id
            activity.user = _user
            activity.category = _category
        activity.save()

        return response

    def set_user_in_like(self, _activity_model, _activity_id, _user):
        """ set 사용자 좋아요 액티비티 """
        response = self.set_user_in_category(_activity_model, _activity_id, _user, 'like')
        
        prev_category = response['prev_category'] # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category'] # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyLikeArticle()
        
        return LikeSuccess()
        
    def set_user_in_dislike(self, _activity_model, _activity_id, _user):
        """ set 사용자 싫어요 액티비티 """
        response = self.set_user_in_category(_activity_model, _activity_id, _user, 'dislike')
        
        prev_category = response['prev_category'] # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category'] # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyDisLikeArticle()
        
        return DisLikeSuccess()

        
    def set_user_in_none(self, _activity_model, _activity_id, _user):
        """ set 사용자 싫어요 액티비티 """
        response = self.set_user_in_category(_activity_model, _activity_id, _user, 'none')
        
        prev_category = response['prev_category'] # 이전 액티비티 상태, 설정한 적 없으면 None
        crt_category = response['crt_category'] # 현재 설정된 액티비티 상태

        if prev_category == crt_category:
            return AlreadyNoneActivityArticle()
        
        if prev_category == 'like':
            return LikeCancleSuccess()

        if prev_category == 'dislike':
            return DisLikeCancleSuccess()
        
        return AlreadyNoneActivityArticle()
