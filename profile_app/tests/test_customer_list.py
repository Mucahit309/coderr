"""Tests for the customer profiles list endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_user


class CustomerProfileListTests(APITestCase):
    """Tests for GET /api/profiles/customer/."""

    def setUp(self):
        self.business = create_user("shop", "business")
        self.customer = create_user("buyer", "customer")
        self.url = reverse("customer-list")

    def test_list_only_customers(self):
        authenticate(self.client, self.business)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], "customer")

    def test_list_fields(self):
        authenticate(self.client, self.business)
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.data[0]),
            [
                "user",
                "username",
                "first_name",
                "last_name",
                "file",
                "uploaded_at",
                "type",
            ],
        )

    def test_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
