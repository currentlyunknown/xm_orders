from django.urls import path

from .views import OrderPostView

urlpatterns = [
    path(
        "",
        OrderPostView.as_view(),
        name="create_order",
    ),
]
