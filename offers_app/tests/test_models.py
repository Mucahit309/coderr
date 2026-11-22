"""Tests for the offer models."""

from django.db import IntegrityError
from django.test import TestCase

from offers_app.models import OfferDetail

from .helpers import create_offer, create_user


class OfferModelTests(TestCase):
    """Tests for Offer and OfferDetail."""

    def setUp(self):
        self.user = create_user("shop", "business")

    def test_offer_str(self):
        offer = create_offer(self.user, title="Logo")
        self.assertEqual(str(offer), "Logo")

    def test_detail_str(self):
        offer = create_offer(self.user)
        self.assertEqual(str(offer.details.first()), "basic design (basic)")

    def test_offer_type_is_unique_per_offer(self):
        offer = create_offer(self.user)
        with self.assertRaises(IntegrityError):
            OfferDetail.objects.create(
                offer=offer,
                title="Duplicate",
                revisions=1,
                delivery_time_in_days=1,
                price=1,
                offer_type="basic",
            )
