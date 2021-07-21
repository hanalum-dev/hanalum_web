from tests.factories.board_factory import BoardFactory
import factory

class ArticleFactory(factory.django.DjangoModelFactory):
  class Meta:
    model='articles.Article'
    django_get_or_create = ('title', 'content')
  title = factory.Sequence(lambda n: 'Article Title %d' % n)
  content = factory.Sequence(lambda n: 'Article %d' % n)
  board = factory.SubFactory(BoardFactory)
