"""Views for registration and login."""

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer


def build_auth_data(user):
    """Return token and user info for a successful authentication."""
    token, _ = Token.objects.get_or_create(user=user)
    return {
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
    }


class RegistrationView(APIView):
    """Creates a new customer or business user."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Register a user and return token and user info."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            build_auth_data(user), status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """Authenticates a user and returns a token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Log in a user and return token and user info."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(build_auth_data(user), status=status.HTTP_200_OK)
