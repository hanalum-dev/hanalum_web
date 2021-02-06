""" 한마음 게시글 폼 모둘입니다. """
from django import forms

from .models import HanmaumArticle


class HanmaumCreationForm(forms.ModelForm):
    """ 한마음 게시글 생성 폼입니다. """
    class Meta:
        """HanmaumCreationForm meta 클래스"""
        model = HanmaumArticle
        fields = [
            "title",
            "interviewer",
            "interviewee",
            "content",
        ]
        widgets = {

        }
        labels = {
            "title" : "제목",
            "interviewer": "인터뷰어",
            "interviewee": "인터뷰이",
            "content": "내용"
        }
