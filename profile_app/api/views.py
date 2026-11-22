"""Views for the profile endpoints."""

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profile_app.models import UserProfile

from .permissions import IsProfileOwner
from .serializers import ProfileSerializer


class ProfileDetailView(RetrieveUpdateAPIView):
    """Retrieves or updates the profile of a user."""

    queryset = UserProfile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    lookup_field = "user_id"
    lookup_url_kwarg = "pk"
    http_method_names = ["get", "patch", "head", "options"]
