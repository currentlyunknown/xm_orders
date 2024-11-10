from decimal import Decimal
from unittest.mock import patch

import pytest
from django.utils.timezone import now
from freezegun import freeze_time

from ...interface import ConversionCommand, OrderStatus
from ...models import Order
from ..tasks import process_order


@pytest.mark.django_db
class TestOrderProcessing:
    handler_factory_path = "orders.features.interface"
    translation_handler_path = f"{handler_factory_path}.ConversionHandler.handle"

    @freeze_time("2024-01-01 12:00:00")
    def test_handle_request_function_updates_Order_object(
        self, conversion_command: ConversionCommand, target_quantity: Decimal
    ):
        order = Order.objects.create(
            user_id=conversion_command.user_id,
            source_currency=conversion_command.source_currency,
            source_quantity=conversion_command.source_quantity,
            target_currency=conversion_command.target_currency,
            status=OrderStatus.PENDING.value,
            pending_at=now(),
        )

        with patch(self.translation_handler_path, return_value=target_quantity):
            process_order(order_id=order.id)

        order.refresh_from_db()

        assert order.user_id == conversion_command.user_id
        assert order.source_currency == conversion_command.source_currency
        assert order.source_quantity == conversion_command.source_quantity
        assert order.target_currency == conversion_command.target_currency
        assert order.started_at is not None
        assert order.executed_at is not None
        assert order.status == OrderStatus.EXECUTED.value
        assert order.target_quantity == target_quantity

    @freeze_time("2024-01-01 12:00:00")
    def test_handle_request_function_updates_Order_object_with_error(
        self, conversion_command: ConversionCommand
    ):
        error = "the export task failed badly"

        order = Order.objects.create(
            user_id=conversion_command.user_id,
            source_currency=conversion_command.source_currency,
            source_quantity=conversion_command.source_quantity,
            target_currency=conversion_command.target_currency,
            status=OrderStatus.PENDING.value,
            pending_at=now(),
        )

        with patch(self.translation_handler_path, side_effect=Exception(error)):
            with pytest.raises(Exception):
                process_order(order_id=order.id)

        order.refresh_from_db()

        assert order.user_id == conversion_command.user_id
        assert order.source_currency == conversion_command.source_currency
        assert order.source_quantity == conversion_command.source_quantity
        assert order.target_currency == conversion_command.target_currency
        assert order.started_at is not None
        assert order.executed_at is None
        assert order.target_quantity is None
        assert order.status == OrderStatus.FAILED.value
        assert order.error == error
