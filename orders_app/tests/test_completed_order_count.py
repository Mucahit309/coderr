"""Tests for the completed order count endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user

from .helpers import create_order


class CompletedOrderCountTests(APITestCase):
    """Tests for GET /api/completed-order-count/<business_user_id>/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.business = create_user("shop", "business")
        create_order(self.customer, self.business)
        create_order(self.customer, self.business, status="completed")
        create_order(self.customer, self.business, status="completed")
        create_order(self.customer, self.business, status="cancelled")
        self.url = self.build_url(self.business.id)

    def build_url(self, user_id):
        """Return the url for the given business user id."""
        return reverse(
            "completed-order-count", kwargs={"business_user_id": user_id}
        )

    def test_count_completed_orders(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"completed_order_count": 2})

    def test_count_without_completed_orders(self):
        empty = create_user("empty", "business")
        authenticate(self.client, self.customer)
        response = self.client.get(self.build_url(empty.id))
        self.assertEqual(response.data, {"completed_order_count": 0})

    def test_count_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_count_unknown_user(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.build_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_count_for_customer_id(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.build_url(self.customer.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
