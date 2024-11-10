from django.urls import path

from .views import OrderGetView

urlpatterns = [
    path(
        "<uuid:order_id>",
        OrderGetView.as_view(),
        name="get_order",
    ),
]
