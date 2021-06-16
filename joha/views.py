from joha.models import Paper, PaperAuthor, PaperVersion
from django.http import response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from copy import deepcopy as dp
from django.contrib import messages
from django.db import DataError, transaction

from helpers.default import default_response

def index(request):
    response = dp(default_response)
 
    return render(request, 'joha/index.dj.html', response)


class JohaReviewsView:
    @classmethod
    def index(cls, request):
        response = dp(default_response)

        return render(request, 'joha/reviews/index.dj.html', response)


    def show(request):
        response = dp(default_response)

        return render(request, 'joha/reviews/show.dj.html', response)


    @classmethod
    def new(request):
        response = dp(default_response)

        return render(request, 'joha/reviews/new.dj.html', response)


    @classmethod
    def edit(request):
        response = dp(default_response)

        return render(request, 'joha/reviews/edit.dj.html', response)


@transaction.atomic
@login_required(login_url='/users/signin')
def apply(request):
    response = dp(default_response)
    current_user = request.user

    if request.method == 'POST':
        paper_title = request.POST.get('paper-title')
        paper_subtitle = request.POST.get('paper-subtitle')
        paper_summary = request.POST.get('paper-summary')
        paper_file = request.FILES.get('paper-file')
        comment_to_reviewer = request.FILES.get('paper-comment')
        
        try:
            with transaction.atomic():
                new_paper = Paper()
                new_paper_author = PaperAuthor()
                new_paper_version = PaperVersion()

                new_paper.title = paper_title
                new_paper.subtitle = paper_subtitle
                new_paper.summary = paper_summary
                
                if not new_paper.title:
                    messages.error(request, '논문 제목을 입력해주세요.')
                    raise DataError
                if not paper_file:
                    messages.error(request, '논문 파일을 제출해주세요.')
                    raise DataError

                new_paper.save()
                new_paper_author.paper = new_paper
                new_paper_author.author = current_user 
                new_paper_author.save()
                new_paper_version.paper = new_paper
                new_paper_version.file = paper_file
                new_paper_version.comment_to_reviewer = comment_to_reviewer
                new_paper_version.save()
        except:
            return render(request, 'joha/reviews/apply.dj.html', response)
        messages.success(request, '논문 리뷰 신청을 완료하였습니다.')
        return redirect("joha:reviews_index")

    return render(request, 'joha/reviews/apply.dj.html', response)
