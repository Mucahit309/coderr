"""Tests for the order list endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.tests.helpers import authenticate, create_user

from .helpers import create_order


class OrderListTests(APITestCase):
    """Tests for GET /api/orders/."""

    def setUp(self):
        self.customer = create_user("buyer", "customer")
        self.stranger = create_user("other", "customer")
        self.business = create_user("shop", "business")
        create_order(self.customer, self.business)
        create_order(self.stranger, self.business)
        self.url = reverse("order-list")

    def test_list_for_customer(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["customer_user"], self.customer.id)

    def test_list_for_business(self):
        authenticate(self.client, self.business)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

    def test_list_excludes_foreign_orders(self):
        uninvolved = create_user("studio", "business")
        authenticate(self.client, uninvolved)
        response = self.client.get(self.url)
        self.assertEqual(response.data, [])

    def test_list_is_plain_list(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertIsInstance(response.data, list)

    def test_order_fields(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.data[0]),
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

    def test_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
