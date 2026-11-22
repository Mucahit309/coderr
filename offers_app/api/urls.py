"""URL routes of the offers_app."""

from django.urls import path

from .views import OfferDetailView, OfferListCreateView

urlpatterns = [
    path("offers/", OfferListCreateView.as_view(), name="offer-list"),
    path(
        "offers/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail",
    ),
]
