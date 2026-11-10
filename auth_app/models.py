"""Models for the auth_app."""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Stores the account type of a user."""

    CUSTOMER = "customer"
    BUSINESS = "business"
    TYPE_CHOICES = [
        (CUSTOMER, "Customer"),
        (BUSINESS, "Business"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.type})"
