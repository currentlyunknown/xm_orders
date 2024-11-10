from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from ..models import Order


class OrderGetListSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderListGetView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderGetListSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user_id=user_id)
        return queryset
