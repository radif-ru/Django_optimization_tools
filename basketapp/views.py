from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from basketapp.models import BasketItem
from mainapp.models import Product
from mainapp.views import LINKS_MENU
from ordersapp.models import OrderItem


@login_required
def index(request):
    # basket_items = BasketItem.objects.filter(user=request.user)
    # basket_items = request.user.basketitem_set.all()
    # при добавлении related_name в модель .._set перестаёт работать, работает заданное имя:
    basket_items = request.user.user_basket.select_related('product',
                                                           'product__category').all()  # подтягивает вместе с данными basket
    # всё что по foreign key связано
    print('basket_items', basket_items.query)  # содержимое запроса
    context = {
        'page_title': 'корзина',
        'links_menu': LINKS_MENU,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    # print(request.META)
    # для возврата на страницу покупки, после логина при покупке товара
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:product_page', args=[pk]))

    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('auth:login'))

    # print(pk, type(pk))
    product = get_object_or_404(Product, pk=pk)
    basket = BasketItem.objects.filter(user=request.user, product=product).first()
    # basket = request.user.basketitem_set.filter(product=pk).first()

    if not basket:
        # basket = BasketItem.objects.create(user=request.user, product=product)  # not in db
        basket = BasketItem(user=request.user, product=product, quantity=1)

        # get basket.quantity -> python level -> update value -> python level -> db level
        # basket.quantity += 1
        # update value on db level
    if basket.pk:
        basket.quantity = F('quantity') + 1
    basket.save()
    db_profile_by_type(basket, 'UPDATE', connection.queries)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(BasketItem, pk=pk).delete()
    return HttpResponseRedirect(reverse('basket:index'))


def change(request, pk, quantity):
    if request.is_ajax():
        basket_item = BasketItem.objects.filter(pk=pk).first()
        if quantity == 0:
            basket_item.delete()
        else:
            if basket_item.product.quantity >= quantity:
                basket_item.quantity = quantity
            else:
                basket_item.quantity = basket_item.product.quantity
            basket_item.save()

        context = {
            'links_menu': LINKS_MENU,
            'basket_items': request.user.user_basket.all(),
        }
        basket_items = loader.render_to_string(
            template_name='basketapp/inc/inc_basket_items.html',
            context=context,
            request=request,
        )
        return JsonResponse({
            'basket_items': basket_items,
            # если делать как ниже, то basket_items не нужен
            # 'basket_cost': user.basket_cost(),
            # 'basket_total_quantity': user.basket_total_quantity(),
            # 'basket_item': basket_item,  # serialization -> drf
        })


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketItem)  # если закомментить будет работа только с заказом
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print('pre_save', type(sender))
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity

    # перехватывание ошибки при количестве товаров меньше 0:
    if instance.product.quantity <= 0:
        instance.product.quantity = 0
        # Надо разобраться как отрендерить страницу с ошибкой, render, HttpResponseRedirect не работают:
        # return HttpResponseRedirect(reverse('basket:product_quantity_err'))
        # return render(request, template_name='basketapp/product_quantity_err.html')
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketItem)  # если закомментить будет работа только с заказом
def product_quantity_update_delete(sender, instance, **kwargs):
    print('pre_delete', type(sender))
    instance.product.quantity += instance.quantity
    instance.product.save()


# def product_quantity_err(request):
#     return render(request, 'basketapp/product_quantity_err.html')


def db_profile_by_type(instance, query_type, queries):
    update_queries = list(filter(lambda x: query_type in x['sql'], queries))
    print(f'db_profile {query_type} for {instance}:')
    [print(query['sql']) for query in update_queries]
