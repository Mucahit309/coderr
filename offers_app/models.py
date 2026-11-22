"""Models for the offers_app."""

from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """An offer created by a business user."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.FileField(
        upload_to="offer_images/", null=True, blank=True
    )
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """One package (basic, standard or premium) of an offer."""

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    TYPE_CHOICES = [
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (PREMIUM, "Premium"),
    ]

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Offer detail"
        verbose_name_plural = "Offer details"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "offer_type"],
                name="unique_offer_type_per_offer",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.offer_type})"
