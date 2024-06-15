from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import ProductsConfig
from .views import ProductViewSet

# app_name = ProductsConfig.name

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
