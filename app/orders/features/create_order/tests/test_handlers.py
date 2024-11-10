from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from ...interface import ConversionCommand, OrderStatus
from ...models import Order
from ..handlers import OrderHandler, OrderResult


@pytest.mark.django_db
class TestOrderHandler:
    pending_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)

    @freeze_time(pending_at)
    def test_order_handler_creates_Order_object(
        self, conversion_command: ConversionCommand
    ):
        mocked_celery_task_function = Mock()

        handler = OrderHandler(celery_task=mocked_celery_task_function)

        result = handler.handle(conversion_command)

        assert Order.objects.count() == 1
        assert isinstance(result, OrderResult)
        assert result.order_status == OrderStatus.PENDING.value

        order: Order = Order.objects.get(id=result.order_id)

        assert order.pending_at == self.pending_at
        assert order.status == OrderStatus.PENDING.value
        assert order.user_id == conversion_command.user_id
        assert order.source_currency == conversion_command.source_currency
        assert order.source_quantity == conversion_command.source_quantity
        assert order.target_currency == conversion_command.target_currency

        mocked_celery_task_function.apply_async.assert_called()
