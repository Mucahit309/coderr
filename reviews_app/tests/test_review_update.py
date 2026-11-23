"""Tests for the review update endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user

from .helpers import create_review


class ReviewUpdateTests(APITestCase):
    """Tests for PATCH /api/reviews/<id>/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.other_customer = create_user("other", "customer")
        self.business = create_user("shop", "business")
        self.review = create_review(self.customer, self.business)
        self.url = reverse("review-detail", kwargs={"pk": self.review.id})

    def patch(self, data):
        """Send the update request."""
        return self.client.patch(self.url, data, format="json")

    def test_patch_success(self):
        authenticate(self.client, self.customer)
        data = {"rating": 5, "description": "Noch besser!"}
        response = self.patch(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Noch besser!")

    def test_patch_returns_full_review(self):
        authenticate(self.client, self.customer)
        response = self.patch({"rating": 5})
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

    def test_patch_only_rating(self):
        authenticate(self.client, self.customer)
        response = self.patch({"rating": 2})
        self.assertEqual(response.data["rating"], 2)
        self.assertEqual(response.data["description"], "Great work!")

    def test_patch_ignores_other_fields(self):
        authenticate(self.client, self.customer)
        other_business = create_user("studio", "business")
        response = self.patch({"business_user": other_business.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.business_user, self.business)

    def test_patch_invalid_rating(self):
        authenticate(self.client, self.customer)
        response = self.patch({"rating": 6})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_foreign_review(self):
        authenticate(self.client, self.other_customer)
        response = self.patch({"rating": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated(self):
        response = self.patch({"rating": 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_not_found(self):
        authenticate(self.client, self.customer)
        url = reverse("review-detail", kwargs={"pk": 9999})
        response = self.client.patch(url, {"rating": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
