"""Serializers for the offer endpoints."""

from django.db import transaction
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


class OfferDetailSerializer(serializers.ModelSerializer):
    """Full data of an offer detail."""

    features = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """Creates offers together with their three details."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        """Ensure there is exactly one detail of each offer type."""
        types = sorted(detail["offer_type"] for detail in value)
        if types != ["basic", "premium", "standard"]:
            raise serializers.ValidationError(
                "An offer needs exactly one basic, standard and "
                "premium detail."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Create the offer and its details."""
        details = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)
        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **detail) for detail in details]
        )
        return offer


class OfferDetailAbsoluteLinkSerializer(OfferDetailLinkSerializer):
    """Id and absolute link of an offer detail."""

    def get_url(self, obj):
        """Return the absolute url of the offer detail."""
        path = f"/api/offerdetails/{obj.id}/"
        return self.context["request"].build_absolute_uri(path)


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Single offer with min price and min delivery time."""

    details = OfferDetailAbsoluteLinkSerializer(many=True, read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

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
        ]
