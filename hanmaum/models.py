""" 한마음 게시글 모델 모듈 파일입니다."""
import html2text
from bs4 import BeautifulSoup
from markdown import markdown

from django.db import models
from django_summernote.fields import SummernoteTextField

from users.models import User
from configs.base_model import BaseModel, BaseModelManager


class HanmaumArticleQuerySet(models.QuerySet):
    """ 한마음 모델 쿼리셋 클래스입니다. """

    def published(self):
        """ published 상태인 게시글만 리턴합니다. """
        return self.filter(status='p').order_by("-updated_at")


class HanmaumArticle(BaseModel):
    """한마음 게시글 모델입니다."""
    class Meta:
        verbose_name = '한마음 게시글'
        verbose_name_plural = '한마음 게시글'

    objects = BaseModelManager.from_queryset(HanmaumArticleQuerySet)()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    author = models.ForeignKey(
        'users.user',
        verbose_name="글쓴이",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )  # 글쓴이
    title = models.CharField(
        verbose_name="제목",
        max_length=200,
    )
    content = SummernoteTextField(
        verbose_name="내용"
    )
    status = models.CharField(
        verbose_name='게시글 공개 상태',
        max_length=2,
        default='p',
        null=False,
        choices=STATUS_CHOICES
    )
    like_count = models.PositiveIntegerField(
        verbose_name="좋아요 수",
        default=0,
        null=True,
        blank=True
    )
    dislike_count = models.PositiveIntegerField(
        verbose_name="싫어요 수",
        default=0,
        null=True,
        blank=True
    )
    viewed_count = models.PositiveIntegerField(
        verbose_name="조회수",
        default=0,
        null=True,
        blank=True
    )
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

    def copy(self, status='d'):
        """ article 복사 메서드 """
        new_article = HanmaumArticle()
        new_article.author = self.author
        new_article.title = self.title
        new_article.content = self.content
        new_article.status = status
        new_article.save()
        return new_article
