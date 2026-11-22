"""Tests for the offer delete endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail

from .helpers import authenticate, create_offer, create_user


class OfferDeleteTests(APITestCase):
    """Tests for DELETE /api/offers/<id>/."""

    def setUp(self):
        self.owner = create_user("shop", "business")
        self.other = create_user("studio", "business")
        self.offer = create_offer(self.owner)
        self.url = reverse("offer-detail", kwargs={"pk": self.offer.id})

    def test_delete_success(self):
        authenticate(self.client, self.owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.exists())

    def test_delete_removes_details(self):
        authenticate(self.client, self.owner)
        self.client.delete(self.url)
        self.assertFalse(OfferDetail.objects.exists())

    def test_delete_foreign_offer(self):
        authenticate(self.client, self.other)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Offer.objects.exists())

    def test_delete_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_found(self):
        authenticate(self.client, self.owner)
        url = reverse("offer-detail", kwargs={"pk": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
