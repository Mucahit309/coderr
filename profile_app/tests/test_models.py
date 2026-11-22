"""Tests for the UserProfile model."""

from django.contrib.auth.models import User
from django.test import TestCase

from profile_app.models import UserProfile


class UserProfileModelTests(TestCase):
    """Tests for the UserProfile model."""

    def test_str(self):
        user = User.objects.create_user("max", "max@mail.de", "pw12345")
        profile = UserProfile.objects.create(user=user, type="business")
        self.assertEqual(str(profile), "max (business)")

    def test_text_fields_default_to_empty_string(self):
        user = User.objects.create_user("eva", "eva@mail.de", "pw12345")
        profile = UserProfile.objects.create(user=user, type="customer")
        self.assertEqual(profile.first_name, "")
        self.assertEqual(profile.tel, "")
        self.assertEqual(profile.working_hours, "")
