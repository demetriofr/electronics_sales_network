"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import getenv

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Electronics saves network API",
        default_version="v1",
        description="API for the electronics saves network",
        terms_of_service="https://github.com/demetriofr/self_study_project/blob/main/LICENSE.md",
        contact=openapi.Contact(email=getenv('CSU_EMAIL')),
        license=openapi.License(name="MIT License"),

    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', include('products.urls', namespace='')),
    path('network_links/', include('network_links.urls', namespace='network_links')),
]
