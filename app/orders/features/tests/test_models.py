import pytest

from orders.features.tests.fakers import OrderFaker

from ..models import Order


@pytest.mark.django_db
class TestModels:
    def test_order(self):
        OrderFaker()
        assert Order.objects.count() == 1
