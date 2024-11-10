import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from orders.features.tests.fakers import OrderFaker, UserFaker


@pytest.mark.django_db
class TestOrderDeleteView:
    base_url = "orders:delete_order"

    def test_url(self):
        order_id = uuid.uuid4()
        expected_url = f"/api/orders/delete-order/{order_id}"
        assert reverse(self.base_url, kwargs={"order_id": order_id}) == expected_url

    def test_successful_deletion_returns_204(self, client, user, user_order):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": user_order.id})
        response = client.delete(url, format="json", follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_returns_404_if_order_from_another_user(self, client, user):
        client.force_authenticate(user=user)
        url = reverse(self.base_url, kwargs={"order_id": OrderFaker().id})
        response = client.delete(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_if_order_does_not_exist(self, client):
        client.force_authenticate(user=UserFaker())
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.delete(url, format="json", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_401_if_not_authenticated(self, client):
        url = reverse(self.base_url, kwargs={"order_id": uuid.uuid4()})
        response = client.delete(url, format="json", follow=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
