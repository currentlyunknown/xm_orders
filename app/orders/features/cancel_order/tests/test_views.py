import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from orders.features.tests.fakers import OrderFaker

from ...interface import OrderStatus


@pytest.mark.django_db
class TestOrderCancelView:
    base_url = "orders:cancel_order"

    def test_url(self):
        order_id = uuid.uuid4()
        expected_url = f"/api/orders/cancel-order/{order_id}"
        assert reverse(self.base_url, kwargs={"order_id": order_id}) == expected_url

    def test_successful_cancellation_returns_updated_order(
        self, client, user, user_order
    ):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": user_order.id})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["status"] == "canceled"
        )  # Confirm the order status has been updated

    def test_returns_400_if_order_status_is_not_pending(self, client, user):
        non_pending_order = OrderFaker(user=user, status=OrderStatus.EXECUTED.value)
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": non_pending_order.id})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Only pending status orders can be canceled"

    def test_returns_404_if_order_does_not_exist(self, client, user):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_if_order_belongs_to_another_user(self, client, user):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": OrderFaker().id})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_401_if_user_is_not_authenticated(self, client):
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
