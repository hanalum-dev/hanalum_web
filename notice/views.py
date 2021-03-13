""" notice(공지사항) view 모듈 파일입니다. """
from copy import deepcopy as dp

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from .models import Notice
from helpers.default import default_response
from comment.models import Comment
from history.models import ViewHistory
from django.core.paginator import Paginator

view_history = ViewHistory()
comment_model = Comment()

def index(request):
    response = dp(default_response)
    top_fixed_notices = Notice.objects.published().top_fixed().recent()
    non_top_fixed_notices = Notice.objects.published().non_top_fixed().recent()

    paginator = Paginator(non_top_fixed_notices, 5)
    page= request.GET.get('page')
    if page == "" or page == None:
        page = 1

    non_top_fixed_notices = paginator.get_page(page)
    start = max(int(page)-5, 1)
    end = min(int(page)+5, paginator.num_pages)

    response.update({
        'banner_title' : '공지사항',
        'top_fixed_notices' : top_fixed_notices,
        'non_top_fixed_notices' : non_top_fixed_notices,
        'range' : [i for i in range(start, end+1)]
    })

    for notice in top_fixed_notices:
        notice.author='한아름'
        notice.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=notice,
        ) or 0
    for notice in non_top_fixed_notices:
        notice.author='한아름'
        notice.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=notice,
        ) or 0

    return render(request, 'notice/index.dj.html', response)


def show(request, notice_id):
    current_user = request.user
    response = dp(default_response)

    notice = get_object_or_404(Notice, pk=notice_id)

    comments = Comment().get_comments(notice)

    response.update({
        'banner_title' : "[공지사항] " + notice.title,
        'notice' : notice,
        'comments' : comments,
    })

    # 사용자 접속 로그 추가
    if current_user.is_authenticated:
        view_history.add_history(
            _viewed_obj=notice,
            _viewer=current_user
        )

    return render(request, 'notice/show.dj.html', response)

@login_required(login_url='/user/signin')
def new_comment(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    user = request.user
    content = request.POST.get('content')

    parent_id = request.POST.get('parent_id')
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    else:
        parent = None

    comment_model.new_comment(
        _commented_object = notice,
        _user = user,
        _content = content,
        _parent=parent
    )

    # TODO: 댓글이 작성되었습니다. 메세지 띄우기
    return redirect("notice:show", notice_id)
