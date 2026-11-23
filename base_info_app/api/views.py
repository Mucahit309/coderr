"""Views for the base info endpoint."""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .stats import build_base_info


class BaseInfoView(APIView):
    """Returns general statistics about the platform."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        """Return review, rating, business and offer statistics."""
        return Response(build_base_info())
