import json
import os
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product
from shop.settings import BASE_DIR, JSON_PATH

with open(os.path.join(BASE_DIR, f'{JSON_PATH}/links_menu.json'),
          encoding="utf-8") as f:
    LINKS_MENU = json.loads(f.read())

with open(os.path.join(BASE_DIR, f'{JSON_PATH}/contact_locations.json'),
          encoding="utf-8") as f:
    LOCATIONS = json.loads(f.read())


def get_categories():
    return ProductCategory.objects.filter(is_active=True)


def get_products():
    return Product.objects.filter(is_active=True, category__is_active=True)


def get_hot_product():
    # products = Product.objects.all()
    # return random.choice(products)
    # Оптимизация запросов (нагрузки). Получаем все id, и из рандомного достаём объект
    products_id = get_products().values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Product.objects.get(pk=hot_product_id)


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
        'categories': get_categories(),
        'products': _related_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', context)


def product_page(request, pk):
    context = {
        'page_title': 'продукт',
        'links_menu': LINKS_MENU,
        'categories': get_categories(),
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
        'categories': get_categories(),
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
        'categories': get_categories(),
        'category': category,
        'products': all_products,
    }
    return render(request, 'mainapp/catalog.html', context)
