from django.urls import path

from .views import OrderCancelView

urlpatterns = [
    path(
        "<uuid:order_id>",
        OrderCancelView.as_view(),
        name="cancel_order",
    ),
]
