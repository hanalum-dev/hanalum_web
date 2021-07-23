import factory
from users.models import User
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model=User
    django_get_or_create = ('email', 'nickname')
  email = fake.email()
  nickname = fake.user_name()
