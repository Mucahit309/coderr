"""Views for the order endpoints."""

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from profile_app.models import UserProfile

from .permissions import IsCustomerUser, IsOrderBusinessUser
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


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


class OrderDetailView(UpdateAPIView):
    """Lets the business user of an order update its status."""

    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated, IsOrderBusinessUser]
    http_method_names = ["patch", "options"]


class BusinessOrderCountView(APIView):
    """Base view counting the orders of a business user by status."""

    permission_classes = [IsAuthenticated]
    order_status = None
    response_key = None

    def get(self, request, business_user_id):
        """Return the number of orders with the given status."""
        business_user = get_object_or_404(
            User, pk=business_user_id, profile__type=UserProfile.BUSINESS
        )
        count = Order.objects.filter(
            business_user=business_user, status=self.order_status
        ).count()
        return Response({self.response_key: count})


class OrderCountView(BusinessOrderCountView):
    """Counts the orders in progress of a business user."""

    order_status = Order.IN_PROGRESS
    response_key = "order_count"


class CompletedOrderCountView(BusinessOrderCountView):
    """Counts the completed orders of a business user."""

    order_status = Order.COMPLETED
    response_key = "completed_order_count"
