""" base_views """
from boards.models import Board
from copy import deepcopy as dp
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render, redirect
from hanalum_web.settings import DEBUG

from articles.models import Article
from boards.models import Board
from hanmaum.models import HanmaumArticle
from users.models import User
from notices.models import Notice
from helpers.default import default_response
from helpers.exeptions import NoPermissionException


def catch_all_exceptions(function):
    """
        views 상에서 공통적으로 사용되는 exceptions를
        decorator로 정의합니다.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        response = dp(default_response)
        if DEBUG:
            return function(*args, **kwargs)
        try:
            return function(*args, **kwargs)
        except NoPermissionException:
            return render(args[0], '402.html')
        except Article.DoesNotExist :
            return render(args[0], '404.html')
        except Board.DoesNotExist:
            return render(args[0], '404.html')
        except HanmaumArticle.DoesNotExist:
            return render(args[0], '404.html')
        except User.DoesNotExist:
            return render(args[0], '404.html')
        except Notice.DoesNotExist:
            return render(args[0], '404.html')
        except Exception as e:
            return render(args[0], '500.html')
    return wrapper
