"""Views for the order endpoints."""

from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from orders_app.models import Order

from .serializers import OrderSerializer


class OrderListView(ListAPIView):
    """Lists the orders of the logged in user."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return orders where the user is customer or business."""
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )
