from django.urls import path

from .views import OrderStatusGetView

urlpatterns = [
    path(
        "<uuid:order_id>",
        OrderStatusGetView.as_view(),
        name="get_order_status",
    ),
]
