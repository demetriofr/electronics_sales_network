from rest_framework.pagination import PageNumberPagination


class ProductsPagination(PageNumberPagination):
    """Pagination class for products."""

    page_size = 10
    page_size_query_param = 'page_size'
