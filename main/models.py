""" 루트 페이지 관련 모듈 파일입니다. """
from django.core.exceptions import ValidationError
from django.db import models

from boards.models import Board

from configs.base_model import BaseModel, BaseModelManager


class TopBanner(BaseModel):
    """ 탑 배너 모델입니다. """
    class Meta:
        verbose_name = '탑배너'
        verbose_name_plural = '탑배너'

    content = models.TextField(
        verbose_name='내용',
        max_length=100
    )
    is_active = models.BooleanField(
        default=False
    )
    # TODO: HNM-0061 탑 배너 배경 색상코드 선택하는 필드 추가
    # TODO: 탑 배너에 이미지 필드 추가

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        """ 탑 배너는 1개만 허용하는 메서드입니다. """
        if self.is_active:
            try:
                current_banner = TopBanner.objects.get(is_active=True)
                if self != current_banner:
                    current_banner.is_active = False
                    current_banner.save()
            except TopBanner.DoesNotExist:  # pylint: disable=no-member
                pass
        super().save(*args, **kwargs)


class MainBoardQuerySet(models.QuerySet):
    """ MainBoard 모델 쿼리셋 클래스입니다. """

    def priority_order(self):
        # FIXME: 가나다 순이 제대로 안 작동함.
        """ 우선순위 높은 순서에 따라 정렬하고, 우선순위가 같다면 게시판 제목의 가나다 순으로 정렬합니다. """
        return self.order_by('-priority', 'board__title')


class MainBoard(BaseModel):
    """ 메인화면에 보이는 게시판을 지정하는 모델입니다. """
    class Meta:
        verbose_name = '메인화면 게시판'
        verbose_name_plural = '메인화면 게시판'

    objects = BaseModelManager.from_queryset(MainBoardQuerySet)()

    board = models.ForeignKey(Board,
                              related_name="main_board",
                              on_delete=models.CASCADE,
                              verbose_name="게시판"
                              )
    priority = models.IntegerField(
        verbose_name="우선순위",
        default=0
    )

    def clean(self):
        """ published 되어있는 게시판만 메인 보드로 허용하는 메서드입니다. """
        if self.board.status != 'p':  # pylint: disable=no-member
            raise ValidationError("published 상태가 아닌 게시판은 메인 화면 보드로 지정할 수 없습니다.")
