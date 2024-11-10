from dataclasses import asdict
from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from ...interface import OrderStatus
from ...models import Order
from ..handlers import OrderResult
from ..views import OrderPostView


@pytest.mark.django_db
class TestExportTaskPostView:
    handler_factory_path = "orders.features.create_order.views.order_handler_factory"
    url = reverse("orders:create_order")

    def test_url(self):
        assert self.url == "/api/orders/create-order/"

    @pytest.mark.skip
    def test_api_client_creates_order_and_returns_201(self, conversion_command):
        client = APIClient()

        mock_handler_factory = Mock(return_value=Mock())

        with patch(self.handler_factory_path, return_value=mock_handler_factory):
            response = client.post(
                self.url, data=asdict(conversion_command), format="json", follow=True
            )

        assert response.status_code == 201
        assert Order.objects.count() == 1
        assert response.data["order_status"] == OrderStatus.PENDING.value
        assert response.data["order_id"] == Order.objects.first().id

    def test_view_creates_order_and_returns_201(self, conversion_command):
        result = OrderResult(order_id=1, order_status=OrderStatus.PENDING.value)

        mock_handler = Mock()
        mock_handler.handle.return_value = result

        mock_handler_factory = Mock(return_value=mock_handler)

        rf = APIRequestFactory()
        request = rf.post(path="/")
        request.data = asdict(conversion_command)

        response = OrderPostView(
            handler_factory=mock_handler_factory,
        ).post(request)

        assert response.status_code == 201
        assert response.data["order_status"] == result.order_status
        assert response.data["order_id"] == result.order_id
