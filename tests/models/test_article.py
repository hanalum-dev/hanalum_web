from tests.factories.article_factory import ArticleFactory
from articles.models import Article
from boards.models import Board
from django.test import TestCase

class ArticleModelMethodTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.Article = ArticleFactory._meta.model

  def setUp(self):
    self.article = ArticleFactory(title='DUMMY_ARTICLE', content="DUMMY_CONTENT")

  def test_str_method(self):
    self.assertEqual(str(self.article), f"[{self.article.board.title}] {self.article.title}")

  def test_abstract_title_method(self):
    self.assertEqual(self.article.title, self.article.abstract_title)
    self.article.title="TEST_"*10
    self.article.save()
    self.assertEqual(len(self.article.abstract_title), 30)
    self.assertEqual(self.article.abstract_title[-3:], '...')

  def test_class_name_classmethod(self):
    self.assertEqual(Article.classname(), '게시판')
