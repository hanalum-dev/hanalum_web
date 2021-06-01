""" 한마음 게시글 모델 모듈 파일입니다."""
import html2text
from bs4 import BeautifulSoup
from markdown import markdown

from django.db import models
from django_summernote.fields import SummernoteTextField

from users.models import User
from articles.models import Article
from hanalum_web.base_model import BaseModel, BaseModelManager

class HanmaumArticleQuerySet(models.QuerySet):
    """ 한마음 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시글만 리턴합니다. """
        return self.filter(status='p').order_by("-updated_at")


class HanmaumArticle(Article, BaseModel):
    """한마음 게시글 모델입니다."""
    objects = BaseModelManager.from_queryset(HanmaumArticleQuerySet)()

    interviewer = models.CharField(
        verbose_name="인터뷰어",
        max_length=10,
        default='',
        null=True,
    )
    interviewee = models.CharField(
        verbose_name="인터뷰이",
        max_length=10,
        default='',
        null=True,
    )
    thumbnail = models.ImageField(
        verbose_name="대표 이미지",
        default='',
        null=True,
        blank=True,
        upload_to="hanmaum/%Y/%m/%d"
    )

    def __str__(self):
        """ classname과 제목 표기 """
        return "[{}] {}".format(HanmaumArticle.classname(), self.title)

    @classmethod
    def classname(cls):
        """ 클래스명 """
        return "한마음"

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
