"""Custom permissions for the profile_app."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwner(BasePermission):
    """Allows read access to all, write access only to the owner."""

    def has_object_permission(self, request, view, obj):
        """Check that only the owner may change a profile."""
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
