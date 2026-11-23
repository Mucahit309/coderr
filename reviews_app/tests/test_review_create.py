"""Tests for the review create endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user
from reviews_app.models import Review

from .helpers import create_review


class ReviewCreateTests(APITestCase):
    """Tests for POST /api/reviews/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.business = create_user("shop", "business")
        self.url = reverse("review-list")
        self.data = {
            "business_user": self.business.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

    def post(self, data):
        """Send the create request."""
        return self.client.post(self.url, data, format="json")

    def test_create_success(self):
        authenticate(self.client, self.customer)
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            list(response.data),
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

    def test_create_sets_reviewer(self):
        authenticate(self.client, self.customer)
        response = self.post(self.data)
        self.assertEqual(response.data["reviewer"], self.customer.id)
        self.assertEqual(Review.objects.get().reviewer, self.customer)

    def test_create_duplicate_review(self):
        create_review(self.customer, self.business)
        authenticate(self.client, self.customer)
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 1)

    def test_create_as_business(self):
        authenticate(self.client, self.business)
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_unauthenticated(self):
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_without_business_user(self):
        authenticate(self.client, self.customer)
        del self.data["business_user"]
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_for_customer_user(self):
        authenticate(self.client, self.customer)
        self.data["business_user"] = self.customer.id
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_for_unknown_user(self):
        authenticate(self.client, self.customer)
        self.data["business_user"] = 9999
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_rating(self):
        authenticate(self.client, self.customer)
        del self.data["rating"]
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_rating_too_high(self):
        authenticate(self.client, self.customer)
        self.data["rating"] = 6
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_rating_too_low(self):
        authenticate(self.client, self.customer)
        self.data["rating"] = 0
        response = self.post(self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
