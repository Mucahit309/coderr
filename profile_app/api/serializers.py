"""Serializers for the profile endpoints."""

from django.contrib.auth.models import User
from rest_framework import serializers

from profile_app.models import UserProfile


class ProfileListSerializer(serializers.ModelSerializer):
    """Profile data without private fields, used for lists."""

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]
        read_only_fields = ["type"]


class ProfileSerializer(ProfileListSerializer):
    """Full profile data including email and creation date."""

    email = serializers.EmailField(source="user.email")

    class Meta(ProfileListSerializer.Meta):
        fields = ProfileListSerializer.Meta.fields + [
            "email",
            "created_at",
        ]
        read_only_fields = ["type", "created_at"]

    def validate_email(self, value):
        """Ensure the email is not used by another user."""
        users = User.objects.filter(email__iexact=value)
        if users.exclude(pk=self.instance.user_id).exists():
            raise serializers.ValidationError(
                "This email is already in use."
            )
        return value

    def update(self, instance, validated_data):
        """Update the profile and the email of the related user."""
        user_data = validated_data.pop("user", {})
        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save(update_fields=["email"])
        return super().update(instance, validated_data)
