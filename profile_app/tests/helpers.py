"""Helper functions shared by the profile tests."""

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from profile_app.models import UserProfile


def create_user(name, account_type):
    """Create a user with a profile."""
    user = User.objects.create_user(name, f"{name}@mail.de", "pw12345")
    UserProfile.objects.create(user=user, type=account_type)
    return user


def authenticate(client, user):
    """Authenticate the test client with the token of the user."""
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
