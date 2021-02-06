from django.db import models


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


class LikeActivity(Activity):
    """ 좋아요/싫어요 등의 액션 모델입니다."""
    # TODO: 이후 슬퍼요, 멋져요 등의 카테고리도 추가하기
    ACTIVITY_CATEGORY = (
        ('like', '좋아요'),
        ('dislike', '싫어요'),
    )

    category = models.CharField(verbose_name="카테고리", max_length=10, null=True, choices=ACTIVITY_CATEGORY)
