"""Tests for the order update endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user

from .helpers import create_order


class OrderUpdateTests(APITestCase):
    """Tests for PATCH /api/orders/<id>/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.business = create_user("shop", "business")
        self.other_business = create_user("studio", "business")
        self.order = create_order(self.customer, self.business)
        self.url = reverse("order-detail", kwargs={"pk": self.order.id})

    def patch(self, data):
        """Send the update request."""
        return self.client.patch(self.url, data, format="json")

    def test_patch_status(self):
        authenticate(self.client, self.business)
        response = self.patch({"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_patch_returns_full_order(self):
        authenticate(self.client, self.business)
        response = self.patch({"status": "cancelled"})
        self.assertEqual(response.data["id"], self.order.id)
        self.assertEqual(response.data["title"], "Logo Design")

    def test_patch_invalid_status(self):
        authenticate(self.client, self.business)
        response = self.patch({"status": "done"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_with_extra_fields(self):
        authenticate(self.client, self.business)
        response = self.patch({"status": "completed", "price": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_without_status(self):
        authenticate(self.client, self.business)
        response = self.patch({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_as_customer(self):
        authenticate(self.client, self.customer)
        response = self.patch({"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_as_other_business(self):
        authenticate(self.client, self.other_business)
        response = self.patch({"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated(self):
        response = self.patch({"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_not_found(self):
        authenticate(self.client, self.business)
        url = reverse("order-detail", kwargs={"pk": 9999})
        response = self.client.patch(
            url, {"status": "completed"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
