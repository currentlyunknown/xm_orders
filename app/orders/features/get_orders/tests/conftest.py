import pytest
from rest_framework.test import APIClient

from orders.features.tests.fakers import OrderFaker, UserFaker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return UserFaker()


@pytest.fixture
def user_orders(user):
    return OrderFaker.create_batch(5, user=user)


@pytest.fixture
def non_user_orders():
    return OrderFaker.create_batch(5)


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
