from rest_framework import serializers
from .models import Product
from .validators import NoSpecialCharactersValidator


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    class Meta:
        model = Product
        fields = '__all__'
        validators = [
            NoSpecialCharactersValidator()
        ]
