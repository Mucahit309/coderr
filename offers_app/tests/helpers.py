"""Helper functions shared by the offers tests."""

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from offers_app.models import Offer, OfferDetail
from profile_app.models import UserProfile

OFFER_TYPES = ["basic", "standard", "premium"]


def create_user(name, account_type):
    """Create a user with a profile."""
    user = User.objects.create_user(name, f"{name}@mail.de", "pw12345")
    UserProfile.objects.create(user=user, type=account_type)
    return user


def authenticate(client, user):
    """Authenticate the test client with the token of the user."""
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


def create_offer(
    user, title="Design Package", prices=(100, 200, 500), days=(5, 7, 10)
):
    """Create an offer with its three details."""
    offer = Offer.objects.create(
        user=user, title=title, description="Professional design offer"
    )
    for offer_type, price, day in zip(OFFER_TYPES, prices, days):
        OfferDetail.objects.create(
            offer=offer,
            title=f"{offer_type} design",
            revisions=2,
            delivery_time_in_days=day,
            price=price,
            features=["Logo Design"],
            offer_type=offer_type,
        )
    return offer
