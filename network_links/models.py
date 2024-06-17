from django.db import models

from config.settings import NULLABLE


class NetworkLink(models.Model):
    """Model for save network links."""

    name = models.CharField(max_length=255, verbose_name='название')
    previous_network_link = models.ForeignKey('self',  related_name='network_link',
                                              verbose_name='предыдущее звено сети', on_delete=models.CASCADE,
                                              **NULLABLE)
    level = models.IntegerField(default=0, editable=False)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                               verbose_name='задолженность', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')

    def __str__(self):
        return self.name

    def get_level(self):
        """Calculate level of network link and update level field."""

        level = 0
        network_link = self.previous_network_link
        while network_link:
            level += 1
            network_link = network_link.previous_network_link
        self.level = level

    def update_debt(self):
        """Update debt field on based debt by products."""

        total_debt = self.network_link_products.aggregate(models.Sum('debt'))['debt__sum'] or 0
        self.debt = total_debt
        self.save()

    def save(self, *args, **kwargs):
        """Override save method for update debt."""

        self.get_level()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'звено сети'
        verbose_name_plural = 'звенья сети'


class ContactInfo(models.Model):
    """Model for save contact information."""

    network_link = models.OneToOneField('network_links.NetworkLink', related_name='contact_info',
                                        on_delete=models.CASCADE, verbose_name='звено сети')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house_number = models.CharField(max_length=5, verbose_name='номер дома')

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house_number}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'


class NetworkLinkProduct(models.Model):
    """Model for save network link products."""

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                related_name='network_link_products', verbose_name='продукт')
    network_link = models.ForeignKey(NetworkLink, on_delete=models.CASCADE,
                                     related_name='network_link_products', verbose_name='звено сети')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='задолженность за продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')

    def __str__(self):
        return f'{self.network_link} - {self.product}'

    class Meta:
        verbose_name = 'продукт звена сети'
        verbose_name_plural = 'продукты звена сети'
