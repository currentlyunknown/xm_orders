from __future__ import annotations

from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ..models import Order


class OrderGetSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderGetView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderGetSerializer
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
