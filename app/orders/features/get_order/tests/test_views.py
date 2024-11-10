import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from orders.features.tests.fakers import OrderFaker, UserFaker


@pytest.mark.django_db
class TestOrderGetView:
    base_url = "orders:get_order"

    def test_url(self):
        order_id = uuid.uuid4()
        expected_url = f"/api/orders/get-order/{order_id}"
        assert reverse(self.base_url, kwargs={"order_id": order_id}) == expected_url

    def test_returns_200_response_with_correct_data(self, client, user, user_order):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": user_order.id})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.data
        assert uuid.UUID(response_data["id"]) == user_order.id

    def test_returns_404_if_conversion_from_another_user(self, client, user):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": OrderFaker().id})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_if_conversion_does_not_exist(self, client):
        client.force_authenticate(user=UserFaker())
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_401_if_not_a_user(self, client):
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.get(url, format="json", follow=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
