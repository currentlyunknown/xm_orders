import factory.fuzzy

from accounts.models import CustomUser

from ..models import Order


class UserFaker(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"test_user{'' if not n else n}@example.com")


class OrderFaker(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFaker)
    source_currency = "USD"
    source_quantity = 100
    target_currency = "EUR"
