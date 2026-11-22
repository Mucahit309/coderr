"""Views for the offer endpoints."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .filters import OfferFilter
from .pagination import OfferPagination
from .queries import annotated_offers
from .serializers import OfferListSerializer


class OfferListView(ListAPIView):
    """Lists offers with filtering, search and ordering."""

    serializer_class = OfferListSerializer
    permission_classes = [AllowAny]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        """Return all offers with min price and delivery time."""
        return annotated_offers()
