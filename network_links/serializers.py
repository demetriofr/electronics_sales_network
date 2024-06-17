from rest_framework import serializers
from .models import ContactInfo, NetworkLink, NetworkLinkProduct
from .validators import LevelNoMoreOrEqualThanTwoValidator


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serializer for ContactInfo model."""

    # Exclude network_link from the required fields and mark it as write-only
    network_link = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ContactInfo
        fields = '__all__'


class NetworkLinkProductSerializer(serializers.ModelSerializer):
    """Serializer for NetworkLinkProduct model."""

    # Exclude network_link from the required fields and mark it as write-only
    network_link = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NetworkLinkProduct
        fields = '__all__'


class NetworkLinkSerializer(serializers.ModelSerializer):
    """Serializer for NetworkLink model and related models."""

    contact_info = ContactInfoSerializer()
    network_link_products = NetworkLinkProductSerializer(many=True)

    class Meta:
        model = NetworkLink
        fields = '__all__'
        read_only_fields = ['debt']
        validators = [
            LevelNoMoreOrEqualThanTwoValidator()
        ]

    def create(self, validated_data):
        """Create network_link and related models."""

        contact_info_data = validated_data.pop('contact_info')
        network_link_products_data = validated_data.pop('network_link_products')

        # Create NetworkLink instance
        network_link = NetworkLink.objects.create(**validated_data)
        network_link.save()

        # Create ContactInfo instance
        contact_info = ContactInfo.objects.create(network_link=network_link, **contact_info_data)
        contact_info.save()

        # Create NetworkLinkProduct instances
        for network_link_product_data in network_link_products_data:
            NetworkLinkProduct.objects.create(network_link=network_link, **network_link_product_data)

        # Refresh debt
        network_link.update_debt()

        return network_link

    def update(self, instance, validated_data):
        """Update network_link and related models."""

        contact_info_data = validated_data.pop('contact_info')
        network_link_products_data = validated_data.pop('network_link_products')

        # Update ContactInfo instance
        for key, value in contact_info_data.items():
            setattr(instance.contact_info, key, value)
        instance.contact_info.save()

        # Update NetworkLink instance
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Update NetworkLinkProduct instances
        for network_link_product_data in network_link_products_data:
            NetworkLinkProduct.objects.filter(
                network_link=instance,
                product=network_link_product_data['product']
            ).update(product=network_link_product_data['product'])

        # Refresh debt
        instance.update_debt()

        return instance
