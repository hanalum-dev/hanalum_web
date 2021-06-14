""" 공지사항(notice) 모델 모듈 파일입니다. """
import html2text
from bs4 import BeautifulSoup
from django.db import models
from django_summernote.fields import SummernoteTextField
from markdown import markdown

from hanalum_web.base_model import BaseModel, BaseModelManager

class NoticeQuerySet(models.QuerySet):
    """ notice 모델 쿼리셋 클래스입니다. """

    def recent(self):
        """ 최근에 수정된 게시글을 먼저 리턴합니다. """
        return self.order_by("-updated_at")

    def published(self):
        """ published 상태인 게시글만 리턴합니다. """
        return self.filter(status='p')

    def top_fixed(self):
        """ top_fixed 상태인 게시글만 리턴합니다. """
        return self.filter(top_fixed=True).order_by('-priority', '-updated_at')

    def non_top_fixed(self):
        """ top_fixed 상태가 아닌 게시글만 리턴합니다. """
        return self.filter(top_fixed=False)

class Notice(BaseModel):
    """ 공지사항 모델 """
    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'

    objects = BaseModelManager.from_queryset(NoticeQuerySet)()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    title = models.CharField(
        verbose_name="제목",
        max_length=100,
        blank=True, null=True
    )
    content = SummernoteTextField(
        verbose_name="내용"
    )
    top_fixed = models.BooleanField(
        verbose_name="상단 고정 게시물",
        default=False,
        null=False
    )
    status = models.CharField(
        verbose_name='공지사항 공개 상태',
        max_length=2,
        default='d',
        null=False,
        choices=STATUS_CHOICES
    )
    priority = models.IntegerField(
        verbose_name="우선순위",
        default=0
    )
    viewed_count = models.PositiveIntegerField(
        verbose_name="조회수",
        default=0,
        null=True,
        blank=True
    )

    def __str__(self):
        return "[{}] {}".format(Notice.classname() ,self.title)

    def abstract_title(self, length=30):
        """ """
        if len(self.title) <= length:
            return str(self.title)
        else:
            return str(self.title)[:(length-3)] + "..."

    def summary(self, length=50):
        """ content 일부 표기"""

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        markdown_text = converter.handle(self.content)
        html = markdown(markdown_text)
        plain_text = ''.join(BeautifulSoup(html).findAll(text=True))

        if len(plain_text) >= length:
            return plain_text[:length] + "..."

        return plain_text[:length]

    def copy(self, status='d'):
        """ notice 복사 메서드 """
        new_notice = Notice()
        new_notice.title = self.title
        new_notice.content = self.content
        new_notice.status = status
        new_notice.save()
        return new_notice

    @classmethod
    def classname(cls):
        """ 클래스명 """
        return "공지사항"
