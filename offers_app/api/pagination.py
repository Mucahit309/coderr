"""Pagination for the offer endpoints."""

from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Page number pagination with a client-controlled page size."""

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100
