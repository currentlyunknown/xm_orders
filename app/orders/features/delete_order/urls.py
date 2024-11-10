from django.urls import path

from .views import OrderDeleteView

urlpatterns = [
    path(
        "<uuid:order_id>",
        OrderDeleteView.as_view(),
        name="delete_order",
    ),
]
