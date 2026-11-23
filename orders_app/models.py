"""Models for the orders_app."""

from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    """An order a customer placed for an offer detail."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_orders"
    )
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_orders"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"
