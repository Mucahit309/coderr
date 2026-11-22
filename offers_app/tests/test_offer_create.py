"""Tests for the offer create endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer

from .helpers import authenticate, create_user, offer_payload


class OfferCreateTests(APITestCase):
    """Tests for POST /api/offers/."""

    def setUp(self):
        self.business = create_user("shop", "business")
        self.customer = create_user("buyer", "customer")
        self.url = reverse("offer-list")

    def post(self, data):
        """Send the create request."""
        return self.client.post(self.url, data, format="json")

    def test_create_success(self):
        authenticate(self.client, self.business)
        response = self.post(offer_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            list(response.data),
            ["id", "title", "image", "description", "details"],
        )
        self.assertEqual(len(response.data["details"]), 3)

    def test_create_sets_creator(self):
        authenticate(self.client, self.business)
        self.post(offer_payload())
        self.assertEqual(Offer.objects.get().user, self.business)

    def test_create_as_customer(self):
        authenticate(self.client, self.customer)
        response = self.post(offer_payload())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_unauthenticated(self):
        response = self.post(offer_payload())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_two_details(self):
        authenticate(self.client, self.business)
        data = offer_payload()
        data["details"].pop()
        response = self.post(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_duplicate_type(self):
        authenticate(self.client, self.business)
        data = offer_payload()
        data["details"][2]["offer_type"] = "basic"
        response = self.post(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_title(self):
        authenticate(self.client, self.business)
        data = offer_payload()
        del data["title"]
        response = self.post(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
