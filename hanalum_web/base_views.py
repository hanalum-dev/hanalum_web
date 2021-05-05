""" base_views """
from functools import wraps

from django.http import HttpResponse

from articles.models import Article
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
            # TODO: NoPermission Page
            return HttpResponse('<h1>You are not authorized to view this page</h1>', status=402)
        except Article.DoesNotExist:
            # TODO: DoesNotPage
            return HttpResponse('<h1>없는 게시글입니다.</h1>', status=404)
    return wrapper
