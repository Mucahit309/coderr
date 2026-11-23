"""Admin configuration for the orders_app."""

from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Shows orders in the admin interface."""

    list_display = ["id", "title", "customer_user", "business_user", "status"]
    list_filter = ["status"]
    search_fields = ["title", "customer_user__username"]
