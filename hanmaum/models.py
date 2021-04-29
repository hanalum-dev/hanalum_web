""" 한마음 게시글 모델 모듈 파일입니다."""
import html2text
from bs4 import BeautifulSoup
from markdown import markdown

from django.db import models
from django_summernote.fields import SummernoteTextField

from users.models import User
from hanalum_web.base_model import BaseModel, BaseModelManager

class HanmaumArticleQueryManager(BaseModelManager):
    """ 한마음 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시글만 리턴합니다. """
        return self.filter(status='p').order_by("-updated_at")


class HanmaumArticle(BaseModel):
    """한마음 게시글 모델입니다."""
    objects = HanmaumArticleQueryManager()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    title = models.CharField(
        verbose_name="인터뷰 제목",
        max_length=100,
        default=''
    )
    interviewer = models.CharField(
        verbose_name="인터뷰어",
        max_length=10,
        default=''
    )
    interviewee = models.CharField(
        verbose_name="인터뷰이",
        max_length=10,
        default=''
    )
    uploader = models.ForeignKey(
        "users.User",
        verbose_name="업로더",
        related_name='uploader',
        on_delete=models.DO_NOTHING,
        null=True,
        db_column="uploader_id"
    )
    content = SummernoteTextField(
        verbose_name="내용"
    )
    thumbnail = models.ImageField(
        verbose_name="대표 이미지",
        null=True,
        blank=True,
        upload_to="hanmaum/%Y/%m/%d"
    )
    status = models.CharField(
        verbose_name='게시글 공개 상태',
        max_length=2,
        default='d',
        null=False,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        """ 제목만 표기 """
        return "{}".format(self.title)

    def classname(self):
        """ 클래스명 """
        return self.__class__.__name__

    def summary(self, length=100):
        """ content 일부 표기"""

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        markdown_text = converter.handle(self.content)
        html = markdown(markdown_text)
        plain_text = ''.join(BeautifulSoup(html).findAll(text=True))

        if len(plain_text) >= length:
            return plain_text[:length] + "..."

        return plain_text[:length]
