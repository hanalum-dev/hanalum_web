""" 루트 페이지 관련 모듈 파일입니다. """
from django.db import models


class TopBanner(models.Model):
    """ 탑 배너 모델입니다. """
    content = models.TextField(verbose_name='내용', max_length=100)
    is_active = models.BooleanField(default=False, )
    created_at = models.DateTimeField(verbose_name='생성된 시각', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정된 시각', auto_now=True)
    # TODO: 탑 배너 배경 색상코드 선택하는 필드 추가
    # TODO: 탑 배너에 이미지 필드 추가

    objects = models.Manager()

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
