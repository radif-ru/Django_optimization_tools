from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OnlyLoggedUserMixin:
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderList(OnlyLoggedUserMixin, ListView):
    extra_context = {
        "page_title": "заказы",
    }
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    # self.request.kwargs


class OrderCreate(OnlyLoggedUserMixin, CreateView):
    extra_context = {
        "page_title": "заказы/добавить заказ",
    }

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.user_basket.select_related('user', 'product').all()
            if basket_items and len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket_items)
                )
                formset = OrderFormSet()
                # for num, form in enumerate(formset.forms):
                # zip(), filter(), map()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
                    form.initial['price'] = basket_item.product.price
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()  # Order object
            if orderitems.is_valid():
                orderitems.instance = self.object  # one to many
                orderitems.save()
            self.request.user.user_basket.all().delete()  # applied QuerySet

        # удаляем пустой заказ
        if self.object.total_cost == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(OnlyLoggedUserMixin, UpdateView):
    extra_context = {
        "page_title": "заказы/обновление заказа",
    }

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST, self.request.FILES,
                instance=self.object
            )
        else:
            queryset = self.object.orderitems.select_related('product')
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object  # можно закомментировать?
                orderitems.save()

        # удаляем пустой заказ
        if self.object.total_cost == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDetail(OnlyLoggedUserMixin, DetailView):
    extra_context = {
        "page_title": "заказы/подробности",
    }
    model = Order


class OrderDelete(OnlyLoggedUserMixin, DeleteView):
    model = Order
    extra_context = {
        "page_title": "заказы/удаление заказа",
    }
    success_url = reverse_lazy('ordersapp:index')


@login_required()
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:index'))
