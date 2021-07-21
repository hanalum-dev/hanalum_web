import factory

class BoardFactory(factory.django.DjangoModelFactory):
  class Meta:
    model='boards.Board'
    django_get_or_create = (
      'title',
    )
  title = factory.Sequence(lambda n: 'Board %d' % n)

