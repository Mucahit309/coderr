"""Custom permissions for the offers_app."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from profile_app.models import UserProfile


class IsBusinessUser(BasePermission):
    """Allows access only to users with a business profile."""

    def has_permission(self, request, view):
        """Check that the user has a business profile."""
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.type == UserProfile.BUSINESS)


class IsOfferOwner(BasePermission):
    """Allows read access to all, write access only to the creator."""

    def has_object_permission(self, request, view, obj):
        """Check that only the creator may change an offer."""
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
