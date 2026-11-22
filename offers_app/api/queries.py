"""Reusable querysets for the offer endpoints."""

from django.db.models import Min

from offers_app.models import Offer


def annotated_offers():
    """Return offers with their min price and min delivery time."""
    return (
        Offer.objects.select_related("user__profile")
        .prefetch_related("details")
        .annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        )
    )
