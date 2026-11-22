"""Tests for the offer retrieve endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_offer, create_user


class OfferRetrieveTests(APITestCase):
    """Tests for GET /api/offers/<id>/."""

    def setUp(self):
        self.owner = create_user("shop", "business")
        self.offer = create_offer(self.owner)
        self.url = reverse("offer-detail", kwargs={"pk": self.offer.id})

    def test_retrieve_success(self):
        authenticate(self.client, self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            list(response.data),
            [
                "id",
                "user",
                "title",
                "image",
                "description",
                "created_at",
                "updated_at",
                "details",
                "min_price",
                "min_delivery_time",
            ],
        )

    def test_retrieve_values(self):
        authenticate(self.client, self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.data["user"], self.owner.id)
        self.assertEqual(response.data["min_price"], 100)
        self.assertEqual(response.data["min_delivery_time"], 5)

    def test_detail_links_are_absolute(self):
        authenticate(self.client, self.owner)
        response = self.client.get(self.url)
        detail = response.data["details"][0]
        self.assertEqual(
            detail["url"],
            f"http://testserver/api/offerdetails/{detail['id']}/",
        )

    def test_retrieve_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_not_found(self):
        authenticate(self.client, self.owner)
        url = reverse("offer-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
