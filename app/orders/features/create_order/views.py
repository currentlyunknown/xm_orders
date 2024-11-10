from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .handlers import order_handler_factory
from .serializers import OrderPostSerializer


class OrderPostView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderPostSerializer
    handler_factory = order_handler_factory

    def post(self, request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        command = serializer.save()

        handler = self.handler_factory()
        result = handler.handle(command=command)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "order_id": result.order_id,
                "order_status": result.order_status,
            },
        )
