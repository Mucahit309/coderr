"""Tests for the review list endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user

from .helpers import create_review


class ReviewListTests(APITestCase):
    """Tests for GET /api/reviews/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.other_customer = create_user("other", "customer")
        self.shop = create_user("shop", "business")
        self.studio = create_user("studio", "business")
        create_review(self.customer, self.shop, rating=4)
        create_review(self.customer, self.studio, rating=5)
        create_review(self.other_customer, self.shop, rating=3)
        self.url = reverse("review-list")
        authenticate(self.client, self.customer)

    def get_ratings(self, params=None):
        """Return the ratings of the reviews for the given query."""
        response = self.client.get(self.url, params)
        return [review["rating"] for review in response.data]

    def test_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_is_plain_list(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.data, list)

    def test_review_fields(self):
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.data[0]),
            [
                "id",
                "business_user",
                "reviewer",
                "rating",
                "description",
                "created_at",
                "updated_at",
            ],
        )

    def test_filter_business_user_id(self):
        ratings = self.get_ratings({"business_user_id": self.shop.id})
        self.assertCountEqual(ratings, [4, 3])

    def test_filter_reviewer_id(self):
        ratings = self.get_ratings({"reviewer_id": self.customer.id})
        self.assertCountEqual(ratings, [4, 5])

    def test_ordering_by_rating(self):
        self.assertEqual(self.get_ratings({"ordering": "rating"}), [3, 4, 5])

    def test_ordering_by_rating_descending(self):
        self.assertEqual(self.get_ratings({"ordering": "-rating"}), [5, 4, 3])

    def test_invalid_filter_value(self):
        response = self.client.get(self.url, {"reviewer_id": "abc"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
