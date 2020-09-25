from mainapp.models import ProductCategory


def get_categories(request):
    return {
        'categories': ProductCategory.objects.filter(is_active=True),
    }
