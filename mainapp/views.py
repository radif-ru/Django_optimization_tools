import json
import os
import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page, never_cache

from geekshop import settings
from mainapp.models import ProductCategory, Product
from geekshop.settings import BASE_DIR, JSON_PATH

# Пример кэширования:
if settings.LOW_CACHE:
    key = 'LINKS_MENU'
    LINKS_MENU = cache.get(key)
    if LINKS_MENU is None:
        with open(os.path.join(BASE_DIR, f'{JSON_PATH}/links_menu.json'),
                  encoding="utf-8", errors='ignore') as f:
            LINKS_MENU = json.loads(f.read())
        cache.set(key, LINKS_MENU)
else:
    with open(os.path.join(BASE_DIR, f'{JSON_PATH}/links_menu.json'),
              encoding="utf-8", errors='ignore') as f:
        LINKS_MENU = json.loads(f.read())

# Пример кэширования:
if settings.LOW_CACHE:
    key = 'LOCATIONS'
    LOCATIONS = cache.get(key)
    if LOCATIONS is None:
        with open(os.path.join(BASE_DIR, f'{JSON_PATH}/contact_locations.json'),
                  encoding="utf-8", errors='ignore') as f:
            LOCATIONS = json.loads(f.read())
        cache.set(key, LOCATIONS)
else:
    with open(os.path.join(BASE_DIR, f'{JSON_PATH}/contact_locations.json'),
              encoding="utf-8", errors='ignore') as f:
        LOCATIONS = json.loads(f.read())


# Пример кэширования:
def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_hot_product():
    # products = Product.objects.all()
    # return random.choice(products)
    # Оптимизация запросов (нагрузки). Получаем все id, и из рандомного достаём объект
    # products_id = get_products().values_list('id', flat=True)
    # hot_product_id = random.choice(products_id)
    # return Product.objects.get(pk=hot_product_id)
    return random.choice(get_products())


def related_products(product):
    return get_products().filter(category=product.category).exclude(id=product.id)


def index(request):
    # print(request.POST)

    featured_new_products = get_products().order_by('pk')
    all_products = get_products().order_by('price')
    context = {
        'page_title': 'INTERIOR',
        'links_menu': LINKS_MENU,
        'products': all_products[:3],
        'featured_new_products': featured_new_products[:4],
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    hot_product = get_hot_product()
    _related_products = related_products(hot_product)

    context = {
        'page_title': 'Products',
        'links_menu': LINKS_MENU,
        'products': _related_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', context)


def product_page(request, pk):
    context = {
        'page_title': 'продукт',
        'links_menu': LINKS_MENU,
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product_page.html', context)


def showroom(request, pk=0, page=1):
    if pk == 0:
        category = {'pk': 0, 'name': 'all', 'page': 1}
        all_products = get_products().order_by('-pk')
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        all_products = get_products().filter(category=category).order_by('price')

    products_paginator = Paginator(all_products, 6)
    try:
        all_products = products_paginator.page(page)
    except PageNotAnInteger:
        all_products = products_paginator.page(1)
    except EmptyPage:
        all_products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Showroom',
        'links_menu': LINKS_MENU,
        'products': all_products,
        'category': category,
    }
    return render(request, 'mainapp/showroom.html', context)


def contact(request):
    context = {
        'page_title': 'Contact',
        'locations': LOCATIONS,
        'links_menu': LINKS_MENU,
    }
    return render(request, 'mainapp/contact.html', context)


# @cache_page(3600)
# def catalog_ajax(request, pk, page=1):
#     pass
#     return render(request, 'mainapp/includes/inc__catalog.html', context)

# @cache_page(3600)
# @never_cache
def catalog(request, pk, page=1):
    # try:
    #     category = ProductCategory.objects.get(pk=pk)
    # except ...
    if pk == 0:
        category = {'pk': 0, 'name': 'all'}
        all_products = get_products().order_by('price')
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        all_products = get_products().filter(category=category).order_by('price')

    products_paginator = Paginator(all_products, 8)
    try:
        all_products = products_paginator.page(page)
    except PageNotAnInteger:
        all_products = products_paginator.page(1)
    except EmptyPage:
        all_products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Catalog',
        'links_menu': LINKS_MENU,
        'products': all_products,
        'category': category,
        'featured_new_products': all_products,
    }
    return render(request, 'mainapp/catalog.html', context)


def catalog_ajax(request, pk=None, page=1):
    if request.is_ajax():
        if pk == 0:
            category = {'pk': 0, 'name': 'all'}
            all_products = get_products().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            all_products = get_products().filter(category=category).order_by('price')

        products_paginator = Paginator(all_products, 8)
        try:
            all_products = products_paginator.page(page)
        except PageNotAnInteger:
            all_products = products_paginator.page(1)
        except EmptyPage:
            all_products = products_paginator.page(products_paginator.num_pages)

        context = {
            # 'page_title': 'Catalog',
            # 'links_menu': LINKS_MENU,
            'products': all_products,
            'category': category,
            'featured_new_products': all_products,
        }

        result = loader.render_to_string(
            template_name='mainapp/includes/inc__catalog_products.html',
            context=context,
            request=request)

        return JsonResponse({'result': result})


def product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        return JsonResponse({'price': product and product.price or 0})
