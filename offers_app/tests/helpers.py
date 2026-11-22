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


def detail_payload(offer_type, price=100, days=5):
    """Return the request data of one offer detail."""
    return {
        "title": f"{offer_type.title()} Design",
        "revisions": 2,
        "delivery_time_in_days": days,
        "price": price,
        "features": ["Logo Design", "Visitenkarte"],
        "offer_type": offer_type,
    }


def offer_payload():
    """Return a valid request body to create an offer."""
    return {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket.",
        "details": [
            detail_payload("basic", 100, 5),
            detail_payload("standard", 200, 7),
            detail_payload("premium", 500, 10),
        ],
    }
