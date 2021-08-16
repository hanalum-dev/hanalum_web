""" notice(공지사항) view 모듈 파일입니다. """
from copy import deepcopy as dp

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from comments.models import Comment
from helpers.default import default_response
from history.models import ViewHistory
from configs.views import catch_all_exceptions

from .models import Notice


@catch_all_exceptions
def index(request):
    """ GET: index """
    response = dp(default_response)
    top_fixed_notices = Notice.objects.published().top_fixed().recent()
    non_top_fixed_notices = Notice.objects.published().non_top_fixed().recent()

    paginator = Paginator(non_top_fixed_notices, 5)
    page = request.GET.get('page')
    if page == "" or page is None:
        page = 1

    non_top_fixed_notices = paginator.get_page(page)
    start = max(int(page) - 5, 1)
    end = min(int(page) + 5, paginator.num_pages)

    response.update({
        'banner_title' : '공지사항',
        'top_fixed_notices' : top_fixed_notices,
        'non_top_fixed_notices' : non_top_fixed_notices,
        'range' : list(range(start, end + 1))
    })

    for notice in top_fixed_notices:
        notice.author = '한아름'
    for notice in non_top_fixed_notices:
        notice.author = '한아름'

    return render(request, 'notices/index.dj.html', response)


@catch_all_exceptions
def show(request, notice_id):
    """ GET: show """
    current_user = request.user
    response = dp(default_response)

    notice = Notice.objects.get(pk=notice_id)
    next_notice = get_next_notice(notice_id)
    prev_notice = get_prev_notice(notice_id)

    comments = Comment.get_comments(notice)

    response.update({
        'banner_title' : "[공지사항] " + notice.title,
        'notice' : notice,
        'comments' : comments,
        'prev_notice': prev_notice,
        'next_notice': next_notice
    })

    # 사용자 접속 로그 추가
    if current_user.is_authenticated:
        ViewHistory.add_history(
            _viewed_obj=notice,
            _viewer=current_user
        )

    return render(request, 'notices/show.dj.html', response)


@catch_all_exceptions
@login_required(login_url='/users/signin')
def new_comment(request, notice_id):
    """ GET: new_comment
        댓글을 추가합니다.
    """

    notice = Notice.objects.get(pk=notice_id)
    user = request.user
    content = request.POST.get('content')

    parent_id = request.POST.get('parent_id')
    if parent_id:
        parent = Comment.objects.get(pk=parent_id)
    else:
        parent = None

    Comment.new_comment(
        _commented_object=notice,
        _user=user,
        _content=content,
        _parent=parent
    )

    # TODO: 댓글이 작성되었습니다. 메세지 띄우기
    return redirect("notices:show", notice_id)


def get_next_notice(notice_id):
    """다음 공지를 반환합니다."""
    return Notice.objects.filter(pk__gt=notice_id).first()


def get_prev_notice(notice_id):
    """이전 공지를 반환합니다."""
    return Notice.objects.filter(pk__lt=notice_id).first()
