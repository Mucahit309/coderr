"""Serializers for the offer endpoints."""

from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Id and relative link of an offer detail."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """Return the relative url of the offer detail."""
        return f"/offerdetails/{obj.id}/"


class OfferListSerializer(serializers.ModelSerializer):
    """Offer overview with min price and min delivery time."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
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
        ]

    def get_user_details(self, obj):
        """Return name data of the offer creator."""
        profile = obj.user.profile
        return {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "username": obj.user.username,
        }
