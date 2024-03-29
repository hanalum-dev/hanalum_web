"""user(사용자 계정) views 모듈입니다."""
from django.http import response
from comments.models import Comment
from copy import deepcopy as dp
import logging

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from helpers.default import default_response
from .forms import UserConfirmationForm, UserCreationForm, CustomPasswordChangeForm
from .models import User
from .tokens import account_activation_token
from configs.views import catch_all_exceptions
from .validators import UserCreationValidator, UserPasswordEditionValidator, UserPermissionValidator
from history.models import LikeActivity
from articles.models import Article
from hanmaum.models import HanmaumArticle

logger = logging.getLogger(__name__)


@transaction.atomic
def signup(request):
    """회원가입 뷰"""
    response = {
        'non_nav' : True,
        'non_banner' : True,
        'status' : True,
        'msg' : '',
        'form' : None,
    }

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
            return render(request, 'users/registrations/new.dj.html', response)

        try:
            with transaction.atomic():
                if form.is_valid():
                    current_site = get_current_site(request)
                    form.save(current_site, request.POST['email'])
                    messages.success(request, '회원가입이 완료되었습니다. 이메일을 확인해주세요.')
                    return redirect('users:signin')
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(e)
        messages.error(request, '인증 이메일을 발송하는 과정에서 오류가 발생하였습니다. 계속 해당 오류가 발생한다면, 한아름에 문의해주세요.')
        return redirect('users:signup')
    else:
        response['form'] = UserCreationForm()
        return render(request, 'users/registrations/new.dj.html', response)


def signin(request):
    """로그인 뷰"""
    response = {
        'non_nav' : True,
        'non_banner' : True,
    }

    if request.method == 'POST':
        form = response['form'] = UserConfirmationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=email, password=password)

            if user is None:
                # TODO: message가 아니라 validation text로 나오게 하기
                messages.error(request, '이메일 혹은 비밀번호가 제대로 입력되지 않았습니다.')
                return render(request, 'users/confirmations/new.dj.html', response)
            elif not user.is_active:
                messages.error(request, '이메일로 발송된 인증 이메일을 확인해주세요.')
                return render(request, 'users/confirmations/new.dj.html', response)
            else:
                messages.success(request, '로그인되었습니다.')
                auth.login(request, user)
                return redirect('/')
        else:
            messages.error(request, '오류가 발생하였습니다.')
            return render(request, 'users/confirmations/new.dj.html', response)

    else:
        if request.user.is_authenticated:
            messages.error(request, '이미 로그인되어있습니다.')
            return redirect('/')
        response['form'] = UserConfirmationForm()
        return render(request, 'users/confirmations/new.dj.html', response)


def signout(request):
    """로그아웃 뷰"""
    auth.logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('/')


@catch_all_exceptions
@login_required(login_url='/users/signin')
def me(request):
    response = dp(default_response)
    current_user = request.user

    like_articles = LikeActivity.get_like_content_objects(
        _user=current_user,
        _content_object=Article,
    )
    like_hanmaum_articles = LikeActivity.get_like_content_objects(
        _user=current_user,
        _content_object=HanmaumArticle
    )
    create_articles = Article.get_articles_include_anonymous_author_created_by(current_user)
    recent_comments = Comment.get_recent_user_comments(
        _user=current_user
    )

    response.update({
        'user': current_user,
        'like_articles': like_articles,
        'like_hanmaum_articles': like_hanmaum_articles,
        'recent_comments': recent_comments,
        'create_articles' : create_articles
    })

    return render(request, 'users/me.dj.html', response)


@catch_all_exceptions
def show(request, user_id):
    """사용자 페이지 뷰"""
    response = dp(default_response)
    user = User.objects.get(pk=user_id)

    UserPermissionValidator.show(user_id)

    like_articles = LikeActivity.get_like_content_objects(
        _user=user,
        _content_object=Article,
    )
    like_hanmaum_articles = LikeActivity.get_like_content_objects(
        _user=user,
        _content_object=HanmaumArticle
    )
    create_articles = Article.get_articles_created_by(user)

    response.update({
        'user': user,
        'like_articles': like_articles,
        'like_hanmaum_articles': like_hanmaum_articles,
        'create_articles' : create_articles
    })

    return render(request, 'users/show.dj.html', response)

# @catch_all_exceptions
# @login_required(login_url='/users/signin')
# def edit(request):
#     """ 사용자 정보 수정 페이지 뷰"""
#     response = dp(default_response)
#     current_user = request.user

#     response.update({
#         'user': current_user,
#         'form' : UserModifyForm()
#     })

#     if request.method == 'POST':
#         form = response['form'] = UserModifyForm(request.POST, request.FILES)

#         if form.is_valid():
#             password = form.cleaned_data['password']
#             avatar = form.cleaned_data['avatar']
#             user = auth.authenticate(request, username=current_user.email, password=password)
#             form.save()
#             messages.error(request, '유저 정보가 변경되었습니다!')
#             return redirect('users:me')
#         else:
#             messages.error(request, '유저 정보가 변경하는데 실패했습니다 :(')
#             return render(request,  'users/edit.dj.html', response)

#     else:
#         response['form'] = UserModifyForm()

#     return render(request, 'users/edit.dj.html', response)

# @catch_all_exceptions


@login_required(login_url='/users/signin')
def password_edit(request):
    """ 사용자 정보 수정 페이지 뷰"""
    response = dp(default_response)
    current_user = request.user

    response.update({
        'user': current_user,
        'form': CustomPasswordChangeForm(current_user)
    })

    if request.method == 'POST':
        form = response['form'] = CustomPasswordChangeForm(current_user, request.POST)
        _password1 = request.POST.get('new_password1')
        _password2 = request.POST.get('new_password2')

        validate_user_form_result = UserPasswordEditionValidator().validate(
            _password1=_password1, _password2=_password2,
        )

        if not validate_user_form_result.status:
            response['status'] = validate_user_form_result.status
            response['msg'] = validate_user_form_result.msg
            response['form'] = form
            messages.error(request, '비밀번호가 변경되지 않았습니다.')
            return render(request, 'users/passwords/edit.dj.html', response)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    messages.success(request, '비밀번호가 정상적으로 변경되었습니다.')
                    return redirect("users:me")
                else:
                    messages.error(request, '비밀번호가 변경되지 않았습니다. :(')
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(e)
        messages.error(request, '비밀번호가 변경되지 않았습니다. :(')
    else:
        response['form'] = CustomPasswordChangeForm(current_user)
    return render(request, 'users/passwords/edit.dj.html', response)


def delete(request):
    """사용자 회원 탈퇴 반영 뷰"""


@transaction.atomic
def activate_account(request, uidb64, token):
    """사용자 인증 메일 활성화 뷰"""
    try:
        with transaction.atomic():
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                auth.login(request, user)
                messages.success(request, '이메일 인증이 완료되었습니다.')
                return redirect("users:signin")
            else:
                messages.error(request, '인증링크가 올바르지 않거나, 인증 기간이 만료되었습니다. 계속해서 오류가 발생한다면, 한아름에 문의해 주세요.')
                return redirect("users:signin")
    except(TypeError, ValueError, OverflowError) as e:
        user = None
        logger.error(e)
