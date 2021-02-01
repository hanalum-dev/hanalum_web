"""user(사용자 계정) views 모듈입니다."""
from django.contrib import auth, messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from .forms import UserConfirmationForm, UserCreationForm
from .models import User
from .tokens import account_activation_token
from .validators import UserCreationValidator


@transaction.atomic
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
            # TODO: 더 간결하게 적기
            response['status'] = validate_user_form_result.status
            response['msg'] = validate_user_form_result.msg
            response['form'] = form
            messages.error(request, '정보 입력이 제대로 되지 않았습니다.')
            return render(request, 'user/registrations/new.html', response)

        try:
            with transaction.atomic():
                if form.is_valid():
                    current_site = get_current_site(request)
                    form.f_save(current_site, request.POST['email'])
                    messages.success(request, '회원가입이 완료되었습니다. 이메일을 확인해주세요.')
                    redirect('user:signin')
        except IntegrityError as e:
            print(e)
        except Exception as e:  # pylint: disable=broad-except
            print(e)
        # TODO: 라벨링 다시 하기
        messages.error(request, '정보 입력이 제대로 되지 않았습니다.')
        return redirect('user:signup')
    else:
        form = UserCreationForm()
        return render(request, 'user/registrations/new.html', {'form': form})


def signin(request):
    """로그인 뷰"""
    response = {
    }

    if request.method == 'POST':
        form = response['form'] = UserConfirmationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=email, password=password)

            if user is None:
                # TODO: 메세지 프레임워크: 오류가 발생하였습니다.
                return render(request, 'use/confirmations/new.html', response)
            else:
                auth.login(request, user)
                # TODO: 메세지 프레임워크: 로그인되었습니다.
                return redirect('')
        else:
            # TODO: 메세지 프레임워크: 오류가 발생하였습니다.
            return render(request, 'use/confirmations/new.html', response)

    else:
        if request.user.is_authenticated:
            # TODO: 메세지 프레임워크: 이미 로그인되어있습니다.
            return redirect('')
        response['form'] = UserConfirmationForm()
        return render(request, 'user/confirmations/new.html', response)


def signout(request):
    """로그아웃 뷰"""
    auth.logout(request)
    # TODO: 메세지 프레임워크 활용: 로그아웃되었습니다
    return redirect('/')


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


def activate_account(request, uidb64, token):
    """사용자 인증 메일 활성화 뷰"""
    # TODO: transaction 적용하기
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        # TODO: 메세지 프레임워크 적용하기
        # 이메일 인증이 되었습니다.
        return redirect("user:signin")
    else:
        # TODO: 여기도 아래 메세지로, 메세지 프레임워크 적용하고 또다른 에러 화면으로 연결시키기
        # 인증링크가 올바르지 않거나, 인증 기간이 만료되었습니다.
        # 계속해서 오류가 발생한다면, 한아름에 건의해주세요.
        return redirect("user:signin")
