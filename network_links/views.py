from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView,
                                     UpdateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     ListAPIView)

from .filters import NetworkLinkFilter
from .models import NetworkLink
from .paginators import NetworkLinksPagination
from .permissions import IsActiveEmployeePermission
from .serializers import NetworkLinkSerializer


class NetworkLinkCreateAPIView(CreateAPIView):
    """View for create network link and related models."""

    serializer_class = NetworkLinkSerializer


class NetworkLinkReadAPIView(RetrieveAPIView):
    """View for read network link and related models."""

    serializer_class = NetworkLinkSerializer
    queryset = NetworkLink.objects.all()
    permission_classes = [IsActiveEmployeePermission]


class NetworkLinkUpdateAPIView(UpdateAPIView):
    """View for update network link and related models."""

    serializer_class = NetworkLinkSerializer
    queryset = NetworkLink.objects.all()
    permission_classes = [IsActiveEmployeePermission]


class NetworkLinkDeleteAPIView(DestroyAPIView):
    """View for delete network link and related models."""

    queryset = NetworkLink.objects.all()
    permission_classes = [IsActiveEmployeePermission]


class NetworkLinkListAPIView(ListAPIView):
    """View for list network links."""

    serializer_class = NetworkLinkSerializer
    queryset = NetworkLink.objects.all().order_by('id')
    permission_classes = [IsActiveEmployeePermission]
    pagination_class = NetworkLinksPagination
    filter_backends =[DjangoFilterBackend]
    filterset_class = NetworkLinkFilter
