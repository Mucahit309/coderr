"""Helper functions shared by the reviews tests."""

from reviews_app.models import Review


def create_review(reviewer, business_user, rating=4, text="Great work!"):
    """Create a review of a business user."""
    return Review.objects.create(
        reviewer=reviewer,
        business_user=business_user,
        rating=rating,
        description=text,
    )
