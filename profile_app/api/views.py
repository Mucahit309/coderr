"""Views for the profile endpoints."""

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profile_app.models import UserProfile

from .permissions import IsProfileOwner
from .serializers import (
    CustomerProfileListSerializer,
    ProfileListSerializer,
    ProfileSerializer,
)


class ProfileDetailView(RetrieveUpdateAPIView):
    """Retrieves or updates the profile of a user."""

    queryset = UserProfile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    lookup_field = "user_id"
    lookup_url_kwarg = "pk"
    http_method_names = ["get", "patch", "head", "options"]


class BusinessProfileListView(ListAPIView):
    """Lists all business profiles."""

    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only profiles of business users."""
        return UserProfile.objects.select_related("user").filter(
            type=UserProfile.BUSINESS
        )


class CustomerProfileListView(ListAPIView):
    """Lists all customer profiles."""

    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only profiles of customer users."""
        return UserProfile.objects.select_related("user").filter(
            type=UserProfile.CUSTOMER
        )
