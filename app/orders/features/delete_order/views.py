from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Order


class OrderDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "order_id"

    def delete(self, request, **kwargs) -> Response:
        order_id = kwargs.get(self.lookup_field)
        user_id = request.user.id

        try:
            order = Order.objects.get(id=order_id, user_id=user_id)
        except Order.DoesNotExist:
            raise Http404()

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
