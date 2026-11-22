"""Tests for the business profiles list endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_user


class BusinessProfileListTests(APITestCase):
    """Tests for GET /api/profiles/business/."""

    def setUp(self):
        self.business = create_user("shop", "business")
        self.customer = create_user("buyer", "customer")
        self.url = reverse("business-list")

    def test_list_only_business(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], "business")

    def test_list_has_no_private_fields(self):
        authenticate(self.client, self.customer)
        response = self.client.get(self.url)
        self.assertNotIn("email", response.data[0])
        self.assertNotIn("created_at", response.data[0])

    def test_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
