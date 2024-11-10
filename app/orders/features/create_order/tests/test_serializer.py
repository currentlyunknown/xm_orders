import uuid
from dataclasses import asdict
from typing import Any, Dict

import pytest

from ..serializers import OrderPostSerializer


@pytest.fixture
def payload(conversion_command) -> Dict[str, Any]:
    return asdict(conversion_command)


@pytest.mark.django_db
class TestOrderPostSerializer:
    def test_validation_fails_when_no_payload(self):
        serializer = OrderPostSerializer(data={})
        assert not serializer.is_valid(raise_exception=False)

    @pytest.mark.parametrize("invalid_currency", ("XXX", "", "GGGG"))
    def test_validation_fails_with_invalid_source_currency(
        self, payload, invalid_currency
    ):
        payload["source_currency"] = invalid_currency
        serializer = OrderPostSerializer(data=payload)
        assert not serializer.is_valid(raise_exception=False)
        assert "source_currency" in serializer.errors

    @pytest.mark.parametrize("invalid_currency", ("XXX", "", "GGGG"))
    def test_validation_fails_when_target_currency_is_incorrect(
        self, payload, invalid_currency
    ):
        payload["target_currency"] = invalid_currency
        serializer = OrderPostSerializer(data=payload)
        assert not serializer.is_valid(raise_exception=False)
        assert "target_currency" in serializer.errors

    def test_validation_fails_when_user_id_is_invalid(self, payload):
        payload["user_id"] = uuid.uuid4()
        serializer = OrderPostSerializer(data=payload)
        assert not serializer.is_valid(raise_exception=False)
        assert "user_id" in serializer.errors

    def test_validation_passes_with_correct_data(self, payload):
        serializer = OrderPostSerializer(data=payload)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.validated_data["user_id"] == payload["user_id"]
        assert (
            serializer.validated_data["source_currency"] == payload["source_currency"]
        )
        assert (
            serializer.validated_data["source_quantity"] == payload["source_quantity"]
        )
        assert (
            serializer.validated_data["target_currency"] == payload["target_currency"]
        )
