"""Tests for the registration and login endpoints."""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import UserProfile


class RegistrationTests(APITestCase):
    """Tests for POST /api/registration/."""

    def setUp(self):
        self.url = reverse("registration")
        self.data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def post(self, data=None):
        """Send the registration request."""
        return self.client.post(self.url, data or self.data, format="json")

    def test_registration_success(self):
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data), {"token", "username", "email", "user_id"}
        )

    def test_registration_creates_profile(self):
        self.post()
        user = User.objects.get(username="exampleUsername")
        self.assertEqual(user.profile.type, "customer")

    def test_passwords_do_not_match(self):
        self.data["repeated_password"] = "otherPassword"
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        User.objects.create_user("other", self.data["email"], "pw12345")
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_type(self):
        self.data["type"] = "admin"
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_username(self):
        del self.data["username"]
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """Tests for POST /api/login/."""

    def setUp(self):
        self.url = reverse("login")
        self.user = User.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
        )

    def test_login_success(self):
        data = {"username": "exampleUsername", "password": "examplePassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertIn("token", response.data)

    def test_login_wrong_password(self):
        data = {"username": "exampleUsername", "password": "wrong"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_data(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileModelTests(APITestCase):
    """Tests for the UserProfile model."""

    def test_str(self):
        user = User.objects.create_user("max", "max@mail.de", "pw12345")
        profile = UserProfile.objects.create(user=user, type="business")
        self.assertEqual(str(profile), "max (business)")
