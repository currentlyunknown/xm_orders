from decimal import Decimal

from celery import shared_task

from ..interface import ConversionCommand, conversion_handler_factory
from ..models import Order


@shared_task()
def process_order(order_id):
    order = Order.objects.get(id=order_id)
    order.mark_as_started()
    try:
        command = ConversionCommand(
            user_id=order.user.id,
            source_quantity=order.source_quantity,
            source_currency=order.source_currency,
            target_currency=order.target_currency,
        )
        handler = conversion_handler_factory()
        target_quantity: Decimal = handler.handle(command)
    except Exception as error:
        order.mark_as_failed(error=str(error))
        raise error
    else:
        order.mark_as_executed(target_quantity=target_quantity)
