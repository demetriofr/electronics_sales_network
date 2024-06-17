from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from .models import Product
from .paginators import ProductsPagination
from .permissions import IsActiveEmployeePermission
from .serializers import ProductSerializer
from .filters import ProductFilter


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission]
    pagination_class = ProductsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

