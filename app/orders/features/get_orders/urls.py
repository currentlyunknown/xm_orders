from django.urls import path

from .views import OrderListGetView

urlpatterns = [
    path(
        "",
        OrderListGetView.as_view(),
        name="get_orders",
    ),
]
