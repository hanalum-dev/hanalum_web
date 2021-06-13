"""article validator"""
from boards.models import Board
from helpers.exeptions import NoPermissionException

from .models import Article


class ArticlePermissionValidator():
    """Article views마다의 권한 제어 클래스"""

    @classmethod
    def show(cls, current_user, article_id):
        """show validator"""

        article = Article.objects.get(pk=article_id)

        board = article.board

        if article.status != 'p':
            raise NoPermissionException()
        if not current_user or not current_user.is_authenticated:
            if board.auth_read > 0 or not board.visible_anonymous:
                raise NoPermissionException()
        elif current_user.read_authority < board.auth_read and not current_user.is_admin:
            raise NoPermissionException()

    @classmethod
    def new(cls, current_user, board_id):
        """new validator"""

        board = Board.objects.get(pk=board_id)

        if not current_user or not current_user.is_authenticated:
            raise NoPermissionException()
        if current_user.write_authority < board.auth_write and not current_user.is_admin:
            raise NoPermissionException()

        return True

    @classmethod
    def edit(cls, current_user, article_id):
        """edit validator"""

        article = Article.objects.get(pk=article_id)
        board = article.board

        cls.new(current_user, board.id)

        if article.status != 'p':
            raise NoPermissionException()
        if current_user != article.author and not current_user.is_admin:
            raise NoPermissionException()

        return True

    @classmethod
    def delete(cls, current_user, article_id):
        """delete validator"""

        cls.edit(current_user, article_id)

        return True

    @classmethod
    def like(cls, current_user, article_id):
        """like validator"""

        article = Article.objects.get(pk=article_id)

        cls.show(current_user, article_id)

        if not article.board.use_good:
            raise NoPermissionException()

        return True

    @classmethod
    def dislike(cls, current_user, article_id):
        """dislike validator"""

        article = Article.objects.get(pk=article_id)

        cls.show(current_user, article_id)

        if not article.board.use_bad:
            raise NoPermissionException()

        return True

    @classmethod
    def restrict_comment(cls, current_user, article_id):
        Article.objects.get(pk=article_id)

        if not current_user.is_admin:
            return NoPermissionException()

        return True

    @classmethod
    def allow_comment(cls, current_user, article_id):
        Article.objects.get(pk=article_id)

        if not current_user.is_admin:
            return NoPermissionException()

        return True
