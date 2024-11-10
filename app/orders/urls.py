from django.urls import include, path

app_name = "orders"

urlpatterns = [
    path(
        "create-order/",
        include("orders.features.create_order.urls"),
    ),
    path(
        "get-order-status/",
        include("orders.features.get_order_status.urls"),
    ),
    path(
        "get-order/",
        include("orders.features.get_order.urls"),
    ),
    path(
        "get-orders/",
        include("orders.features.get_orders.urls"),
    ),
    path(
        "delete-order/",
        include("orders.features.delete_order.urls"),
    ),
    path(
        "cancel-order/",
        include("orders.features.cancel_order.urls"),
    ),
]
