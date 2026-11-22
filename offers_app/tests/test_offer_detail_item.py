"""Tests for the offer detail item endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_offer, create_user


class OfferDetailItemTests(APITestCase):
    """Tests for GET /api/offerdetails/<id>/."""

    def setUp(self):
        self.user = create_user("buyer", "customer")
        offer = create_offer(create_user("shop", "business"))
        self.detail = offer.details.first()
        self.url = reverse(
            "offer-detail-item", kwargs={"pk": self.detail.id}
        )

    def test_retrieve_success(self):
        authenticate(self.client, self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            list(response.data),
            [
                "id",
                "title",
                "revisions",
                "delivery_time_in_days",
                "price",
                "features",
                "offer_type",
            ],
        )

    def test_retrieve_values(self):
        authenticate(self.client, self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["offer_type"], "basic")
        self.assertEqual(response.data["price"], 100)
        self.assertEqual(response.data["features"], ["Logo Design"])

    def test_retrieve_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_found(self):
        authenticate(self.client, self.user)
        url = reverse("offer-detail-item", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
