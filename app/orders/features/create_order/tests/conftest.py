from decimal import Decimal

import pytest

from orders.features.interface import ConversionCommand
from orders.features.tests.fakers import UserFaker


@pytest.fixture
def user():
    return UserFaker()


@pytest.fixture
def conversion_command(user) -> ConversionCommand:
    return ConversionCommand(
        user_id=user.id,
        source_currency="USD",
        source_quantity=Decimal("100.00"),
        target_currency="EUR",
    )


@pytest.fixture
def target_quantity() -> Decimal:
    return Decimal("1.23")
