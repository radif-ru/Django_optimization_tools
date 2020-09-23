from django import template
from django.conf import settings

register = template.Library()


def media_folder_products(string):
    """ Шаблонный фильтр медифайлов продуктовs

    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    :param string: входной путь
    :return: модифицированный путь
    """
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')  # регистрация фильтра через декоратор
def media_folder_users(string):
    """ Шаблонный фильтр медифайлов пользователей

    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    :param string: входной путь
    :return: модифицированный путь
    """
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


# регистрация фильтра, работает так же как и декоратор
register.filter('media_folder_products', media_folder_products)
