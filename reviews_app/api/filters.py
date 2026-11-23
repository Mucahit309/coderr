"""Filters for the review endpoints."""

import django_filters

from reviews_app.models import Review


class ReviewFilter(django_filters.FilterSet):
    """Filters reviews by business user and reviewer."""

    business_user_id = django_filters.NumberFilter(
        field_name="business_user_id"
    )
    reviewer_id = django_filters.NumberFilter(field_name="reviewer_id")

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]
