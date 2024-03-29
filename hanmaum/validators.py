"""article validator"""
from helpers.exeptions import NoPermissionException

from .models import HanmaumArticle


class HanmaumArticlePermissionValidator():
    """Article views마다의 권한 제어 클래스"""

    @classmethod
    def new(cls, current_user):
        if not current_user or not current_user.is_authenticated:
            raise NoPermissionException()
        if not current_user.is_hanmaum_member:
            raise NoPermissionException()
        return True

    @classmethod
    def show(cls, current_user, article_id):
        """show validator"""

        article = HanmaumArticle.objects.get(pk=article_id)

        if current_user and current_user.is_authenticated and current_user.is_hanmaum_member:
            return True 
        if article.status != 'p':
            raise NoPermissionException()

    @classmethod
    def like(cls, current_user, article_id):
        """like validator"""

        article = HanmaumArticle.objects.get(pk=article_id)
        cls.show(current_user, article_id)

        return True

    @classmethod
    def dislike(cls, current_user, article_id):
        """dislike validator"""

        article = HanmaumArticle.objects.get(pk=article_id)
        cls.show(current_user, article_id)

        return True
