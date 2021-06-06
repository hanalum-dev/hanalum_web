""" base_views """
from boards.models import Board
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect

from articles.models import Article
from boards.models import Board
from hanmaum.models import HanmaumArticle
from users.models import User
from notices.models import Notice
from helpers.exeptions import NoPermissionException


def catch_all_exceptions(function):
    """
        views 상에서 공통적으로 사용되는 exceptions를
        decorator로 정의합니다.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except NoPermissionException:
            return redirect('402')
        except Article.DoesNotExist :
            return redirect('404')
        except Board.DoesNotExist:
            return redirect('404')
        except HanmaumArticle.DoesNotExist:
            return redirect('404')
        except User.DoesNotExist:
            return redirect('404')
        except Notice.DoesNotExist:
            return redirect('404')
        except Exception as e:
            return redirect('500')
    return wrapper
