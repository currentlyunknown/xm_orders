import uuid

import pytest
from django.urls import reverse

from orders.features.get_orders.views import OrderGetListSerializer

from ...models import Order


@pytest.mark.django_db
class TestOrderListGetView:
    base_url = "orders:get_orders"

    def test_url(self):
        expected_url = reverse(self.base_url)
        assert expected_url == "/api/orders/get-orders/"

    def test_returns_200_response_with_correct_data(
        self, authenticated_client, user_orders
    ):
        url = reverse(self.base_url)
        response = authenticated_client.get(url)
        assert response.status_code == 200

        response_data = response.json()
        expected_fields = list(OrderGetListSerializer().fields.keys())

        for document_data in response_data:
            for field in expected_fields:
                assert field in document_data

    def test_returns_200_response_with_no_documents_if_none_provided(
        self, authenticated_client
    ):
        url = reverse(self.base_url)
        response = authenticated_client.get(url)
        assert response.status_code == 200

        response_data = response.json()

        assert not response_data

    def test_returns_only_user_orders(
        self, authenticated_client, user, user_orders, non_user_orders
    ):
        url = reverse(self.base_url)
        response = authenticated_client.get(url)
        assert response.status_code == 200

        response_data = response.json()

        user_order_ids = set(
            Order.objects.filter(user=user).values_list("id", flat=True)
        )
        non_user_order_ids = set(
            Order.objects.exclude(user=user).values_list("id", flat=True)
        )

        for order_data in response_data:
            assert uuid.UUID(order_data["id"]) in user_order_ids
            assert uuid.UUID(order_data["id"]) not in non_user_order_ids

    def test_returns_401_if_not_authenticated(self, client):
        url = reverse(self.base_url)
        response = client.get(url)
        assert response.status_code == 401
