from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)

    def basket_cost(self):
        return sum(item.product.price * item.quantity for item in self.user_basket.all())

    def basket_total_quantity(self):
        return sum(item.quantity for item in self.user_basket.all())

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
