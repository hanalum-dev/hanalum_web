""" comment view 모듈 입니다. """
# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Comment

def destroy(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.destroy()

    messages.success(request, "댓글이 삭제되었습니다.")
    return redirect(request.META.get('HTTP_REFERER'))
