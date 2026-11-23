"""Views for the order endpoints."""

from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from orders_app.models import Order

from .permissions import IsCustomerUser
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(ListCreateAPIView):
    """Lists the user's orders and lets customers create orders."""

    def get_permissions(self):
        """Allow customers to create, all logged in users to read."""
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Use the create format for POST, the read format otherwise."""
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        """Return orders where the user is customer or business."""
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )
