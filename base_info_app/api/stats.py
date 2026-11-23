"""Aggregations for the base info endpoint."""

from django.db.models import Avg

from offers_app.models import Offer
from profile_app.models import UserProfile
from reviews_app.models import Review


def get_average_rating():
    """Return the average rating rounded to one decimal place."""
    average = Review.objects.aggregate(average=Avg("rating"))["average"]
    return round(average, 1) if average is not None else 0.0


def build_base_info():
    """Return the statistics of the platform."""
    business_profiles = UserProfile.objects.filter(
        type=UserProfile.BUSINESS
    )
    return {
        "review_count": Review.objects.count(),
        "average_rating": get_average_rating(),
        "business_profile_count": business_profiles.count(),
        "offer_count": Offer.objects.count(),
    }
