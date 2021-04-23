""" comments view 모듈 입니다. """
# from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Comment

def update(request, comment_id):
    new_content = request.POST.get('content')

    comment = get_object_or_404(Comment, pk=comment_id)
    if new_content:
        comment.content = new_content
        comment.save()
        messages.success(request, "댓글이 수정되었습니다.")
    else:
        messages.error(request, "댓글 내용을 입력해주세요.")

    return redirect(request.META.get('HTTP_REFERER'))


def destroy(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.destroy()

    messages.success(request, "댓글이 삭제되었습니다.")
    return redirect(request.META.get('HTTP_REFERER'))
