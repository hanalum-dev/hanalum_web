from django.shortcuts import render

def personal_information(request):
    return render(request, 'policies/personal_information.html')