"""Tests for the Review model."""

from django.db import IntegrityError
from django.test import TestCase

from offers_app.tests.helpers import create_user

from .helpers import create_review


class ReviewModelTests(TestCase):
    """Tests for the Review model."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.business = create_user("shop", "business")
        self.review = create_review(self.customer, self.business)

    def test_str(self):
        self.assertEqual(str(self.review), "buyer -> shop (4/5)")

    def test_one_review_per_business_user(self):
        with self.assertRaises(IntegrityError):
            create_review(self.customer, self.business, rating=5)
