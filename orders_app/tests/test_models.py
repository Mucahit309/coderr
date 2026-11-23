"""Tests for the Order model."""

from django.test import TestCase

from offers_app.tests.helpers import create_user
from orders_app.models import Order

from .helpers import create_order


class OrderModelTests(TestCase):
    """Tests for the Order model."""

    def setUp(self):
        self.order = create_order(
            create_user("buyer", "customer"),
            create_user("shop", "business"),
        )

    def test_str(self):
        self.assertEqual(str(self.order), "Logo Design (in_progress)")

    def test_default_status(self):
        self.assertEqual(self.order.status, Order.IN_PROGRESS)
