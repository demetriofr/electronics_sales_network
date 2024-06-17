from django_filters import FilterSet, CharFilter

from .models import NetworkLink


class NetworkLinkFilter(FilterSet):
    """Filter for NetworkLink model."""

    country = CharFilter(field_name='contact_info__country')

    class Meta:
        model = NetworkLink
        fields = []  # leave it blank because we are using a related field
