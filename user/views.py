"""user(사용자 계정) views 모듈입니다."""
from copy import deepcopy as dp
import logging

from django.contrib import auth, messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from helpers.default import default_response
from .forms import UserConfirmationForm, UserCreationForm
from .models import User
from .tokens import account_activation_token
from .validators import UserCreationValidator
from history.models import LikeActivity, ViewHistory
from article.models import Article
from hanmaum.models import HanmaumArticle

logger = logging.getLogger(__name__)
ARTICLE = Article()
HANMAUMARTICLE = HanmaumArticle()
like_activity = LikeActivity()
view_history = ViewHistory()

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
            return render(request, 'user/registrations/new.dj.html', response)

        try:
            with transaction.atomic():
                if form.is_valid():
                    current_site = get_current_site(request)
                    form.save(current_site, request.POST['email'])
                    messages.success(request, '회원가입이 완료되었습니다. 이메일을 확인해주세요.')
                    return redirect('user:signin')
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(e)
        # TODO: 라벨링 다시 하기
        messages.error(request, '정보 입력이 제대로 되지 않았습니다.')
        return redirect('user:signup')
    else:
        response['form'] = UserCreationForm()
        return render(request, 'user/registrations/new.dj.html', response)


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
                return render(request, 'user/confirmations/new.dj.html', response)
            else:
                messages.success(request, '로그인되었습니다.')
                auth.login(request, user)
                return redirect('/')
        else:
            messages.error(request, '오류가 발생하였습니다.')
            return render(request, 'user/confirmations/new.dj.html', response)

    else:
        if request.user.is_authenticated:
            messages.error(request, '이미 로그인되어있습니다.')
            return redirect('/')
        response['form'] = UserConfirmationForm()
        return render(request, 'user/confirmations/new.dj.html', response)


def signout(request):
    """로그아웃 뷰"""
    auth.logout(request)
    # TODO: HNM-0074: 메세지 프레임워크 활용: 로그아웃되었습니다
    return redirect('/')

def me(request):
    response = dp(default_response)
    user = get_object_or_404(User, pk=request.user.id)

    if not request.user.is_authenticated or not user:
        messages.error(request, "로그인 후, 이용할 수 있습니다.")
        return redirect("user:signin")

    # FIXME: activity 개선하면서 작동 안될거임.(게시물을 가져오는게 아니라 activity가 리턴됨.)
    like_articles = like_activity.get_like_activities(
        _user=user,
        _content_object=ARTICLE
    )
    for like_article in like_articles:
        try:
            article = Article.objects.get(id=like_article.id)
            like_article.title = article.title
            like_article.updated_at = article.updated_at
        except:
           continue

    # TODO: 코드 개선하기
    like_hanmaum_activities = like_activity.get_like_activities(
        _user=user,
        _content_object=HANMAUMARTICLE
    )

    for activity in like_hanmaum_activities:
        try:
            activity.article = HanmaumArticle.objects.get(id = activity.content_id)
            activity.article.total_viewed_count = view_history.total_viewed_count(
            _viewed_obj=activity.article,
            )
        except:
            pass

    response.update({
        'user':user,
        'like_articles': like_articles,
        'like_hanmaum_activities': like_hanmaum_activities
    })

    return render(request, 'user/me.dj.html', response)

def show(request, user_id):
    """사용자 페이지 뷰"""
    response = dp(default_response)
    user = get_object_or_404(User, pk=user_id)
    response['user'] = user
    return render(request, 'user/show.dj.html', response)


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
    # TODO: HNM-0075: transaction 적용하기
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        # TODO: HNM-0076: 메세지 프레임워크 적용하기
        # 이메일 인증이 되었습니다.
        return redirect("user:signin")
    else:
        messages.error(request, '인증링크가 올바르지 않거나, 인증 기간이 만료되었습니다.')
        messages.error(request, '계속해서 오류가 발생한다면, 한아름에 건의해 주세요.')
        return redirect("user:signin")
