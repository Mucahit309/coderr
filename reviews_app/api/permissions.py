"""Custom permissions for the reviews_app."""

from rest_framework.permissions import BasePermission

from profile_app.models import UserProfile


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    def has_permission(self, request, view):
        """Check that the user is a customer."""
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.type == UserProfile.CUSTOMER)
