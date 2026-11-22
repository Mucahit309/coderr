"""Views for the offer endpoints."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import IsBusinessUser
from .queries import annotated_offers
from .serializers import (
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferSerializer,
)


class OfferListCreateView(ListCreateAPIView):
    """Lists offers and lets business users create new ones."""

    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        """Allow anyone to read, only business users to create."""
        if self.request.method == "POST":
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        """Use the overview for reading, the full data for creating."""
        if self.request.method == "POST":
            return OfferSerializer
        return OfferListSerializer

    def get_queryset(self):
        """Return all offers with min price and delivery time."""
        return annotated_offers()

    def perform_create(self, serializer):
        """Save the offer with the logged in user as creator."""
        serializer.save(user=self.request.user)


class OfferDetailView(RetrieveAPIView):
    """Returns a single offer."""

    serializer_class = OfferRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return all offers with min price and delivery time."""
        return annotated_offers()
