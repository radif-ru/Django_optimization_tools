from django.core.cache import cache

from geekshop import settings
from mainapp.models import ProductCategory


# Пример кэширования:
def get_categories(request):
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
    else:
        links_menu = ProductCategory.objects.filter(is_active=True)

    return {
        'categories': links_menu
    }

# def get_categories(request):
#     return {
#         'categories': ProductCategory.objects.filter(is_active=True),
#     }
