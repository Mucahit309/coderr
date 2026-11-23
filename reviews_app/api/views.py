"""Views for the review endpoints."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review

from .filters import ReviewFilter
from .permissions import IsCustomerUser, IsReviewOwner
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateView(ListCreateAPIView):
    """Lists reviews and lets customers create new ones."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        """Allow customers to create, all logged in users to read."""
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Save the review, only one per business user is allowed."""
        reviewer = self.request.user
        business_user = serializer.validated_data["business_user"]
        if Review.objects.filter(
            business_user=business_user, reviewer=reviewer
        ).exists():
            raise PermissionDenied(
                "You have already reviewed this business user."
            )
        serializer.save(reviewer=reviewer)


class ReviewDetailView(UpdateAPIView, DestroyAPIView):
    """Lets the creator of a review update or delete it."""

    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]
    http_method_names = ["patch", "delete", "options"]
