from __future__ import annotations

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField, Serializer, UUIDField
from rest_framework.views import APIView

from ..interface import OrderStatus
from ..models import Order


class OrderCancelSerializer(Serializer):
    id = UUIDField()
    status = CharField()


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCancelSerializer
    lookup_field = "order_id"

    def get(self, request, **kwargs) -> Response:
        order_id = kwargs.get(self.lookup_field)
        user_id = request.user.id

        try:
            order = Order.objects.get(id=order_id, user_id=user_id)
        except Order.DoesNotExist:
            raise Http404()

        if order.status == OrderStatus.PENDING.value:
            order.mark_as_canceled()
            order.save()
        else:
            return Response(
                {"error": "Only pending status orders can be canceled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(order)

        return Response(serializer.data)
