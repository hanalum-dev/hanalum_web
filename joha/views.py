from django.http import response
from django.shortcuts import render
from copy import deepcopy as dp

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


    @classmethod
    def apply(cls, request):
        response = dp(default_response)
        
        if request.method == 'POST':
            return
            
        return render(request, 'joha/reviews/apply.dj.html', response)
    
