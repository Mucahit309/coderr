"""Admin configuration for the offers_app."""

from django.contrib import admin

from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """Shows the details inside the offer."""

    model = OfferDetail
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Shows offers in the admin interface."""

    list_display = ["title", "user", "updated_at"]
    search_fields = ["title", "user__username"]
    inlines = [OfferDetailInline]
