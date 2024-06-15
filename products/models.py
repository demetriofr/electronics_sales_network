from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='название продукта')
    model = models.CharField(max_length=100, verbose_name='модель')
    release_date = models.DateField(verbose_name='дата выхода на рынок')

    def __str__(self):
        return f'{self.name} ({self.model})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
