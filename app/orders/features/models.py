import uuid
from decimal import Decimal

from django.db import models
from django.utils.timezone import now

from accounts.models import CustomUser

from .interface import OrderStatus


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    source_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    source_currency = models.CharField(max_length=3)
    target_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    target_currency = models.CharField(max_length=3)
    status = models.CharField(default=OrderStatus.PENDING.value, max_length=255)
    error = models.TextField(blank=True)
    pending_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    executed_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-pending_at"]

    def mark_as_started(self):
        self.status = OrderStatus.STARTED.value
        self.started_at = now()
        self.save()

    def mark_as_failed(self, error: str):
        self.status = OrderStatus.FAILED.value
        self.error = error
        self.save()

    def mark_as_canceled(self):
        self.status = OrderStatus.CANCELED.value
        self.canceled_at = now()
        self.save()

    def mark_as_executed(self, target_quantity: Decimal):
        self.target_quantity = target_quantity
        self.executed_at = now()
        self.status = OrderStatus.EXECUTED.value
        self.save()
