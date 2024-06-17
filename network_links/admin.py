from django.contrib import admin
from django.utils.html import format_html

from network_links.models import NetworkLink, ContactInfo, NetworkLinkProduct


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number')
    search_fields = ('city',)


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1


class NetworkLinkProductInline(admin.TabularInline):
    model = NetworkLinkProduct
    extra = 1


class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'debt', 'created_at', 'contact_info_city', 'contact_info_link')
    search_fields = ('name', 'contact_info__city')
    list_filter = ('contact_info__city',)
    inlines = [ContactInfoInline, NetworkLinkProductInline]
    actions = ['clear_debt']

    def contact_info_city(self, obj):
        """Display city from contact info."""

        return obj.contact_info.city if obj.contact_info else None
    contact_info_city.short_description = 'City'

    def contact_info_link(self, obj):
        """Display link to previous network link."""

        if obj.previous_network_link:
            return format_html('<a href="{}">{}</a>',
                               obj.previous_network_link.id, obj.previous_network_link)
        return None
    contact_info_link.short_description = 'Предыдущее звено сети'

    def clear_debt(self, request, queryset):
        """Clear debt for selected network links."""

        for network_link in queryset:
            products = NetworkLinkProduct.objects.filter(network_link=network_link)
            for product in products:
                product.debt = 0
                product.save()
        queryset.update(debt=0)

    clear_debt.short_description = 'Очистить задолженность перед поставщиком у выбранных объектов'


admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(NetworkLink, NetworkLinkAdmin)
admin.site.register(NetworkLinkProduct)
