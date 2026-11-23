"""Tests for the base info endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import create_offer, create_user
from reviews_app.tests.helpers import create_review


class BaseInfoTests(APITestCase):
    """Tests for GET /api/base-info/."""

    def setUp(self):
        self.shop = create_user("shop", "business")
        self.studio = create_user("studio", "business")
        create_offer(self.shop)
        create_offer(self.studio)
        for index, rating in enumerate([4, 5, 5]):
            customer = create_user(f"buyer{index}", "customer")
            create_review(customer, self.shop, rating=rating)
        self.url = reverse("base-info")

    def test_base_info_is_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_info_fields(self):
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.data),
            [
                "review_count",
                "average_rating",
                "business_profile_count",
                "offer_count",
            ],
        )

    def test_base_info_counts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["review_count"], 3)
        self.assertEqual(response.data["business_profile_count"], 2)
        self.assertEqual(response.data["offer_count"], 2)

    def test_average_rating_is_rounded(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["average_rating"], 4.7)

    def test_invalid_token_is_ignored(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BaseInfoEmptyTests(APITestCase):
    """Tests for GET /api/base-info/ on an empty platform."""

    def test_empty_platform(self):
        response = self.client.get(reverse("base-info"))
        self.assertEqual(
            response.data,
            {
                "review_count": 0,
                "average_rating": 0.0,
                "business_profile_count": 0,
                "offer_count": 0,
            },
        )
