"""URL routes of the orders_app."""

from django.urls import path

from .views import OrderCountView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "order-count/<int:business_user_id>/",
        OrderCountView.as_view(),
        name="order-count",
    ),
]
