""" notice(공지사항) view 모듈 파일입니다. """
from copy import deepcopy as dp

from django.shortcuts import render, redirect, get_object_or_404
from helpers.default import default_response

from .models import Notice
from comment.models import Comment

comment_model = Comment()

def index(request):
    response = dp(default_response)
    response.update({
        'banner_title' : '공지사항',
        'top_fixed_notices' : Notice.objects.published().top_fixed().recent(),
        'non_top_fixed_notices' : Notice.objects.published().non_top_fixed().recent(),
    })

    # TODO: HNM-0097: 공지사항 페이지네이션 추가


    return render(request, 'notice/index.dj.html', response)


def show(request, notice_id):
    response = dp(default_response)

    notice = get_object_or_404(Notice, pk=notice_id)

    comments = Comment().get_comments(notice)

    response.update({
        'banner_title' : "[공지사항] " + notice.title,
        'notice' : notice,
        'comments' : comments,
    })

    return render(request, 'notice/show.dj.html', response)

def new_comment(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    user = request.user
    content = request.POST.get('content')

    comment_model.new_comment(
        _commented_object = notice,
        _user = user,
        _content = content,
    )

    return redirect("notice:show", notice_id)