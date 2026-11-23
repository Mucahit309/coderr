"""Serializers for the review endpoints."""

from rest_framework import serializers

from profile_app.models import UserProfile
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Full review data, used for reading and creating."""

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["reviewer", "created_at", "updated_at"]

    def validate_business_user(self, value):
        """Ensure the reviewed user is a business user."""
        profile = getattr(value, "profile", None)
        if profile is None or profile.type != UserProfile.BUSINESS:
            raise serializers.ValidationError(
                "The reviewed user must be a business user."
            )
        return value


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Updates only rating and description of a review."""

    class Meta:
        model = Review
        fields = ["rating", "description"]

    def to_representation(self, instance):
        """Return the updated review in the full review format."""
        return ReviewSerializer(instance, context=self.context).data
