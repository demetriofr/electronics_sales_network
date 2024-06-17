from django_filters import FilterSet, CharFilter

from .models import Product


class ProductFilter(FilterSet):
    """Filter for Product model."""

    id = CharFilter(field_name='id', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['id']  # list of fields by which you can filter
