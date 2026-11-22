"""Tests for the profile detail endpoint."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import authenticate, create_user


class ProfileDetailTests(APITestCase):
    """Tests for GET and PATCH /api/profile/<pk>/."""

    def setUp(self):
        self.owner = create_user("owner", "business")
        self.other = create_user("other", "customer")
        self.url = reverse("profile-detail", kwargs={"pk": self.owner.id})

    def test_get_success(self):
        authenticate(self.client, self.other)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "owner")
        self.assertEqual(response.data["type"], "business")

    def test_get_empty_fields_are_strings(self):
        authenticate(self.client, self.owner)
        response = self.client.get(self.url)
        for field in ["first_name", "last_name", "location", "tel"]:
            self.assertEqual(response.data[field], "")
        self.assertEqual(response.data["description"], "")
        self.assertEqual(response.data["working_hours"], "")

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_not_found(self):
        authenticate(self.client, self.owner)
        url = reverse("profile-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile(self):
        authenticate(self.client, self.owner)
        data = {"first_name": "Max", "email": "new@mail.de"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Max")
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.email, "new@mail.de")

    def test_patch_foreign_profile(self):
        authenticate(self.client, self.other)
        response = self.client.patch(
            self.url, {"first_name": "Hack"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated(self):
        response = self.client.patch(
            self.url, {"first_name": "Max"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_duplicate_email(self):
        authenticate(self.client, self.owner)
        data = {"email": self.other.email}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_keeps_own_email(self):
        authenticate(self.client, self.owner)
        data = {"email": self.owner.email}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_not_allowed(self):
        authenticate(self.client, self.owner)
        response = self.client.put(self.url, {}, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
