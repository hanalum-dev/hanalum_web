""" articles 모델 파일입니다. """
import html2text
from bs4 import BeautifulSoup
from markdown import markdown

from django.core.exceptions import ValidationError
from django.db import models
from django_summernote.fields import SummernoteTextField


class ArticleQuerySet(models.QuerySet):
    """ articles 모델 쿼리셋 클래스입니다. """

    def recent(self):
        """ 최신 게시글부터 담아서 리턴합니다. """
        return self.order_by("-created_at")

    def published(self):
        """ published 상태인 게시글만 리턴합니다. """
        return self.filter(status='p')

    def top_fixed(self):
        """ 상단 고정 게시글만 리턴합니다. """
        return self.filter(top_fixed=True)

    def non_top_fixed(self):
        """ 상단 고정이 아닌 게시글만 리턴합니다. """
        return self.filter(top_fixed=False)

    def five(self):
        """ 5개의 게시글만 리턴합니다. """
        return self[:5]

class Article(models.Model):
    """ 게시글 모델 """
    objects = ArticleQuerySet.as_manager()

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('t', 'trash')
    )

    board = models.ForeignKey(
        'boards.board',
        verbose_name="게시판",
        on_delete = models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='articles'
    )  # 게시판
    author = models.ForeignKey(
        'users.user',
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
    anonymous_author = models.BooleanField(
        verbose_name='익명 여부',
        default=False,
        null=False
    )
    status = models.CharField(
        verbose_name='게시글 공개 상태',
        max_length=2,
        default='p',
        null=False,
        choices=STATUS_CHOICES
    )
    top_fixed = models.BooleanField(
        verbose_name="상단 고정 게시물",
        default=False,
        null=False
    )
    created_at = models.DateTimeField(
        verbose_name="생성된 날짜",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 날짜",
        auto_now=True
    )

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

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        """ articles record는 아래 조건이 성립해야 합니다. """
        # board가 익명 사용가능할 때, 익명 저자가 허용된다.
        if self.anonymous_author and not self.board.use_anonymous:
            raise ValidationError("해당 board는 익명 저자 기능을 사용할 수 없습니다.")
        super().save(*args, **kwargs)

class ArticleAttachment(models.Model):
    """ 게시글 첨부파일 모델 """
    article = models.ForeignKey(
        'articles.article',
        related_name='articles',
        on_delete=models.DO_NOTHING
    )
    attachment = models.FileField(
        verbose_name="첨부파일",
        upload_to="files/%Y/%m/%d/"
    )

    # TODO: 첨부된 파일은 article이 지워지고 특정 기간이 지난 후에 삭제되게 하기.
