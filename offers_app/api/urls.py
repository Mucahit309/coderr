"""URL routes of the offers_app."""

from django.urls import path

from .views import (
    OfferDetailView,
    OfferListCreateView,
    SingleOfferDetailView,
)

urlpatterns = [
    path("offers/", OfferListCreateView.as_view(), name="offer-list"),
    path(
        "offers/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail",
    ),
    path(
        "offerdetails/<int:pk>/",
        SingleOfferDetailView.as_view(),
        name="offer-detail-item",
    ),
]
