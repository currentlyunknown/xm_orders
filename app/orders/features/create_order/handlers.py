from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.utils.timezone import now

from ..interface import ConversionCommand, OrderStatus
from ..models import Order
from .tasks import process_order


@dataclass
class OrderResult:
    order_id: UUID
    order_status: str


@staticmethod
def order_handler_factory() -> OrderHandler:
    return OrderHandler(celery_task=process_order)


class OrderHandler:
    def __init__(self, celery_task):
        self.celery_task = celery_task

    def handle(self, command: ConversionCommand) -> OrderResult:
        task = self._create_order(command=command)
        self.celery_task.apply_async(args=[task.id])

        return OrderResult(order_id=task.id, order_status=task.status)

    def _create_order(self, command: ConversionCommand) -> Order:
        order = Order.objects.create(
            user_id=command.user_id,
            source_currency=command.source_currency,
            source_quantity=command.source_quantity,
            target_currency=command.target_currency,
            status=OrderStatus.PENDING.value,
            pending_at=now(),
        )

        return order
