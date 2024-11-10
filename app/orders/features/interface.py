import time
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID


class OrderStatus(Enum):
    PENDING = "pending"
    STARTED = "started"
    FAILED = "failed"
    CANCELED = "canceled"
    EXECUTED = "executed"


@dataclass
class ConversionCommand:
    user_id: UUID
    source_quantity: Decimal
    source_currency: str
    target_currency: str
    version: int = 1


class ConversionHandler:
    def handle(self, command: ConversionCommand) -> Decimal:
        time.sleep(3)
        return Decimal("123.45")


def conversion_handler_factory() -> ConversionHandler:
    return ConversionHandler()


CURRENCIES = ("USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD")
