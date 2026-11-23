"""Tests for the review delete endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user
from reviews_app.models import Review

from .helpers import create_review


class ReviewDeleteTests(APITestCase):
    """Tests for DELETE /api/reviews/<id>/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.other_customer = create_user("other", "customer")
        self.business = create_user("shop", "business")
        self.review = create_review(self.customer, self.business)
        self.url = reverse("review-detail", kwargs={"pk": self.review.id})

    def test_delete_success(self):
        authenticate(self.client, self.customer)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.exists())

    def test_delete_foreign_review(self):
        authenticate(self.client, self.other_customer)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.exists())

    def test_delete_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_found(self):
        authenticate(self.client, self.customer)
        url = reverse("review-detail", kwargs={"pk": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_again_after_delete(self):
        authenticate(self.client, self.customer)
        self.client.delete(self.url)
        data = {"business_user": self.business.id, "rating": 5}
        response = self.client.post(
            reverse("review-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
