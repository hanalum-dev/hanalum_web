from users.models import User
from django.shortcuts import get_object_or_404, render

def preview_user_activation(request):
    response = {
        'domain': 'alpha.hanalum.kr',
        'user': get_object_or_404(User, pk=1),
        'uid': 1,
        'token': 1,
    }

    return render(request, 'mails/activation.dj.html', response)