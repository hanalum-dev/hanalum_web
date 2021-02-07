""" article 모델 파일입니다. """
import html2text
from bs4 import BeautifulSoup
from markdown import markdown

from django.db import models
from django_summernote.fields import SummernoteTextField


class ArticleQuerySet(models.QuerySet):
    """ article 모델 쿼리셋 클래스입니다. """

    def recent(self):
        """ 최신 게시글부터 담아서 리턴합니다. """
        return self.order_by("-created_at")


class Article(models.Model):
    """ 게시글 모델 """

    board = models.ForeignKey(
        'board.board',
        verbose_name="게시판",
        on_delete = models.DO_NOTHING,
        blank=True,
        null=True,
    )  # 게시판
    author = models.ForeignKey(
        'user.user',
        verbose_name="글쓴이",
        on_delete = models.DO_NOTHING,
        blank=True,
        null=True,
    ) # 글쓴이
    title = models.CharField(
        verbose_name="제목",
        max_length=200,
    )
    content = SummernoteTextField(
        verbose_name="내용"
    )
    created_at = models.DateTimeField(
        verbose_name="생성된 날짜",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 날짜",
        auto_now=True
    )

    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return "[{}]{}".format(self.board, self.title)

    def abstract_title(self):
        if len(self.title) <= 30:
            return str(self.title)
        else:
            return str(self.title)[:27] + "..."

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

    def classname(self):
        """ 클래스명 """
        return self.__class__.__name__


class ArticleAttachment(models.Model):
    """ 게시글 첨부파일 모델 """
    article = models.ForeignKey(
        'article.article',
        related_name='article',
        on_delete=models.DO_NOTHING
    )
    attachment = models.FileField(
        verbose_name="첨부파일",
        upload_to="files/%Y/%m/%d/"
    )

    # 첨부된 파일은 article이 지워지고 특정 기간이 지난 후에 삭제되게 하기.