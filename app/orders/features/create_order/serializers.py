from uuid import UUID

from rest_framework import fields, serializers

from ..interface import CURRENCIES, ConversionCommand
from ..models import CustomUser


class OrderPostSerializer(serializers.Serializer):
    user_id = fields.UUIDField(required=True)
    source_currency = serializers.CharField(required=True, max_length=3)
    source_quantity = serializers.DecimalField(
        required=True, max_digits=12, decimal_places=2
    )
    target_currency = serializers.CharField(required=True, max_length=3)

    def _validate_currency_code(self, currency_code: str) -> str:
        if currency_code not in CURRENCIES:
            raise serializers.ValidationError(
                f"{currency_code} is not a valid currency code."
            )
        return currency_code

    def validate_user_id(self, user_id: UUID) -> UUID:
        try:
            CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"No user found with ID {user_id}.")
        else:
            return user_id

    def validate_source_currency(self, currency_code: str) -> str:
        return self._validate_currency_code(currency_code=currency_code)

    def validate_target_currency(self, currency_code: str) -> str:
        return self._validate_currency_code(currency_code=currency_code)

    def create(self, validated_data) -> ConversionCommand:
        return ConversionCommand(**validated_data)
