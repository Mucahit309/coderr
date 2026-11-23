"""URL routes of the reviews_app."""

from django.urls import path

from .views import ReviewListView

urlpatterns = [
    path("reviews/", ReviewListView.as_view(), name="review-list"),
]
