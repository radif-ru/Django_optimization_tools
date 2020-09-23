from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from authapp.models import ShopUser
from basketapp.models import BasketItem
from mainapp.models import Product
from mainapp.views import LINKS_MENU, get_categories


@login_required
def index(request):
    # basket_items = BasketItem.objects.filter(user=request.user)
    # basket_items = request.user.basketitem_set.all()
    # при добавлении related_name в модель .._set перестаёт работать, работает заданное имя:
    basket_items = request.user.user_basket.all()
    context = {
        'page_title': 'корзина',
        'links_menu': LINKS_MENU,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    print(request.META)
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
        basket = BasketItem(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

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
