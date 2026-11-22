"""Tests for the offer list endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import create_offer, create_user


class OfferListTests(APITestCase):
    """Tests for GET /api/offers/."""

    def setUp(self):
        self.owner = create_user("shop", "business")
        self.other = create_user("studio", "business")
        create_offer(self.owner, title="Website Design")
        create_offer(
            self.other,
            title="Logo Package",
            prices=(300, 400, 500),
            days=(8, 9, 10),
        )
        self.url = reverse("offer-list")

    def get_titles(self, params=None):
        """Return the titles of the offers for the given query."""
        response = self.client.get(self.url, params)
        return [offer["title"] for offer in response.data["results"]]

    def test_list_is_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_is_paginated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(
            set(response.data), {"count", "next", "previous", "results"}
        )

    def test_offer_fields(self):
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.data["results"][0]),
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
                "user_details",
            ],
        )

    def test_min_price_and_delivery_time(self):
        response = self.client.get(self.url, {"creator_id": self.owner.id})
        offer = response.data["results"][0]
        self.assertEqual(offer["min_price"], 100)
        self.assertEqual(offer["min_delivery_time"], 5)

    def test_detail_links(self):
        response = self.client.get(self.url, {"creator_id": self.owner.id})
        details = response.data["results"][0]["details"]
        self.assertEqual(len(details), 3)
        self.assertEqual(
            details[0]["url"], f"/offerdetails/{details[0]['id']}/"
        )

    def test_user_details(self):
        response = self.client.get(self.url, {"creator_id": self.owner.id})
        self.assertEqual(
            response.data["results"][0]["user_details"],
            {"first_name": "", "last_name": "", "username": "shop"},
        )

    def test_filter_creator_id(self):
        titles = self.get_titles({"creator_id": self.owner.id})
        self.assertEqual(titles, ["Website Design"])

    def test_filter_min_price(self):
        self.assertEqual(self.get_titles({"min_price": 200}), ["Logo Package"])

    def test_filter_max_delivery_time(self):
        titles = self.get_titles({"max_delivery_time": 6})
        self.assertEqual(titles, ["Website Design"])

    def test_ordering_by_min_price(self):
        titles = self.get_titles({"ordering": "min_price"})
        self.assertEqual(titles, ["Website Design", "Logo Package"])

    def test_ordering_by_min_price_descending(self):
        titles = self.get_titles({"ordering": "-min_price"})
        self.assertEqual(titles, ["Logo Package", "Website Design"])

    def test_search(self):
        self.assertEqual(self.get_titles({"search": "logo"}), ["Logo Package"])

    def test_page_size(self):
        response = self.client.get(self.url, {"page_size": 1})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["next"])

    def test_invalid_filter_value(self):
        response = self.client.get(self.url, {"min_price": "abc"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
