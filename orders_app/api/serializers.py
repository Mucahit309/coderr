"""Serializers for the order endpoints."""

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Full order data, used for reading."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order from an offer detail."""

    offer_detail_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        """Create the order as a copy of the chosen offer detail."""
        detail = get_object_or_404(
            OfferDetail.objects.select_related("offer"),
            pk=validated_data["offer_detail_id"],
        )
        return Order.objects.create(
            customer_user=self.context["request"].user,
            **self.build_order_data(detail),
        )

    def build_order_data(self, detail):
        """Return the order fields copied from the offer detail."""
        return {
            "business_user": detail.offer.user,
            "title": detail.title,
            "revisions": detail.revisions,
            "delivery_time_in_days": detail.delivery_time_in_days,
            "price": detail.price,
            "features": detail.features,
            "offer_type": detail.offer_type,
        }

    def to_representation(self, instance):
        """Return the created order in the full order format."""
        return OrderSerializer(instance, context=self.context).data


class OrderStatusSerializer(serializers.ModelSerializer):
    """Updates only the status of an order."""

    class Meta:
        model = Order
        fields = ["status"]

    def validate(self, attrs):
        """Ensure the request contains only a status."""
        extra_fields = set(self.initial_data) - {"status"}
        if extra_fields or "status" not in attrs:
            raise serializers.ValidationError(
                "Only the field 'status' can be updated."
            )
        return attrs

    def to_representation(self, instance):
        """Return the updated order in the full order format."""
        return OrderSerializer(instance, context=self.context).data
