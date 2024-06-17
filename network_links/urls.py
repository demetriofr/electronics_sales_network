from django.urls import path

from .apps import NetworkLinksConfig
from .views import (NetworkLinkCreateAPIView,
                    NetworkLinkReadAPIView,
                    NetworkLinkUpdateAPIView,
                    NetworkLinkDeleteAPIView,
                    NetworkLinkListAPIView)

app_name = NetworkLinksConfig.name

urlpatterns = [
    path('', NetworkLinkCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', NetworkLinkReadAPIView.as_view(), name='read'),
    path('<int:pk>/update/', NetworkLinkUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', NetworkLinkDeleteAPIView.as_view(), name='delete'),
    path('list/', NetworkLinkListAPIView.as_view(), name='list'),
]
