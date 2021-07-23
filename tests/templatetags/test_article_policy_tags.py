from django.test import TestCase
from articles.templatetags import article_policy_tags
from tests.factories.user_factory import UserFactory

class ArticlePolicyTagTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.User = UserFactory._meta.model

  def setUp(self):
    self.user = UserFactory()

  def test_comment_restrictable(self):
    self.assertFalse(article_policy_tags.comment_restrictable(self.user))
    self.user.is_admin = True
    self.user.save()
    self.assertTrue(article_policy_tags.comment_restrictable(self.user))
