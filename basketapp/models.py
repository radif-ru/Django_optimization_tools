from django.contrib.auth import get_user_model
from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class BasketItem(models.Model):
    # user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='user_basket'
    )
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    mod_datetime = models.DateTimeField(auto_now=True,  verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        ordering = ['product']
