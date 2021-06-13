from django.shortcuts import render
from copy import deepcopy as dp

from helpers.default import default_response

def index(request):
    response = dp(default_response)
 
    return render(request, 'joha/index.dj.html', response)