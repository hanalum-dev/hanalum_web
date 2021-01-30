"""user(사용자 계정) views 모듈입니다."""
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render

from .forms import UserCreationForm
from .models import User
from .validators import UserCreationValidator


def signup(request):
    """회원가입 뷰"""
    response = {
        'status' : True,
        'msg' : '',
        'form' : None,
    }

    # TODO: error message 다중 적용 필요
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        _email = request.POST.get('email')
        _nickname = request.POST.get('nickname')
        _realname = request.POST.get('realname')
        _password1 = request.POST.get('password1')
        _password2 = request.POST.get('password2')

        validate_user_form_result = UserCreationValidator().validate(
            _email=_email, _nickname=_nickname, _realname=_realname, _password1=_password1, _password2=_password2,
        )

        if not validate_user_form_result.status:
            response['status'] = validate_user_form_result.status
            response['msg'] = validate_user_form_result.msg
            response['form'] = form
            return render(request, 'user/registrations/new.html', response)

        if form.is_valid():
            current_site = get_current_site(request)
            form.f_save(current_site, request.POST['email'])
            # TODO: message framework 사용해서, 이메일 확인하라는 메세지 추가하기
            redirect('user:signin')
        else:
            # TODO: 이것도 따로 helper errors 클래스 분리하기
            response['status'] = False
            response['msg'] = '입력이 제대로 되지 않았습니다.'
            return render(request, 'user/registrations/new.html', response)

        return redirect('user:signup')
    else:
        form = UserCreationForm()
        return render(request, 'user/registrations/new.html', {'form': form})


def signin(request):
    """로그인 뷰"""
    return


def signout(request):
    """로그아웃 뷰"""
    return


def show(request):
    """사용자 페이지 뷰"""
    response = {
    }
    user_id = request.GET.get('user_id')

    user = User.objects.get(user_id=user_id)

    response['user'] = user

    return render(request, 'user/show.html', response)


def edit(request):
    """ 사용자 정보 수정 페이지 뷰"""
    return


def update(request):
    """ 사용자 정보 수정 반영 뷰"""
    return


def delete(request):
    """사용자 회원 탈퇴 반영 뷰"""
