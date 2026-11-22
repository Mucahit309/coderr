"""Custom permissions for the offers_app."""

from rest_framework.permissions import BasePermission

from profile_app.models import UserProfile


class IsBusinessUser(BasePermission):
    """Allows access only to users with a business profile."""

    def has_permission(self, request, view):
        """Check that the user has a business profile."""
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.type == UserProfile.BUSINESS)
