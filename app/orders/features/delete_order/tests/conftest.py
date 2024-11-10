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
def user_order(user):
    return OrderFaker(user=user)
