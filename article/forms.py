""" 한마음 게시글 폼 모둘입니다. """
from django_summernote.widgets import SummernoteWidget

from django import forms

from .models import Article


class ArticleCreationForm(forms.ModelForm):
    """ 게시글 생성 폼 클래스 입니다. """

    class Meta:
        """ArticleCreationForm meta 클래스"""
        model = Article
        fields = [
            "title",
            "content",
        ]
        widgets = {
            "content": SummernoteWidget(
                attrs={
                    'summernote': {
                        'width': '100%',
                        'height': '600px',
                    }
                }
            )
        }
        labels = {
            "title" : "제목",
            "content": "내용"
        }
