""" 한마음 게시글 폼 모둘입니다. """
from django import forms
from .models import HanmaumArticle
from django_summernote.widgets import SummernoteWidget


class HanmaumCreationForm(forms.ModelForm):
    """ 게시글 생성 폼 클래스 입니다. """

    class Meta:
        """HanmaumCreationForm meta 클래스"""
        model = HanmaumArticle
        fields = [
            "title",
            "content",
            "status",
            "interviewer",
            "interviewee",
            "thumbnail",
        ]
        widgets = {
            "content": SummernoteWidget(
                attrs={
                    'summernote': {
                        'width': '100%',
                        'height': '600px',
                    }
                }
            ),
            "title": forms.TextInput(
                attrs={
                    'class': 'article-title-form'
                }
            )
        }
        labels = {
            "title" : "제목",
            "status" : "상태",
            "interviewer": "인터뷰어",
            "interviewee": "인터뷰이",
            "content": "내용",
            "thumbnail": "썸네일",
        }
