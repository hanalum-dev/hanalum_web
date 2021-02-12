""" 공지사항(notice) 모델 모듈 파일입니다. """
import html2text
from bs4 import BeautifulSoup
from django.db import models
from django_summernote.fields import SummernoteTextField
from markdown import markdown


class Notice(models.Model):
    """ 공지사항 모델 """

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
    created_at = models.DateTimeField(
        verbose_name="생성된 날짜",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 날짜",
        auto_now=True
    )

    def __str__(self):
        return "{}".format(self.title)

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

    def classname(self):
        """ 클래스명 """
        return self.__class__.__name__
