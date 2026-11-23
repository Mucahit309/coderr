"""Helper functions shared by the orders tests."""

from orders_app.models import Order


def create_order(customer, business, status=Order.IN_PROGRESS):
    """Create an order between a customer and a business user."""
    return Order.objects.create(
        customer_user=customer,
        business_user=business,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=["Logo Design", "Visitenkarten"],
        offer_type="basic",
        status=status,
    )
