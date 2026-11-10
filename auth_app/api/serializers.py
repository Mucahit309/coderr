"""Serializers for registration and login."""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """Validates and creates a new user together with its profile."""

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.TYPE_CHOICES, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True, "allow_blank": False},
        }

    def validate_email(self, value):
        """Ensure the email address is not used yet."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already in use."
            )
        return value

    def validate(self, attrs):
        """Ensure both passwords match."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        """Create the user and its profile."""
        validated_data.pop("repeated_password")
        account_type = validated_data.pop("type")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=account_type)
        return user


class LoginSerializer(serializers.Serializer):
    """Validates the login credentials."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate the user and add it to the validated data."""
        user = authenticate(
            username=attrs["username"], password=attrs["password"]
        )
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs
