"""Tests for the offer update endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_offer, create_user


class OfferUpdateTests(APITestCase):
    """Tests for PATCH /api/offers/<id>/."""

    def setUp(self):
        self.owner = create_user("shop", "business")
        self.other = create_user("studio", "business")
        self.offer = create_offer(self.owner)
        self.url = reverse("offer-detail", kwargs={"pk": self.offer.id})

    def patch(self, data):
        """Send the update request."""
        return self.client.patch(self.url, data, format="json")

    def test_patch_title(self):
        authenticate(self.client, self.owner)
        response = self.patch({"title": "New title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New title")
        self.assertEqual(len(response.data["details"]), 3)

    def test_patch_response_fields(self):
        authenticate(self.client, self.owner)
        response = self.patch({"title": "New title"})
        self.assertEqual(
            list(response.data),
            ["id", "title", "image", "description", "details"],
        )

    def test_patch_single_detail(self):
        authenticate(self.client, self.owner)
        data = {"details": [{"offer_type": "basic", "price": 120}]}
        response = self.patch(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [detail["price"] for detail in response.data["details"]]
        self.assertEqual(prices, [120, 200, 500])

    def test_patch_keeps_detail_ids(self):
        authenticate(self.client, self.owner)
        ids = list(self.offer.details.values_list("id", flat=True))
        data = {"details": [{"offer_type": "standard", "title": "Neu"}]}
        response = self.patch(data)
        new_ids = [detail["id"] for detail in response.data["details"]]
        self.assertEqual(new_ids, ids)

    def test_patch_detail_without_type(self):
        authenticate(self.client, self.owner)
        response = self.patch({"details": [{"price": 120}]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_duplicate_types(self):
        authenticate(self.client, self.owner)
        details = [
            {"offer_type": "basic", "price": 120},
            {"offer_type": "basic", "price": 130},
        ]
        response = self.patch({"details": details})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_invalid_price(self):
        authenticate(self.client, self.owner)
        data = {"details": [{"offer_type": "basic", "price": -5}]}
        response = self.patch(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_foreign_offer(self):
        authenticate(self.client, self.other)
        response = self.patch({"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated(self):
        response = self.patch({"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_not_found(self):
        authenticate(self.client, self.owner)
        url = reverse("offer-detail", kwargs={"pk": 9999})
        response = self.client.patch(url, {"title": "X"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
