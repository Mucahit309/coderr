"""Tests for the order create endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import (
    authenticate,
    create_offer,
    create_user,
)


class OrderCreateTests(APITestCase):
    """Tests for POST /api/orders/."""

    def setUp(self):
        self.business = create_user("shop", "business")
        self.customer = create_user("buyer", "customer")
        self.detail = create_offer(self.business).details.first()
        self.url = reverse("order-list")

    def post(self, data):
        """Send the create request."""
        return self.client.post(self.url, data, format="json")

    def test_create_success(self):
        authenticate(self.client, self.customer)
        response = self.post({"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            list(response.data),
            [
                "id",
                "customer_user",
                "business_user",
                "title",
                "revisions",
                "delivery_time_in_days",
                "price",
                "features",
                "offer_type",
                "status",
                "created_at",
                "updated_at",
            ],
        )

    def test_create_copies_offer_data(self):
        authenticate(self.client, self.customer)
        response = self.post({"offer_detail_id": self.detail.id})
        self.assertEqual(response.data["customer_user"], self.customer.id)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["price"], 100)
        self.assertEqual(response.data["offer_type"], "basic")
        self.assertEqual(response.data["status"], "in_progress")

    def test_create_as_business(self):
        authenticate(self.client, self.business)
        response = self.post({"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_unauthenticated(self):
        response = self.post({"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_without_detail_id(self):
        authenticate(self.client, self.customer)
        response = self.post({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_invalid_detail_id(self):
        authenticate(self.client, self.customer)
        response = self.post({"offer_detail_id": "abc"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_unknown_detail(self):
        authenticate(self.client, self.customer)
        response = self.post({"offer_detail_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
