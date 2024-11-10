from __future__ import annotations

from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField, DecimalField, Serializer, UUIDField
from rest_framework.views import APIView

from ..models import Order


class OrderStatusGetSerializer(Serializer):
    id = UUIDField()
    status = CharField()
    target_quantity = DecimalField(max_digits=12, decimal_places=2, required=False)


class OrderStatusGetView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderStatusGetSerializer
    lookup_field = "order_id"

    def get(self, request, **kwargs) -> Response:
        order_id = kwargs.get(self.lookup_field)
        user_id = request.user.id

        try:
            order = Order.objects.get(id=order_id, user_id=user_id)
        except Order.DoesNotExist:
            raise Http404()

        serializer = self.serializer_class(order)

        return Response(serializer.data)
