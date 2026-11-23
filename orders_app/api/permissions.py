"""Custom permissions for the orders_app."""

from rest_framework.permissions import BasePermission

from profile_app.models import UserProfile


def has_profile_type(user, account_type):
    """Return True if the user has a profile of the given type."""
    profile = getattr(user, "profile", None)
    return bool(profile and profile.type == account_type)


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    def has_permission(self, request, view):
        """Check that the user is a customer."""
        return has_profile_type(request.user, UserProfile.CUSTOMER)
